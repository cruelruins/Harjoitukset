teksti = "kissa juoksee ja kissa nukkuu ja kissa syö"

kissa = 0
ja = 0


sana = teksti.find("kissa")
while sana != -1:
    kissa += 1
    sana = teksti.find("kissa", sana + 1)


sana = teksti.find("ja")
while sana != -1:
    ja += 1
    sana = teksti.find("ja", sana + 1)

print(f"Kissoja löytyi: {kissa}")
print(f"Ja sanoja löytyi: {ja}")

if kissa > ja:
    print("Kissoja on enemmän")
elif kissa < ja:
    print("Ja-sanoja on enemmän")
