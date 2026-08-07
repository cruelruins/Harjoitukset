import os

def tervehdi(nimi):
    print("Hei "+ nimi + "!")

tervehdi(os.environ.get('USERNAME'))