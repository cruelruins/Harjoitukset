teksti = "kissa juoksee ja kissa nukkuu ja kissa syö"
valinta = input("Kirjoita kirjain tai sana: ")
laskin = 0

kirjain = teksti.find(valinta)
while kirjain != -1:
    print(kirjain)
    kirjain = teksti.find(valinta, kirjain + 1)
    laskin += 1

print(valinta, "on teksissä", laskin)