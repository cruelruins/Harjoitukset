teksti = "Tervetuloa salaiseen peliin"
yrityksia = 3
arvatut_kirjaimet = []

while yrityksia > 0:

    nayta = ""
    loytyi_kaikki = True
    
    for kirjain in teksti:
        if kirjain.lower() in arvatut_kirjaimet or kirjain == " ":
            nayta += kirjain + " "
        else:
            nayta += "_ "
            loytyi_kaikki = False
    
    print(f"\nLause: {nayta}")

    if loytyi_kaikki:
        print("Hienoa! Voitit pelin!")
        break

    arvaus = input("Arvaa kirjain: ").strip().lower()

    if not arvaus:
        continue

    if arvaus in arvatut_kirjaimet:
        print(f"Olet jo arvannut kirjaimen '{arvaus}'!")
    elif arvaus in teksti.lower():
        print("Oikein! Kaikki kyseiset kirjaimet paljastettiin.")
        arvatut_kirjaimet.append(arvaus)
    else:
        yrityksia -= 1
        arvatut_kirjaimet.append(arvaus)
        print(f"Väärin! Yrityksiä jäljellä: {yrityksia}")

if yrityksia == 0:
    print(f"\nPeli päättyi. Oikea lause oli: {teksti}")