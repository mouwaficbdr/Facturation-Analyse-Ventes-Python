import pandas as pd
from datetime import datetime
import os
import sys

class InvoiceManager:
    def __init__(self, data_folder="invoices_data"):
        """Initialize the invoice manager with a specific data folder"""
        # Create folder if it doesn't exist
        os.makedirs(data_folder, exist_ok=True)
        
        # Set the file path
        self.INVOICE_FILE = os.path.join(data_folder, "invoices_history.xlsx")
        self.initialize_file()
        
        # Menu dictionary
        self.menus = {
            'main': {
                '1': {'text': 'Add invoice', 'action': self.add_invoice_interface},
                '2': {'text': 'Show all invoices', 'action': self.show_all_invoices},
                '3': {'text': 'Search by client', 'action': self.search_by_client_interface},
                '4': {'text': 'Search by date', 'action': self.search_by_date_interface},
                '5': {'text': 'Exit', 'action': self.exit_program}
            }
        }

    def initialize_file(self):
        """Create the Excel file with required columns if it doesn't exist"""
        if not os.path.exists(self.INVOICE_FILE):
            columns = [
                "Invoice_number",
                "Date",
                "Client",
                "Product_code",
                "Products",
                "Quantity",
                "Unit_price",
                "Amount_HT",
                "VAT",
                "Amount_TTC"
            ]
            try:
                pd.DataFrame(columns=columns).to_excel(
                    self.INVOICE_FILE, 
                    index=False, 
                    engine='openpyxl'
                )
                print(f"File created successfully: {self.INVOICE_FILE}")
            except PermissionError:
                print(f"Error: Cannot create file. Permission denied for {self.INVOICE_FILE}")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error creating file: {str(e)}")
                sys.exit(1)

    def add_invoice(self, invoice_number, client, products_details):
        """
        Add a new invoice to the system
        :param invoice_number: Invoice number (str)
        :param client: Client name (str)
        :param products_details: List of dictionaries containing products
        """
        try:
            # Calculate amounts
            amount_ht = sum(p['quantity'] * p['unit_price'] for p in products_details)
            vat = amount_ht * 0.2  # VAT at 20%
            amount_ttc = amount_ht + vat

            # Prepare data
            new_invoice = {
                "Invoice_number": invoice_number,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Client": client,
                "Product_code": ";".join(str(p['code']) for p in products_details),
                "Products": ";".join(p['name'] for p in products_details),
                "Quantity": ";".join(str(p['quantity']) for p in products_details),
                "Unit_price": ";".join(f"{p['unit_price']:.2f}" for p in products_details),
                "Amount_HT": f"{amount_ht:.2f}",
                "VAT": f"{vat:.2f}",
                "Amount_TTC": f"{amount_ttc:.2f}"
            }

            # Read and update file
            df = pd.read_excel(self.INVOICE_FILE, engine='openpyxl')
            df = pd.concat([df, pd.DataFrame([new_invoice])], ignore_index=True)
            
            # Save with improved Excel formatting
            with pd.ExcelWriter(self.INVOICE_FILE, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                worksheet = writer.sheets['Sheet1']
                
                # Add auto-filters
                worksheet.auto_filter.ref = worksheet.dimensions
                
                # Adjust column width
                for column in worksheet.columns:
                    max_length = max(len(str(cell.value)) for cell in column)
                    worksheet.column_dimensions[column[0].column_letter].width = max_length + 2

            print(f"\nInvoice {invoice_number} added successfully for {client} (Total TTC: {amount_ttc:.2f}€)")

        except Exception as e:
            print(f"\nError adding invoice: {str(e)}")

    def show_all_invoices(self):
        """Display all invoices with improved formatting"""
        try:
            df = pd.read_excel(self.INVOICE_FILE, engine='openpyxl')
            
            if df.empty:
                print("\nNo invoices found.")
                return

            print("\n=== ALL INVOICES ===")
            
            # Sort by date descending
            df = df.sort_values('Date', ascending=False)
            
            # Improved formatting
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            pd.set_option('display.colheader_justify', 'center')
            
            print(df.to_string(index=False))
            print(f"\nTotal invoices: {len(df)}")
            print(f"Global amount TTC: {df['Amount_TTC'].astype(float).sum():.2f}€")

        except Exception as e:
            print(f"\nError reading invoices: {str(e)}")

    def search_by_client(self, client):
        """Display invoices for a specific client"""
        try:
            df = pd.read_excel(self.INVOICE_FILE, engine='openpyxl')
            client_invoices = df[df['Client'].str.lower() == client.lower()]
            
            if client_invoices.empty:
                print(f"\nNo invoices found for client: {client}")
                return

            print(f"\n=== INVOICES FOR {client.upper()} ===")
            
            # Sort and format
            client_invoices = client_invoices.sort_values('Date', ascending=False)
            print(client_invoices[['Invoice_number', 'Date', 'Amount_TTC']].to_string(index=False))
            
            print(f"\nTotal invoices: {len(client_invoices)}")
            print(f"Total amount: {client_invoices['Amount_TTC'].astype(float).sum():.2f}€")

        except Exception as e:
            print(f"\nError during search: {str(e)}")

    def search_by_date(self, date):
        """Display invoices for a specific date"""
        try:
            df = pd.read_excel(self.INVOICE_FILE, engine='openpyxl')
            df['Date_only'] = pd.to_datetime(df['Date']).dt.date
            search_date = datetime.strptime(date, "%Y-%m-%d").date()
            
            date_invoices = df[df['Date_only'] == search_date]
            
            if date_invoices.empty:
                print(f"\nNo invoices found for date: {date}")
                return

            print(f"\n=== INVOICES FOR {date} ===")
            print(date_invoices.to_string(index=False))
            
            print(f"\nTotal invoices: {len(date_invoices)}")
            print(f"Total amount: {date_invoices['Amount_TTC'].astype(float).sum():.2f}€")

        except ValueError:
            print("\nInvalid date format. Use YYYY-MM-DD.")
        except Exception as e:
            print(f"\nError during search: {str(e)}")

    # User interfaces
    def add_invoice_interface(self):
        print("\n--- NEW INVOICE ---")
        invoice_number = input("Invoice number: ").strip()
        client = input("Client: ").strip()
        
        products = []
        while True:
            print("\nAdd a product (leave blank to finish):")
            code = input("Product code: ").strip()
            if not code:
                break
                
            name = input("Product name: ").strip()
            try:
                quantity = int(input("Quantity: ").strip())
                price = float(input("Unit price (excl. tax): ").strip())
            except ValueError:
                print("Error: quantity and price must be numbers")
                continue
                
            products.append({
                'code': code,
                'name': name,
                'quantity': quantity,
                'unit_price': price
            })
        
        if not products:
            print("Cancelled: no products added")
            return
            
        self.add_invoice(invoice_number, client, products)

    def search_by_client_interface(self):
        client = input("\nEnter client name: ").strip()
        if client:
            self.search_by_client(client)
        else:
            print("Invalid client name")

    def search_by_date_interface(self):
        date = input("\nEnter date (YYYY-MM-DD): ").strip()
        if date:
            self.search_by_date(date)
        else:
            print("Invalid date")

    def exit_program(self):
        print("\nThank you for using the invoice management system. Goodbye!")
        sys.exit()

    def show_menu(self, menu_type):
        print("\n" + "="*50)
        print("INVOICE MANAGEMENT SYSTEM".center(50))
        print("="*50)
        
        menu = self.menus.get(menu_type, {})
        for key, item in menu.items():
            print(f"{key}. {item['text']}")
        
        print("="*50)

    def run(self):
        """Main application entry point"""
        while True:
            self.show_menu('main')
            choice = input("Your choice (1-5): ").strip()
            
            action = self.menus['main'].get(choice, {}).get('action')
            if action:
                action()
            else:
                print("\nInvalid choice. Please select an option between 1 and 5.")

if __name__ == "__main__":
    # Create with default folder
    manager = InvoiceManager()
    
    # Or specify custom folder:
    # manager = InvoiceManager(data_folder="my_invoices_folder")
    
    manager.run()