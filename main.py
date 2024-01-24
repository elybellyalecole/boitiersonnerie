# Importation des librairies
import time, calendar # Temps, date, calendrier
from datetime import datetime as dt
import pandas # Gestion des fichiers CSV
from playsound import playsound as ps

def check_time():
    now = dt.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

class Sonnerie:
    ''' Proprietes: horaires (liste),  '''
    def __init__(self, nom, horaires, son):
        self.nom = nom
        self.horaires = horaires
        self.son = son
    
    def sonner(self):
        print(f"SONNERIE {self.nom} EN MARCHE")
        ps(self.son)
        print("SONNERIE TERMINEE")

memetemps = ['7:45:00', '11:00:00']
primaire = Sonnerie('PRIMAIRE', ['07:45:00', '08:30:00', '09:15:00', '09:30:00', '10:15:00', '10:45:00', '11:00:00', '11:45:00', '13:00:00', '13:45:00', '14:30:00'], './sons/primaire.mp3')
secondaire = Sonnerie('SECONDAIRE', ['07:45:00', '08:40:00', '08:45:00', '09:40:00', '10:00:00', '10:55:00', '11:00:00', '11:55:00', '12:00:00', '12:55:00', '13:50:00', '14:45:00', '14:50:00', '15:45:00', '15:55:00', '16:50:00', '16:55:00', '17:50:00'], './sons/secondaire.mp3')

while True:
    t = check_time()
    if (t in memetemps):
        primaire.sonner()
        time.sleep(10)
    elif (t in primaire.horaires):
        primaire.sonner()
    elif (t in secondaire.horaires):
        secondaire.sonner()
    print("EN ATTENTE D'UNE SONNERIE")