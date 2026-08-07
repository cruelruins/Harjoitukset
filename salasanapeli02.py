teksti = "Tervetuloa_salaiseen_peliin"
yrityksia = 3
loytyneet_indeksi = 0

while yrityksia > 0:

    nayta = ""
    for i in range(len(teksti)):
        if i < loytyneet_indeksi:
            nayta += teksti[i] + " "
        else:
            nayta += "___ "
    
    print(f"\nLause: {nayta}")
    arvaus = input("Arvaa seuraava sana: ").strip()


    if arvaus.lower() == teksti[loytyneet_indeksi].lower():
        print("Oikein!")
        loytyneet_indeksi += 1
        

        if loytyneet_indeksi == len(teksti):
            print(f"Hienoa! Lause oli: {teksti}")
            break
    else:
        yrityksia -= 1
        print(f"Väärin! Yrityksiä jäljellä: {yrityksia}")

if yrityksia == 0:
    print(f"\nPeli päättyi. Et löytänyt koko lausetta.")