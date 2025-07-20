import pandas as pd
from openpyxl import load_workbook

class Model:

    _WORK_DIR = "./data/"

    # Mise en place de la fonction d'insertion de données dans un fichier
    def add_data(self, data, file):
        workfile = self._WORK_DIR + file
        wb = load_workbook(workfile)

        # Find the active/good sheet
        ws = wb.active

        newline = ws.max_row

        writer = pd.ExcelWriter(workfile, engine='openpyxl', if_sheet_exists=ws, mode="a")

        data.to_excel(writer, startrow=newline, index=False, header=False)
        writer.close()

