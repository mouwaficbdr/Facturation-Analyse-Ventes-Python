import pandas as pd

def generate_discount_card_for_invoice(invoice_row, discounts_path='data/CartesReduction.xlsx', invoices_path='exports/historique_factures.xlsx'):
    client = invoice_row['Client']
    amount = invoice_row['Amount_TTC']

    try:
        df_discounts = pd.read_excel(discounts_path)
    except Exception:
        df_discounts = pd.DataFrame(columns=['numero_carte', 'code_client', 'taux_reduction'])

    if client in set(df_discounts['code_client']):
        return

    try:
        df_invoices = pd.read_excel(invoices_path)
    except Exception:
        return
    df_client_invoices = df_invoices[df_invoices['Client'] == client].sort_values('Date')

    if len(df_client_invoices) == 1:
        return

    if amount < 50000:
        return
    elif amount < 100000:
        discount = 5
    elif amount < 200000:
        discount = 10
    else:
        discount = 15

    card_number = f"{client}-001"
    new_card = {
        'numero_carte': card_number,
        'code_client': client,
        'taux_reduction': discount
    }
    df_discounts = pd.concat([df_discounts, pd.DataFrame([new_card])], ignore_index=True)
    df_discounts.to_excel(discounts_path, index=False) 