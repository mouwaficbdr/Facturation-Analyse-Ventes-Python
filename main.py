import pandas as pd
from datetime import datetime
import os

# Nom du fichier de sauvegarde (format Excel moderne)
FICHIER_FACTURES = "historique_factures.xlsx"

# Initialisation du fichier Excel s'il n'existe pas
def initialiser_fichier():
    if not os.path.exists(FICHIER_FACTURES):
        df = pd.DataFrame(columns=[
            "Numero_facture",
            "Date",
            "Client",
            "code Produit",
            "Produits",
            "Prix unitaire",
            "Montant Total(TTC)"
        ])
        df.to_excel(FICHIER_FACTURES, index=False)

# Ajouter une nouvelle facture
def ajouter_facture(numero, client, code_produit, produits,prix_unitaire, montantTotal):
    initialiser_fichier()
    nouvelle_facture = {
        "Numero_facture": numero,
        "Date": datetime.now().strftime("%Y-%m-%d"), 
        "Client": client,
        "code Produit": code_produit,
        "Produits": produits,
        "Prix unitaire": prix_unitaire,
        "Montant Total (TTC)": montantTotal
    }
    df = pd.read_excel(FICHIER_FACTURES) 
    df = pd.concat([df, pd.DataFrame([nouvelle_facture])], ignore_index=True)
    df.to_excel(FICHIER_FACTURES, index=False)  # Écrire dans le fichier Excel

# Afficher l'historique complet
def afficher_historique_complet():
    df = pd.read_excel(FICHIER_FACTURES)
    if df.empty:
        print("Aucune facture enregistrée.")
    else:
        print("=== Historique complet des factures ===")
        print(df.to_string(index=False))

# Afficher les factures d'un client
def afficher_historique_client(client):
    df = pd.read_excel(FICHIER_FACTURES)
    df_client = df[df["Client"] == client]
    if df_client.empty:
        print(f"Aucune facture trouvée pour le client {client}.")
    else:
        print(f"=== Historique des factures pour {client} ===")
        print(df_client.to_string(index=False))

#Afficher les factures a une date donnée
def afficher_historique_date_client(date):
    df = pd.read_excel(FICHIER_FACTURES)
    df_date_client = df[df["Date"] == date]
    if df_date_client.empty:
        print(f"Aucune fature trouvée pour cette date {date}.")
    else:
        print(f"=== Historique des factures pour cette {date} ===")
        print(df_client.to_string(index=False))

#Sortie de l'application
def exit():
        os.system("exit")
        

# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Ajout de factures (exemple)
#     ajouter_facture("FAC-008", "Client C", 1000, "Produit 8")

#     # Affichage
#     afficher_historique_client("Client C")
