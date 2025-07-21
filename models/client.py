import pandas as pd
from models.model import Model

class Client(Model):
    
    def __init__(self, name, contact, ifu, file = "Clients.xlsx"):
        if type(contact) != int:
            raise ClientDataError(f"Le contat {contact} n'est pas correcte.")
        
        if len(str(contact)) != 9:
            raise ClientDataError(f"Le numéro {contact} doit être un numéro à 9 chiffres.")
        
        if type(ifu) != int:
            raise ClientIFUError(f"Le numéro IFU {ifu} n'est pas correcte")
        
        if len(str(ifu)) != 13:
            raise ClientIFUError(f"Le numéro IFU {ifu} doit être à 13 chiffres")
        
        clients_ifu = pd.DataFrame(self._getAllData(file))
        if not clients_ifu[clients_ifu['IFU'] == ifu].empty:
            raise ClientIFUError(f"Le numéro IFU {ifu} existe déjà (Vous êtes suspect !!).")

        self._createData(file, 'C', [name, contact, ifu])


    # Retourne tous les clients sous forme de liste de dictionnaire
    @staticmethod
    def getallClients ():
        return Model._getAllData(Client, "Clients.xlsx")
    


# Client Exception Definition
class ClientDataError(Exception):
    pass

class ClientIFUError(ClientDataError):
    pass