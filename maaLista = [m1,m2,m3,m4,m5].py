teksti = "Tervetuloa salaiseen peliin"
sana = input("Arvaa sana: ")

etsi = teksti.find(sana)

if etsi == -1:
    print("Ei löytynyt.")

else:
    print(f"Sana löytyi kohdasta: {etsi}")
