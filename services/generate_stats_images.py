import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Style général
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

# Charger les données
invoices_path = 'exports/historique_factures.xlsx'
df = pd.read_excel(invoices_path)

# S'assurer que les dates sont bien au format datetime
if not pd.api.types.is_datetime64_any_dtype(df['Date']):
    df['Date'] = pd.to_datetime(df['Date'])

# Créer le dossier exports/stats s'il n'existe pas
stats_dir = 'exports/stats'
os.makedirs(stats_dir, exist_ok=True)

# 1. Chiffre d'affaires par mois
plt.figure(figsize=(10, 5))
df['Month'] = df['Date'].dt.to_period('M')
ca_by_month = df.groupby('Month')['Amount_TTC'].sum()
ax = ca_by_month.plot(kind='bar', color=sns.color_palette('Blues', n_colors=len(ca_by_month)), title="Chiffre d'affaires par mois")
ax.set_ylabel('CA (FCFA)')
ax.set_xlabel('Mois')
ax.set_xticklabels([str(m) for m in ca_by_month.index], rotation=45, ha='right')
for i, v in enumerate(ca_by_month.values):
    ax.text(i, v + max(ca_by_month.values)*0.01, f'{int(v):,}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(stats_dir, 'ca_par_mois.png'))
plt.close()

# 2. Top 5 produits les plus vendus
plt.figure(figsize=(10, 5))
top_products = df.groupby('Products')['Quantity'].sum().sort_values(ascending=False).head(5)
ax = sns.barplot(x=top_products.index, y=top_products.values, palette='viridis')
ax.set_title('Top 5 produits les plus vendus')
ax.set_ylabel('Quantité vendue')
ax.set_xlabel('Produit')
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
for i, v in enumerate(top_products.values):
    ax.text(i, v + max(top_products.values)*0.01, f'{int(v):,}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(stats_dir, 'top_5_produits.png'))
plt.close()

# 3. Répartition du chiffre d'affaires par client (camembert)
plt.figure(figsize=(8, 8))
ca_by_client = df.groupby('Client')['Amount_TTC'].sum().sort_values(ascending=False)
# On limite à 8 clients pour la lisibilité, les autres sont regroupés
if len(ca_by_client) > 8:
    ca_by_client = ca_by_client.head(7).append(pd.Series({'Autres': ca_by_client[7:].sum()}))
colors = sns.color_palette('pastel', n_colors=len(ca_by_client))
plt.pie(ca_by_client, labels=ca_by_client.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'white'})
plt.title('Répartition du CA par client')
plt.tight_layout()
plt.savefig(os.path.join(stats_dir, 'ca_par_client.png'))
plt.close()

# 4. Nombre de commandes par client
plt.figure(figsize=(12, 5))
orders_by_client = df.groupby('Client')['Invoice_number'].nunique().sort_values(ascending=False)
ax = sns.barplot(x=orders_by_client.index, y=orders_by_client.values, palette='magma')
ax.set_title('Nombre de commandes par client')
ax.set_ylabel('Nombre de commandes')
ax.set_xlabel('Client')
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
for i, v in enumerate(orders_by_client.values):
    ax.text(i, v + max(orders_by_client.values)*0.01, f'{int(v):,}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(stats_dir, 'commandes_par_client.png'))
plt.close()
