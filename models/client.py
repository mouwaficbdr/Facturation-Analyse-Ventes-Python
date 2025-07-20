import pandas as pd
from model import Model

class Client(Model):
    
    @staticmethod
    def add_client(name, contact, ifu):
        if(type(contact) != int):
            raise ClientDataError(f"Le contat {contact} n'est pas correcte.")
        
        if(len(str(contact)) != 9):
            raise ClientDataError(f"Le numéro {contact} doit être un numéro à 9 chiffres.")
        
        if(type(ifu) != int):
            raise ClientIFUError(f"Le numéro IFU {ifu} n'est pas correcte")
        
        if(len(str(ifu)) != 13):
            raise ClientIFUError(f"Le numéro IFU {ifu} doit être à 13 chiffres")
        
        
    




# Client Exception Definition
class ClientDataError(Exception):
    pass

class ClientIFUError(ClientDataError):
    pass