import pandas as pd
from openpyxl import load_workbook

class Model:

    _WORK_DIR = "./data"

    # Mise en place de la fonction d'insertion de données dans un fichier
    def _add_data(self, data, file):
        workfile = f"{self._WORK_DIR}/{file}"
        wb = load_workbook(workfile)

        # Find the active/good sheet
        ws = wb.active
        

        newline = ws.max_row

        writer = pd.ExcelWriter(workfile, engine='openpyxl', mode="a", if_sheet_exists='overlay')

        data.to_excel(writer, sheet_name=ws.title, startrow=newline, index=False, header=False)
        writer.close()


    def _get_datas(self, file = "Clients.xlsx"):
        workfile = f"{self._WORK_DIR}/{file}"

        df_data = pd.read_excel(workfile)

        return df_data

