teksti = "kissa juoksee ja kissa nukkuu ja kissa syö"
valinta = [
"ja", "kissa"
]
ja = 0
kissa = 0

sana = teksti.find("kissa")

while sana != -1:
    kissa += 1
    sana = teksti.find("kissa", sana + 1)

sana = teksti.find("ja")
while sana != -1:
    ja += 1
    sana = teksti.find("ja", sana + 1)


if kissa > ja:
        print("kissa", kissa)
        print("ja", ja)

elif kissa < ja:
    print("ja", ja)
    print("kissa", kissa)