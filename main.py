# Importation des librairies
import time, calendar # Temps, date, calendrier
from datetime import datetime as dt
import pandas # Gestion des fichiers CSV

def check_time():
    now = dt.now()
    current_time = now.strftime("%H:%M")
    return current_time

class Sonnerie:
    ''' Proprietes: horaires (liste),  '''
    def __init__(self, horaires):
        self.horaires = horaires

    
primaire = Sonnerie(['07:45', '08:40', '08:45', '09:40'])
secondaire = Sonnerie(['07:45', '08:40', '08:45', '09:40'])

while True:
    if (check_time() in primaire.horaires):
        print("Sonne")
        time.sleep(60)
    else:
        print("Pas sonne")
        