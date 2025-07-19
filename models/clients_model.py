from json import load
from pickle import NONE
import pandas as p
from openpyxl import load_workbook

class Client:
    __managed_file="data/Clients.xlsx"

    def __init__(self, nom=None, contact=None, IFU=None):
        if nom!=None and contact!=None and IFU!=None:
             file_=load_workbook(self.__managed_file)
             new_file_=file_.active
             
             if new_file_!= None :
                new_file_.append([nom, contact, IFU])
                file_.save(self.__managed_file)

    def allClients (self):
        return p.DataFrame(p.read_excel(self.__managed_file))

    def deleteClient(self, index) :
        file_=load_workbook(self.__managed_file)
        new_file_=file_.active

        if new_file_ != None :
            new_file_.delete_rows(index)
            file_.save(self.__managed_file)
            

