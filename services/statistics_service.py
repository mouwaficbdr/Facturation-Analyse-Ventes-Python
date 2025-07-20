import pandas as pd


class StatisticsService:
    def __init__(self, invoices_path, clients_path, products_path, discounts_path):
        self.invoices_path = invoices_path
        self.clients_path = clients_path
        self.products_path = products_path
        self.discounts_path = discounts_path

        self.df_invoices = self._load_excel(self.invoices_path)
        self.df_clients = self._load_excel(self.clients_path)
        self.df_products = self._load_excel(self.products_path)
        self.df_discounts = self._load_excel(self.discounts_path)

    def _load_excel(self, path):
        try:
            return pd.read_excel(path)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {path}: {e}")
            return pd.DataFrame()

    def total_revenue(self):
        return self.df_invoices['Amount_TTC'].sum()

    def total_clients(self):
        return len(self.df_clients)

    def total_products(self):
        return len(self.df_products)

    def total_discount_cards(self):
        return len(self.df_discounts)

    def best_selling_product(self):
        sales = self.df_invoices.groupby('Products')['Quantity'].sum()
        if sales.empty:
            return None, 0
        product = sales.idxmax()
        quantity = sales.max()
        return product, quantity

    def best_client(self):
        client_revenue = self.df_invoices.groupby('Client')['Amount_TTC'].sum()
        if client_revenue.empty:
            return None, 0
        client = client_revenue.idxmax()
        amount = client_revenue.max()
        return client, amount

    def sales_distribution_by_client(self):
        orders = self.df_invoices.groupby('Client')['Invoice_number'].nunique()
        revenue = self.df_invoices.groupby('Client')['Amount_TTC'].sum()
        result = []
        for client in orders.index:
            result.append({
                'Client': client,
                'Order_count': orders[client],
                'Revenue': revenue[client]
            })
        return result

    