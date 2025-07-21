import pandas as pd

def get_all_discounts(path='data/CartesReduction.xlsx'):
    try:
        df = pd.read_excel(path)
    except Exception:
        return []
    discounts = []
    for _, row in df.iterrows():
        discounts.append({
            'id': row.get('numero_carte'),
            'numero_client': row.get('code_client'),
            'code_client': row.get('code_client'),
            'taux_reduction': row.get('taux_reduction')
        })
    return discounts
