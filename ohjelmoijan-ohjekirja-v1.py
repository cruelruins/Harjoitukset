import os
import re
import sys
import time
import textwrap
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

LUA_URL = "https://www.lua.org/manual/5.4/manual.html"
PHP_URL = "https://www.php.net/manual/en/index.php"

CACHE_DIR = Path.home() / ".terminal_manuals"
LUA_CACHE = CACHE_DIR / "lua"
PHP_CACHE = CACHE_DIR / "php"

USER_AGENT = "TerminalManual/1.0 Python"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24


def pause():
    input("\nPress Enter...")


def download(url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def cached_download(url, cache_file):
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8", errors="replace")

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    html = download(url)
    cache_file.write_text(html, encoding="utf-8")
    return html


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_lines(parts):
    text = "".join(parts)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    result = []
    for line in text.split("\n"):
        line = line.rstrip()

        if not line:
            if result and result[-1] != "":
                result.append("")
            continue

        if not line.startswith("    "):
            line = re.sub(r"[ ]{2,}", " ", line)

        result.append(line)

    while result and result[0] == "":
        result.pop(0)

    while result and result[-1] == "":
        result.pop()

    return result


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current = None
        self.in_script = False
        self.in_style = False
        self.in_heading = False
        self.heading_buffer = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "script":
            self.in_script = True
            return

        if tag == "style":
            self.in_style = True
            return

        if tag in ("h1", "h2", "h3", "h4"):
            if self.current is not None:
                self.finish_section()

            self.in_heading = True
            self.heading_buffer = []
            return

        if tag == "br":
            self.add_text("\n")
        elif tag in ("p", "div", "li", "pre", "blockquote", "tr"):
            self.add_text("\n")
        elif tag == "td":
            self.add_text("    ")

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "script":
            self.in_script = False
            return

        if tag == "style":
            self.in_style = False
            return

        if tag in ("h1", "h2", "h3", "h4"):
            title = clean_text(" ".join(self.heading_buffer))
            self.current = {"title": title, "lines": []}
            self.sections.append(self.current)
            self.in_heading = False
            self.heading_buffer = []
            return

        if tag in ("p", "div", "li", "pre", "blockquote", "tr"):
            self.add_text("\n")

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return

        if self.in_heading:
            self.heading_buffer.append(data)
        else:
            self.add_text(data)

    def add_text(self, text):
        if self.current is not None:
            self.current["lines"].append(
                text.replace("\xa0", " ").replace("\t", "    ")
            )

    def finish_section(self):
        if self.current is not None:
            self.current["lines"] = clean_lines(self.current["lines"])


def parse_sections(html):
    parser = TextParser()
    parser.feed(html)

    if parser.current is not None:
        parser.finish_section()

    return [
        section
        for section in parser.sections
        if section["title"] or section["lines"]
    ]


class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self.current_href = None
        self.current_text = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "script":
            self.in_script = True
            return

        if tag == "style":
            self.in_style = True
            return

        if tag != "a":
            return

        attributes = dict(attrs)
        href = attributes.get("href")

        if href:
            self.current_href = href
            self.current_text = []

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return

        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "script":
            self.in_script = False
            return

        if tag == "style":
            self.in_style = False
            return

        if tag != "a":
            return

        if self.current_href is not None:
            absolute = urljoin(self.base_url, self.current_href)
            title = clean_text(" ".join(self.current_text))
            self.links.append((absolute, title))

        self.current_href = None
        self.current_text = []


class LuaManual:
    def __init__(self):
        self.sections = []

    def load(self):
        cache = LUA_CACHE / "manual.html"
        html = cached_download(LUA_URL, cache)
        self.sections = parse_sections(html)

    def search(self, query):
        query = query.lower()
        results = []

        for index, section in enumerate(self.sections):
            text = (
                section["title"] + "\n" +
                "\n".join(section["lines"])
            ).lower()

            if query in text:
                results.append(index)

        return results


class PHPManual:
    def __init__(self):
        self.pages = {}
        self.load_index()

    def url_to_filename(self, url):
        parsed = urlparse(url)
        name = parsed.path.rstrip("/").replace("/", "_")

        if not name:
            name = "index"

        if parsed.query:
            name += "_" + re.sub(r"[^a-zA-Z0-9_-]", "_", parsed.query)

        return name + ".html"

    def cache_file(self, url):
        return PHP_CACHE / self.url_to_filename(url)

    def allowed_url(self, url):
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and parsed.netloc == "www.php.net"
            and parsed.path.startswith("/manual/en/")
            and parsed.path.endswith(".php")
        )

    def load_page(self, url):
        if url in self.pages and self.pages[url]["loaded"]:
            return self.pages[url]

        try:
            html = cached_download(url, self.cache_file(url))
        except Exception as error:
            print(f"\nCould not download:\n{url}\n{error}")
            pause()
            return None

        sections = parse_sections(html)
        title = sections[0]["title"] if sections else url

        page = {
            "url": url,
            "title": title,
            "sections": sections,
            "loaded": True,
        }

        self.pages[url] = page
        return page

    def discover_links(self, url, html):
        parser = LinkParser(url)
        parser.feed(html)

        new_pages = []

        for link, title in parser.links:
            link = link.split("#", 1)[0]

            if not self.allowed_url(link):
                continue

            if link not in self.pages:
                self.pages[link] = {
                    "url": link,
                    "title": title or link,
                    "sections": [],
                    "loaded": False,
                }
                new_pages.append(link)
            elif title and self.pages[link]["title"] == link:
                self.pages[link]["title"] = title

        return new_pages

    def load_index(self):
        cache = self.cache_file(PHP_URL)
        html = cached_download(PHP_URL, cache)

        self.pages[PHP_URL] = {
            "url": PHP_URL,
            "title": "PHP Manual",
            "sections": parse_sections(html),
            "loaded": True,
        }

        self.discover_links(PHP_URL, html)

    def discover_everything(self):
        print("\nDiscovering PHP manual pages...")
        queue = [PHP_URL]
        seen = set()

        while queue:
            url = queue.pop(0)

            if url in seen:
                continue

            seen.add(url)

            print(
                f"\rDiscovered: {len(self.pages):5} pages",
                end="",
                flush=True,
            )

            try:
                html = cached_download(url, self.cache_file(url))
                new_pages = self.discover_links(url, html)
                queue.extend(new_pages)
            except Exception:
                pass

        print()
        print(f"Total discovered pages: {len(self.pages)}")

    def download_everything(self):
        self.discover_everything()

        urls = list(self.pages)
        print("\nDownloading PHP manual...")

        for number, url in enumerate(urls, 1):
            print(
                f"\rDownloading {number}/{len(urls)}",
                end="",
                flush=True,
            )

            try:
                self.load_page(url)
            except Exception:
                pass

            time.sleep(0.02)

        print("\nFinished.")

    def search(self, query):
        query = query.lower()
        results = []

        for url, page in self.pages.items():
            if not page["loaded"]:
                continue

            text = page["title"].lower()

            for section in page["sections"]:
                text += "\n" + section["title"].lower()
                text += "\n" + "\n".join(section["lines"]).lower()

            if query in text:
                results.append(url)

        return results


def wrap_lines(lines, width):
    result = []

    for line in lines:
        if not line:
            result.append("")
            continue

        if line.startswith("    "):
            result.append(line)
            continue

        wrapped = textwrap.wrap(
            line,
            width=max(20, width),
            replace_whitespace=False,
            drop_whitespace=True,
        )

        result.extend(wrapped if wrapped else [""])

    return result


def collect_section_text(section):
    output = []

    if section["title"]:
        output.extend([section["title"], ""])

    output.extend(section["lines"])
    return output


def view_lua_section(manual, index):
    section = manual.sections[index]
    lines = collect_section_text(section)
    position = 0

    while True:
        clear()
        cols, rows = terminal_size()
        width = max(40, cols - 4)

        print("=" * cols)
        print(" LUA 5.4 MANUAL")
        print(f" Section {index + 1}/{len(manual.sections)}")
        print(f" {section['title']}")
        print("=" * cols)

        wrapped = wrap_lines(lines, width)
        height = max(5, rows - 7)

        chunk = wrapped[position:position + height]
        print("\n".join(chunk))
        new_position = min(position + height, len(wrapped))

        print("\n" + "-" * cols)

        if new_position >= len(wrapped):
            print("[Enter] return  [n] next  [p] previous  [q] contents")
        else:
            print("[Enter] next page  [q] contents")

        command = input("> ").strip().lower()

        if command == "q":
            return
        if command == "n" and index + 1 < len(manual.sections):
            view_lua_section(manual, index + 1)
            return
        if command == "p" and index > 0:
            view_lua_section(manual, index - 1)
            return
        if new_position >= len(wrapped):
            return

        position = new_position


def lua_contents(manual):
    while True:
        clear()
        cols, _ = terminal_size()

        print("=" * cols)
        print(" LUA 5.4 MANUAL")
        print(" Contents")
        print("=" * cols)
        print()

        for i, section in enumerate(manual.sections, 1):
            print(f"{i:4}. {section['title']}")

        print("\n" + "-" * cols)
        print("number = open   s = search   q = back")

        command = input("> ").strip().lower()

        if command == "q":
            return

        if command == "s":
            query = input("\nSearch Lua manual: ").strip()
            if not query:
                continue

            results = manual.search(query)
            clear()

            print("=" * cols)
            print(" LUA SEARCH RESULTS")
            print("=" * cols)
            print()

            for n, index in enumerate(results, 1):
                print(f"{n:4}. {manual.sections[index]['title']}")

            if results:
                choice = input("\nOpen result number: ").strip()
                try:
                    selected = int(choice) - 1
                    if 0 <= selected < len(results):
                        view_lua_section(manual, results[selected])
                except ValueError:
                    pass
            else:
                print("No results.")

            pause()
            continue

        try:
            number = int(command)
            if 1 <= number <= len(manual.sections):
                view_lua_section(manual, number - 1)
        except ValueError:
            pass


def view_php_page(manual, url):
    page = manual.load_page(url)

    if page is None:
        return

    if not page["sections"]:
        print("No readable content found.")
        pause()
        return

    section_index = 0

    while section_index < len(page["sections"]):
        section = page["sections"][section_index]
        lines = collect_section_text(section)
        position = 0

        while position < len(lines):
            clear()
            cols, rows = terminal_size()
            width = max(40, cols - 4)

            print("=" * cols)
            print(" PHP MANUAL")
            print(f" {page['title']}")
            print(
                f" Section {section_index + 1}/"
                f"{len(page['sections'])}"
            )
            print("=" * cols)

            wrapped = wrap_lines(lines, width)
            height = max(5, rows - 7)

            chunk = wrapped[position:position + height]
            print("\n".join(chunk))

            new_position = min(position + height, len(wrapped))

            print("\n" + "-" * cols)

            if new_position < len(wrapped):
                print("[Enter] next page  [q] return")
            else:
                print(
                    "[Enter] next section  "
                    "[p] previous section  "
                    "[q] return"
                )

            command = input("> ").strip().lower()

            if command == "q":
                return

            if command == "p":
                break

            position = new_position

        else:
            section_index += 1


def php_contents(manual):
    while True:
        clear()
        cols, _ = terminal_size()

        print("=" * cols)
        print(" PHP MANUAL")
        print(" Contents")
        print("=" * cols)
        print()

        pages = list(manual.pages.items())

        for i, (url, page) in enumerate(pages, 1):
            status = "" if page["loaded"] else "*"
            print(f"{i:4}. {status}{page['title']}")

        print("\n* = discovered but not downloaded")
        print("\n" + "-" * cols)
        print("number = open")
        print("s = search downloaded pages")
        print("a = discover + download ALL PHP pages")
        print("r = refresh PHP index")
        print("q = back")

        command = input("> ").strip().lower()

        if command == "q":
            return

        if command == "a":
            clear()
            try:
                manual.download_everything()
            except KeyboardInterrupt:
                print("\nStopped by user.")
            pause()
            continue

        if command == "r":
            try:
                manual.load_index()
            except Exception as error:
                print(f"\nRefresh failed: {error}")
                pause()
            continue

        if command == "s":
            query = input("\nSearch PHP manual: ").strip()
            if not query:
                continue

            results = manual.search(query)
            clear()

            print("=" * cols)
            print(" PHP SEARCH RESULTS")
            print("=" * cols)
            print()

            for i, url in enumerate(results, 1):
                print(f"{i:4}. {manual.pages[url]['title']}")

            print()

            if results:
                choice = input("Open result number: ").strip()
                try:
                    selected = int(choice) - 1
                    if 0 <= selected < len(results):
                        view_php_page(manual, results[selected])
                except ValueError:
                    pass
            else:
                print(
                    "No results in downloaded pages. "
                    "Use 'a' to download everything."
                )
                pause()

            continue

        try:
            number = int(command)
            if 1 <= number <= len(pages):
                view_php_page(manual, pages[number - 1][0])
        except ValueError:
            pass


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    lua = None
    php = None

    while True:
        clear()
        cols, _ = terminal_size()

        print("=" * cols)
        print(" TERMINAL PROGRAMMING MANUALS")
        print("=" * cols)
        print()
        print(" 1. Lua 5.4 Manual")
        print(" 2. PHP Manual")
        print(" q. Quit")
        print()

        command = input("> ").strip().lower()

        if command == "q":
            clear()
            return

        if command == "1":
            if lua is None:
                print("\nLoading Lua 5.4 manual...")
                try:
                    lua = LuaManual()
                    lua.load()
                except Exception as error:
                    print(f"\nCould not load Lua manual:\n{error}")
                    pause()
                    continue

            lua_contents(lua)

        elif command == "2":
            if php is None:
                clear()
                print("Loading PHP manual index...")
                try:
                    php = PHPManual()
                except Exception as error:
                    print(f"\nCould not load PHP manual:\n{error}")
                    pause()
                    continue

            php_contents(php)


if __name__ == "__main__":
    main()
