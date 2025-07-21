from models.model import Model
from models.client import ClientCodeError
from models.client import Client
from services import 

def insert_facture(code_client):
    if(Client._findEntry("Clients.xlsx", "code_client", code_client)):
        