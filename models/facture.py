import pandas as pd
from datetime import datetime
import os

class FactureManager:
    def __init__(self, data_folder="export"):
        """Initialise le gestionnaire de factures"""
        os.makedirs(data_folder, exist_ok=True)
        self.INVOICES_FILE = os.path.join(data_folder, "historique_factures.xlsx")
        self._initialize_invoices_file()
        
    def _initialize_invoices_file(self):
        """Crée le fichier d'historique des factures s'il n'existe pas"""
        if not os.path.exists(self.INVOICES_FILE):
            columns = [
                "numero_facture",
                "date",
                "code_client",
                "nom_client",
                "produits",
                "quantites",
                "prix_unitaire",
                "total_ht",
                "remise",
                "tva",
                "total_ttc"
            ]
            pd.DataFrame(columns=columns).to_excel(self.INVOICES_FILE, index=False)


    def ajouter_facture(self, numero_facture, remise, client, produits):
        """
        Ajoute une facture à l'historique, une ligne par produit.
        :param numero_facture: Numéro unique de facture
        :param client: Dictionnaire contenant les infos client
        :param produits: Liste de dictionnaires des produits
        """
        try:
            lignes = []
            for p in produits:
                montant_ht = p['quantite'] * p['prix']
                montant_remise = montant_ht * (1 - remise/100)
                tva = montant_remise * 0.18
                montant_ttc = montant_remise + tva
                ligne = {
                    "numero_facture": numero_facture,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "code_client": client['code'],
                    "nom_client": client['nom'],
                    "produits": p['code'],
                    "quantites": p['quantite'],
                    "prix_unitaire": f"{p['prix']:.2f}",
                    "total_ht": f"{montant_ht:.2f}",
                    "remise": f"{remise}%",
                    "tva": f"{tva:.2f}",
                    "total_ttc": f"{montant_ttc:.2f}"
                }
                lignes.append(ligne)

            # Mise à jour du fichier
            df = pd.read_excel(self.INVOICES_FILE)
            df = pd.concat([df, pd.DataFrame(lignes)], ignore_index=True)
            df.to_excel(self.INVOICES_FILE, index=False)

            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture : {str(e)}")
            return False


    def get_historique_complet(self):
        """
        Retourne l'historique complet des factures sous forme d'une liste de dictionnaires.
        Si le fichier est vide, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            if df.empty:
                return []
            df = df.sort_values('date', ascending=False)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de la lecture de l'historique : {str(e)}")
            return []

    def get_factures_client(self, code_client):
        """
        Retourne l'historique des factures pour un client spécifique sous forme d'une liste de dictionnaires.
        Si aucune facture n'est trouvée ou en cas d'erreur, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            df_client = df[df['code_client'] == code_client]
            if df_client.empty:
                return []
            df_client = df_client.sort_values('date', ascending=False)
            return df_client.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de la recherche : {str(e)}")
            return []

    def get_facture_detaillee(self, numero_facture):
        """
        Retourne une facture spécifique sous forme d'une liste de dictionnaires (une seule ligne ou vide).
        Si la facture n'est pas trouvée ou en cas d'erreur, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            facture = df[df['numero_facture'] == numero_facture]
            if facture.empty:
                return []
            return facture.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de l'affichage : {str(e)}")
            return []
        
#Fonction pour les calcules
    def calcul_remise(total_ht, remise_pourcent):
        #Calcule le montant de la remise
        return total_ht * (remise_pourcent / 100)

    def montant_ht_apres_remise(total_ht, remise_pourcent):
        #Calcule le montant HT après remise.
        return total_ht - calcul_remise(total_ht, remise_pourcent)

    def montant_tva(THT_remise, tva_pourcent=18):
        #Calcule le montant de la TVA sur le HT après remise.
        return THT_remise * (tva_pourcent / 100)

    def montant_ttc(THT_remise, tva_pourcent=18):
        #Calcule le montant TTC (HT après remise + TVA).
        return THT_remise + montant_tva(THT_remise, tva_pourcent)