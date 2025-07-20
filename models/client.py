import pandas as pd
from model import Model

class Client(Model):
    
    def __init__(self, name, contact, ifu):
        if(type(contact) != int):
            raise ClientDataError(f"Le contat {contact} n'est pas correcte.")
        
        if(len(str(contact)) != 9):
            raise ClientDataError(f"Le numéro {contact} doit être un numéro à 9 chiffres.")
        
        if(type(ifu) != int):
            raise ClientIFUError(f"Le numéro IFU {ifu} n'est pas correcte")
        
        if(len(str(ifu)) != 13):
            raise ClientIFUError(f"Le numéro IFU {ifu} doit être à 13 chiffres")
        
        new_client = pd.DataFrame({
            'code_client': [self.create_code_client()],
            'nom': [name],
            'contact': [contact],
            'IFU': [ifu]
        })

        self._add_data(new_client, "Clients.xlsx")
        

        

        
        
    def create_code_client(self):
        clients = self._get_datas()
        
        last_code = clients['code_client'].tail(1)

        last_number = int(last_code.strip('C'))
        new_client_code = ""

        if(last_number + 1 < 10):
            new_client_code = f"C00{last_number + 1}"
        elif(last_number >= 10 and last_number < 100):
            new_client_code = f"C0{last_number + 1}"
        else:
            new_client_code = f"C{last_number + 1}"

        return new_client_code



# Client Exception Definition
class ClientDataError(Exception):
    pass

class ClientIFUError(ClientDataError):
    pass