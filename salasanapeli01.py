teksti = "Todella Todella mahtava"
yrityksiä = 3

while yrityksiä > 0:
    sana = input("Arvaa sana: ")
    etsi = teksti.find(sana)

    if etsi != -1 and etsi != +1:
        print(f"Sana löytyi kohdasta: {1::etsi}")
        break

    else:
        yrityksiä -= 1
        print(f"Ei löytynyt.")
        print("Yrityksiä jäljellä:", yrityksiä)

if yrityksiä == 0:
    print("Liian monta yritystä!")