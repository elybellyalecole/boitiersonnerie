# Importation des librairies
import time, datetime, calendar # Temps, date, calendrier
import pandas # Gestion des fichiers CSV

class Sonnerie:
    ''' Proprietes: horaires (liste),  '''
    def __init__(self, horaires):
        self.horaires = horaires

    def check_sonnerie(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")