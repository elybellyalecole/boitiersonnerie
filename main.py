# Importation des librairies
import time, calendar # Temps, date, calendrier
import datetime as dt
import pandas # Gestion des fichiers CSV
from pygame import mixer # Gestion du son
# import RPi.GPIO as GPIO # Gestion du Raspberry Pi

# Variables vers les ficihers de son
sonPrimaire = "./sons/primaire.wav"
sonSecondaire = "./sons/secondaire.wav"
sonMatinale = "./sons/matinale.wav"

# Variables des sonneries
horairePrimaire = ["07:45:00.0", "08:30:00.0", "09:15:00.0", "09:45:00.0", "10:15:00.0", "10:45:00.0", "11:00:00.0", "11:45:00.0", "13:00:00.0", "13:45:00.0", "14:30:00.0"]
horaireSecondaire = ["07:45:30.0", "08:40:00.0", "08:45:00.0", "09:40:00.0", "10:00:00.0", "10:55:00.0", "11:00:30.0", "11:55:00.0", "12:00:00.0", "12:55:00.0", "13:50:00.0", "14:45:00.0", "14:50:00.0", "15:45:00.0", "15:55:00.0", "16:50:00.0", "16:55:00.0", "17:50:00.0"]

# Variables des jours ou la sonnerie ne sonne pas (vacances + jours feries + weekend)
joursnonsonne = []

# Initialiser la module de mixer de pygame pour le son
mixer.init()

def check_time():
    ''' Fonction qui renvoie le temps actuel en string de format H:M:S '''
    current_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:-5]
    return current_time

def check_date():
    ''' Fonction qui renvoie le temps actuel en string de format H:M:S '''
    current_date = dt.datetime.now().strftime("%Y-%m-%d")
    return current_date

def sonner(nom, son):
    # Fonction pour mettre le son en marche
    print(f"SONNERIE {nom} EN MARCHE")
    mixer.Channel(0).play(mixer.Sound(son)) # Play le son


while True:
    # Check le temps et le mettre dans la variable t
    t = check_time()
    d = check_date()
    date = dt.date(int(d[0:4]), int(d[5:7]), int(d[8:10]))

    # Si on est pas en weekend
    if date.weekday() <= 4:
        # Musique matinale 7:35:00 - 7:45:00
        if (t=="07:35:00.0"):
            print("MUSIQUE MATINALE EN MARCHE")
            mixer.Channel(1).play(mixer.Sound(sonMatinale), -1, 600000) # Play le son sonMatinale avec un loop de -1 (infini) pour 600000ms (10min)

        # Si on est le Vendredi

        # Sonneries primaire/secondaire
        if (t in horairePrimaire):
            sonner("PRIMAIRE", sonPrimaire)
        elif (t in horaireSecondaire):
            sonner("SECONDAIRE", sonSecondaire)
    else:
        print("Weekend, pas de sonnerie")
        