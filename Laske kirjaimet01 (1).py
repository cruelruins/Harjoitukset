teksti = "Tietokoneet tekevät töitä tänäänkin todella tehokkaasti"

valinta = input("Kirjoita kirjain: ")

kirjain = teksti.find(valinta)
while kirjain != -1:
    print(kirjain)
    kirjain = teksti.find(valinta, kirjain + 1)