import pandas as p
from model import Model

class Products (Model):
    __managed_file="Produits.xlsx"
    __code_produit_root="P"

    def __init__(self, libelle=None, prix_unitaire=None):
        if libelle!= None and prix_unitaire!=None :
            self._createData(self.__managed_file,self.__code_produit_root, [libelle, prix_unitaire])

    def getAllProducts(self):
        return self._getAllData(self.__managed_file)

