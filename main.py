# Importation des librairies
import time, calendar # Temps, date, calendrier
import datetime as dt
import pandas as pd # Gestion des fichiers CSV
from pygame import mixer # Gestion du son
# import RPi.GPIO as GPIO # Gestion du Raspberry Pi

# Lire le fichier CSV
dataVacances = pd.read_csv("data/vacances.csv")
dataHoraires = pd.read_csv("data/horaires.csv")

# Variables des vacances + sonneries
vacances = []
for i in range(len(dataVacances)):
    vacances.append((dataVacances['DATEDEBUT'][i], dataVacances['DATEFIN'][i]))
print(vacances)
horairePrimaire = dataHoraires['PRIMAIRE'].tolist()
horaireSecondaire = dataHoraires['SECONDAIRE'].tolist()


# Variables vers les ficihers de son
sonPrimaire = "./sons/primaire.wav"
sonSecondaire = "./sons/secondaire.wav"
sonMatinale = "./sons/matinale.wav"


# Variables des jours ou la sonnerie ne sonne pas (vacances + jours feries + weekend)
joursnonsonne = []

# Initialiser la module de mixer de pygame pour le son
mixer.init()

# Fonctions
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

def check_vacances(dateDebut, dateFin):
    '''
    str, str -> bool
    Fonction qui prend en entrée la date du debut et de la fin des vacances et renvoie True si le jour d'aujourd'hui se situe entre ces 2 dates
    '''
    mois = int(check_date()[5:7])
    moisDebut = int(dateDebut[5:7])
    moisFin = int(dateFin[5:7])
    jour = int(check_date()[8:10])
    jourDebut = int(dateDebut[8:10])
    jourFin = int(dateFin[8:10])
    
    if mois==moisDebut==moisFin:
        if jour>=jourDebut and jour<=jourFin:
            return True
    elif mois==moisDebut:
        if jour>=jourDebut:
            return True
    elif mois==moisFin:
        if jour<=jourFin:
            return True
    elif mois>moisDebut and mois<moisFin:
        return True

    return False

assert check_vacances('2024-02-05', '2024-02-12') == True
assert check_vacances('2024-01-12', '2024-02-12') == True
assert check_vacances('2023-01-12', '2024-02-12') == True
assert check_vacances('2024-05-12', '2024-06-12') == False
assert check_vacances('2024-01-10', '2024-03-10') == True
    

while True:
    # Check le temps et le mettre dans la variable t
    t = check_time()
    d = check_date()
    date = dt.date(int(d[0:4]), int(d[5:7]), int(d[8:10]))

    # Check si on est en vacances
    if check_vacances():
        # Si on est en vacances
        print("EN VACANCES, PAS DE SONNERIE")
    else:
        #Si on est pas en vacances
        # Check si on est en weekday
        if date.weekday() <= 4:
            # Musique matinale 7:35:00 - 7:45:00
            if (t=="07:35:00.0"):
                print("MUSIQUE MATINALE EN MARCHE")
                mixer.Channel(1).play(mixer.Sound(sonMatinale), -1, 600000) # Play le son sonMatinale avec un loop de -1 (infini) pour 600000ms (10min)

            # Check si on est le Vendredi
            if date.weekday() == 4:
                # Sonneries primaire/secondaire seulement jusqu'a 11:45 et 12:55 (respectivement)
                if (t in horairePrimaire[:8]):
                    sonner("PRIMAIRE", sonPrimaire)
                elif (t in horaireSecondaire[:10]):
                    sonner("SECONDAIRE", sonSecondaire)
            else:
                # Sonneries primaire/secondaire
                if (t in horairePrimaire):
                    sonner("PRIMAIRE", sonPrimaire)
                elif (t in horaireSecondaire):
                    sonner("SECONDAIRE", sonSecondaire)
        # Si on est en weekend
        else:
            print("EN WEEKEND, PAS DE SONNERIE")
        