import pandas as pd
from models.client import Client

# Variables globales pour les seuils et taux de réduction
DISCOUNT_THRESHOLDS = [
    {"amount": 50000, "discount": 0},
    {"amount": 100000, "discount": 10},
    {"amount": 200000, "discount": 15},
]


#Fonction pour générer une carte de réduction pour la dernière facture
#Vous devrez l'appeler seulement après la génération de la facture et l'enregistrement de la facture dans l'historique des factures sinon dohi !!!
#Dans ces conditions, elle n'aura besoin qu'on lui passe aucun paramètre
def generate_discount_card_for_last_invoice(discounts_path='data/CartesReduction.xlsx', invoices_path='exports/historique_factures.xlsx'):
    try:
        df_invoices = pd.read_excel(invoices_path)
    except Exception:
        return
    if df_invoices.empty:
        return
    invoice_row = df_invoices.iloc[-1]
    client = invoice_row['Client']
    amount = invoice_row['Amount_HT']

    try:
        df_discounts = pd.read_excel(discounts_path)
    except Exception:
        df_discounts = pd.DataFrame(columns=['numero_carte', 'code_client', 'taux_reduction'])

    if client in set(df_discounts['code_client']):
        return

    df_client_invoices = df_invoices[df_invoices['Client'] == client].sort_values('Date')
    if len(df_client_invoices) == 1:
        return

    # Détermination du taux de réduction selon le montant
    discount = None
    for threshold in DISCOUNT_THRESHOLDS:
        if amount < threshold["amount"]:
            discount = threshold["discount"]
            break
    if discount is None:
        discount = DISCOUNT_THRESHOLDS[-1]["discount"]
    if amount < DISCOUNT_THRESHOLDS[0]["amount"]:
        return

    card_number = f"{client}-001"
    new_card = {
        'numero_carte': card_number,
        'code_client': client,
        'taux_reduction': discount
    }
    df_discounts = pd.concat([df_discounts, pd.DataFrame([new_card])], ignore_index=True)
    df_discounts.to_excel(discounts_path, index=False) 
