import pandas as pd
from datetime import datetime
import os

class FactureManager:
    def __init__(self, data_folder="data"):
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

    def ajouter_facture(self, numero_facture,remise, client, produits):
        """
        Ajoute une facture à l'historique
        :param numero_facture: Numéro unique de facture
        :param client: Dictionnaire contenant les infos client
        :param produits: Liste de dictionnaires des produits
        """
        try:
            # Calcul des montants
            total_ht = sum(p['quantite'] * p['prix'] for p in produits)
            tht_remise = total_ht * (1 - remise/100)
            tva = tht_remise * 0.18
            total_ttc = tht_remise + tva

            # Préparation des données
            nouvelle_facture = {
                "numero_facture": numero_facture,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "code_client": client['code'],
                "nom_client": client['nom'],
                "produits": ";".join(p['code'] for p in produits),
                "quantites": ";".join(str(p['quantite']) for p in produits),
                "prix_unitaire": ";".join(f"{p['prix']:.2f}" for p in produits),
                "total_ht": f"{total_ht:.2f}",
                "remise": f"{remise}%",
                "tva": f"{tva:.2f}",
                "total_ttc": f"{total_ttc:.2f}"
            }

            # Mise à jour du fichier
            df = pd.read_excel(self.INVOICES_FILE)
            df = pd.concat([df, pd.DataFrame([nouvelle_facture])], ignore_index=True)
            df.to_excel(self.INVOICES_FILE, index=False)

            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture : {str(e)}")
            return False

    def _calculer_remise(self, code_client, montant):
        """Calcule la remise selon les règles métier"""
        # Implémentez ici votre logique de calcul de remise
        return 0  # Par défaut, pas de remise

    def afficher_historique_complet(self):
        """Affiche toutes les factures avec un formatage clair"""
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            
            if df.empty:
                print("\nAucune facture dans l'historique.")
                return

            print("\n=== HISTORIQUE COMPLET DES FACTURES ===")
            print(f"Nombre total de factures : {len(df)}")
            print(f"Chiffre d'affaires total : {df['total_ttc'].astype(float).sum():.2f}€\n")
            
            # Tri par date décroissante
            df = df.sort_values('date', ascending=False)
            
            # Formatage amélioré
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            
            print(df[['numero_facture', 'date', 'nom_client', 'total_ttc']].to_string(index=False))
            
        except Exception as e:
            print(f"\nErreur lors de la lecture de l'historique : {str(e)}")

    def afficher_factures_client(self, code_client):
        """Affiche l'historique des factures pour un client spécifique"""
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            df_client = df[df['code_client'] == code_client]
            
            if df_client.empty:
                print(f"\nAucune facture trouvée pour le client {code_client}.")
                return

            client_name = df_client.iloc[0]['nom_client']
            print(f"\n=== FACTURES POUR {client_name.upper()} ===")
            print(f"Nombre de factures : {len(df_client)}")
            print(f"Total dépensé : {df_client['total_ttc'].astype(float).sum():.2f}€\n")
            
            # Tri par date décroissante
            df_client = df_client.sort_values('date', ascending=False)
            
            # Affichage détaillé
            for _, facture in df_client.iterrows():
                print(f"Facture n°{facture['numero_facture']} - {facture['date']}")
                print(f"Montant TTC : {facture['total_ttc']}€")
                print("Produits :")
                
                # Détail des produits
                produits = facture['produits'].split(';')
                quantites = facture['quantites'].split(';')
                prix = facture['prix_unitaire'].split(';')
                
                for p, q, px in zip(produits, quantites, prix):
                    print(f"  - {p} : {q} x {px}€")
                
                print(f"Remise : {facture['remise']}")
                print("-" * 40)
                
        except Exception as e:
            print(f"\nErreur lors de la recherche : {str(e)}")

    def afficher_facture_detaillee(self, numero_facture):
        """Affiche une facture spécifique en détail"""
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            facture = df[df['numero_facture'] == numero_facture]
            
            if facture.empty:
                print(f"\nFacture {numero_facture} introuvable.")
                return

            facture = facture.iloc[0]
            print("\n" + "=" * 50)
            print(f"FACTURE N° {facture['numero_facture']}".center(50))
            print("=" * 50)
            print(f"Date : {facture['date']}")
            print(f"Client : {facture['nom_client']} (Code: {facture['code_client']})")
            print("-" * 50)
            print("DÉTAIL DES PRODUITS:")
            
            # Affichage du tableau des produits
            produits = facture['produits'].split(';')
            quantites = facture['quantites'].split(';')
            prix = facture['prix_unitaire'].split(';')
            
            
            for p, q, px in zip(produits, quantites, prix):
                total = float(q) * float(px)
                print(f"| {p:11} | {q:8} | {float(px):13.2f}€ | {total:8.2f}€ |")
            
            print("\n" + "-" * 50)
            print(f"Total HT: {facture['total_ht']}€")
            print(f"Remise: {facture['remise']}")
            print(f"TVA (18%): {facture['tva']}€")
            print(f"Total TTC: {facture['total_ttc']}€")
            print("=" * 50 + "\n")
            
        except Exception as e:
            print(f"\nErreur lors de l'affichage : {str(e)}")