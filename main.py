from models.client import Client, ClientIFUError, ClientDataError

try:
    andy = Client('Andy', 900993248, 1234567890769)
    

except ClientIFUError as e:
    print(f"Erreur: {e}")