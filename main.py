# Importation des librairies
import time, calendar # Temps, date, calendrier
import datetime as dt
import csv # Gestion des fichiers CSV
from pygame import mixer # Gestion du son
from gpiozero import Button
import tm1637

button_s=Button(2)
button_i=Button(3)

tm = tm1637.TM1637(clk=14, dio=4)

# Lire le fichier CSV
fichierDataVacances = open("data/vacances.csv", "r")
tableDataVacances = csv.DictReader(fichierDataVacances, delimiter=",")
dataVacances = [ligne for ligne in tableDataVacances]
fichierDataHoraires = open("data/horaires.csv", "r")
tableDataHoraires = csv.DictReader(fichierDataHoraires, delimiter=",")
dataHoraires = [dict(ligne) for ligne in tableDataHoraires]

# Variables des vacances + sonneries
vacances = []
for i in range(len(dataVacances)):
    vacances.append((dataVacances[i]['DATEDEBUT'], dataVacances[i]['DATEFIN']))

horairePrimaire=[]
horaireSecondaire=[]
for i in range(len(dataHoraires)):
    horairePrimaire.append(dataHoraires[i]['PRIMAIRE'])
    horaireSecondaire.append(dataHoraires[i]['SECONDAIRE'])

# Variables alarmes
check_alarme_s = False #alarme seisme
check_alarme_i = False #alarme intrusion

# Variables vers les ficihers de son
sonPrimaire = "sons/primaire.wav"
sonSecondaire = "sons/secondaire.wav"
sonMatinale = "sons/matinale.wav"
sonSeisme = "sons/earthquake.mp3"
sonIntrusion = "sons/intrusion.mp3"

# Initialiser la module de mixer de pygame pour le son
mixer.init()
mixer.Channel(0)
mixer.Channel(1)
mixer.Channel(2)

# Fonctions
def check_time():
    ''' Fonction qui renvoie le temps actuel en string de format H:M:S '''
    current_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:-5]
    return current_time

def check_date():
    ''' Fonction qui renvoie le temps actuel en string de format J:M:A '''
    current_date = dt.datetime.now().strftime("%Y-%m-%d")
    return current_date

def sonner(nom, son):
    # Fonction pour mettre le son en marche
    print(f"SONNERIE {nom} EN MARCHE")
    mixer.Channel(0).play(mixer.Sound(son)) # Play le son

def check_vacances_ferie():
    '''
    str, str -> bool
    Fonction qui prend en entrée la date du debut et de la fin des vacances et renvoie True si le jour d'aujourd'hui se situe entre ces 2 dates
    '''
    clesvacances = False
    for i in range(len(vacances)):
        mois = int(check_date()[5:7])
        moisDebut = int(vacances[i][0][5:7])
        moisFin = int(vacances[i][1][5:7])
        jour = int(check_date()[8:10])
        jourDebut = int(vacances[i][0][8:10])
        jourFin = int(vacances[i][1][8:10])
        
        if mois==moisDebut==moisFin:
            if jour>=jourDebut and jour<=jourFin:
                clesvacances = True
        elif mois==moisDebut:
            if jour>=jourDebut:
                clesvacances = True
        elif mois==moisFin:
            if jour<=jourFin:
                clesvacances = True
        elif mois>moisDebut and mois<moisFin:
            clesvacances = True
    return clesvacances


while True:
    # Check le temps et le mettre dans la variable t
    t = check_time()
    d = check_date()
    date = dt.date(int(d[0:4]), int(d[5:7]), int(d[8:10]))

    if check_alarme_s==False and check_alarme_i==False:
        # Check si on est en vacances ou un jour ferie
        if check_vacances_ferie():
            # Si on est en vacances ou un jour ferie
            print("EN VACANCES, PAS DE SONNERIE")
        else:
            #Si on est pas ni en vacances ni dans un jour ferie
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
    
    # Alertes
    if (button_s.is_pressed): # Bouton seisme clique (changer avec bouton au lieu de keyboard)
        if check_alarme_s==False:
            mixer.Channel(0).stop()
            mixer.Channel(1).stop()
            mixer.Channel(2).play(mixer.Sound(sonSeisme), -1)
            check_alarme_s=True
        else:
            mixer.Channel(2).stop()
            check_alarme_s=False

    if (button_i.is_pressed): # Bouton intrusion clique (changer avec bouton au lieu de keyboard)
        if check_alarme_i==False:
            mixer.Channel(0).stop()
            mixer.Channel(1).stop()
            mixer.Channel(2).play(mixer.Sound(sonIntrusion), -1)
            check_alarme_i=True
        else:
            mixer.Channel(2).stop()
            check_alarme_i=False
            
    tm.numbers(int(t[:2]),int(t[3:5]))