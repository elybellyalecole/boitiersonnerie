# Importation des librairies
import time, calendar # Temps, date, calendrier
from datetime import datetime as dt
import pandas # Gestion des fichiers CSV
from pygame import mixer

# Variables vers les ficihers de son
sonPrimaire = "./sons/primaire.wav"
sonSecondaire = "./sons/secondaire.wav"
sonMatinale = "./sons/matinale.wav"

def check_time():
    ''' Fonction qui renvoie le temps actuel en string de format H:M:S '''
    now = dt.now()
    current_time = now.strftime("%H:%M:%S.%f")[:-5]
    return current_time

# Initialiser la module de mixer de pygame pour le son
mixer.init()

class Sonnerie:
    '''
    Classe pour chaque sonnerie differente
    Propriétés: nom de la sonnerie (str), horaires (liste), directoire son (string)
    '''
    def __init__(self, nom, horaires, son):
        # Initialiser les variables de la classe
        self.nom = nom
        self.horaires = horaires
        self.son = son
    
    def sonner(self):
        # Fonction pour mettre le son en marche
        print(f"SONNERIE {self.nom} EN MARCHE")
        mixer.Channel(0).play(mixer.Sound(self.son)) # Play le son

memetemps = ["7:45:00.0", "11:00:00.0"]
primaire = Sonnerie("PRIMAIRE", ["07:45:00.0", "08:30:00.0", "09:15:00.0", "09:45:00.0", "10:15:00.0", "10:45:00.0", "11:00:00.0", "11:45:00.0", "13:00:00.0", "13:45:00.0", "14:30:00.0"], sonPrimaire)
secondaire = Sonnerie("SECONDAIRE", ["07:45:00.0", "08:40:00.0", "08:45:00.0", "09:40:00.0", "10:00:00.0", "10:55:00.0", "11:00:00.0", "11:55:00.0", "12:00:00.0", "12:55:00.0", "13:50:00.0", "14:45:00.0", "14:50:00.0", "15:45:00.0", "15:55:00.0", "16:50:00.0", "16:55:00.0", "17:50:00.0"], sonSecondaire)

while True:
    # Check le temps et le mettre dans la variable t
    t = check_time()

    print(t)

    # Musique matinale 7:35:00 - 7:45:00
    if (t=="07:35:00.0"):
        print("MUSIQUE MATINALE EN MARCHE")
        mixer.Channel(1).play(mixer.Sound(sonMatinale), -1, 600000) # Play le son sonMatinale avec un loop de -1 (infini) pour 600000ms (10min)

    # Sonneries primaire/secondaire
    if (t in memetemps):
        primaire.sonner()
        time.sleep(10) 
    elif (t in primaire.horaires):
        primaire.sonner()
    elif (t in secondaire.horaires):
        secondaire.sonner()