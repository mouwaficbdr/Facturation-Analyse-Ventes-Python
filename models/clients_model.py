
from pickle import NONE
import pandas as p
from openpyxl import load_workbook
from model import Model
from services.statistics_service import StatisticsService
class Client(Model):
    __managed_file="Clients.xlsx"
    __code_client_root="C"

# Sauvegarder le nouveau client crée dans le fichier excel des clients 
# si les params sont passés. 
    def __init__(self, nom=None, contact=None, IFU=None):
        if nom!=None and contact!=None and IFU!=None:
            self._createData(self.__managed_file, self.__code_client_root, [nom, contact, IFU])
            
# Retourne tous les clients sous forme de dataframes
    def getallClients (self):
        return self._getAllData(self.__managed_file);



# Test rapide de création d'entrée et affichage de toutes entrées au format JSON, venez me taper!
# print((Client('Abdel', 4582258, 779525255)).getallClients())