from multiprocessing.connection import Client
import tkinter as tk
from tkinter.font import BOLD
from produits_model import Products
from tkinter import messagebox
from clients_model import Client
from statistics_service import StatisticsService

statis = StatisticsService(
    'exports/historique_factures .xlsx',
    'data/Clients.xlsx',
    'data/Produits.xlsx',
    'data/CartesReduction.xlsx'
)


class FacturationApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Application de Facturation")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.resizable(False, False)

        self.bodyFrame = tk.Frame(self.root, bg="#F5F5F5", padx=15, pady=15)
        self.root.configure(bg='#EEEEEE')

        self.create_header()
        self.create_body()

        self.root.mainloop()

    def create_header(self):
        header = tk.Frame(self.root, bg="white", padx=10)
        header.pack(fill="x")
        label = tk.Label(header, text="Application de facturation", font=("Roboto", 18, "bold"), bg="white", foreground='black')
        label.pack(side='left')
        quit_btn = tk.Button(header, text="Quitter", fg="white", bg="#BF3F3F",
                             font=("Roboto", 11, "bold"), relief="solid", borderwidth=1, command=self.root.quit)
        quit_btn.pack(side="right", padx=15, pady=15)

    def create_body(self):
        self.bodyFrame.pack(fill="both", expand=True)

        self.bodyFrame.columnconfigure(0, weight=0)
        self.bodyFrame.columnconfigure(1, weight=1)
        self.bodyFrame.rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_board_container()
        self.show_section(self.boardMotion)  

    def create_sidebar(self):
        sidebar = tk.Frame(self.bodyFrame, width=230, background="#F5F5F5")
        sidebar.grid(row=0, column=0, sticky="ns")

        for i in range(5):
            sidebar.columnconfigure(i, weight=2)

        self.menu_items = {
            'Tableau de bord': self.boardMotion,
            'Consulter un fichier': self.fileMotion,
            'Générer une facture': self.factureMotion,
            'Ajouter un produit': self.productMotion,
            'historique' : self.historyMotion,
            'Statisques': self.StatisquesMotion,
        }

        self.sidebar_buttons = {}

        for label, function in self.menu_items.items():
            button = tk.Button(sidebar, text=label, anchor="center", padx=10, pady=10,
                               background='black', foreground='white', justify="center", relief='flat', width=25)
            button.config(command=lambda f=function, b=button: self.on_click(f, b))
            button.pack(fill="x", pady=1)
            self.sidebar_buttons[button] = function

    def create_board_container(self):
        container = tk.Frame(self.bodyFrame)
        container.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(container, bg="#F5F5F5")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        # le frame contenant les éléments à implémenter
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="#F5F5F5",
            padx=10,
            pady=10,
            highlightthickness=0,  # No highlight border
            bd=0                   # No border
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=750)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollable_frame.bind("<Enter>", lambda e: self._bind_to_mousewheel(self.canvas))
        self.scrollable_frame.bind("<Leave>", lambda e: self._unbind_from_mousewheel(self.canvas))

    def clear_scrollable_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_section(self, section_function):
        self.clear_scrollable_frame()
        section_function(self.scrollable_frame)

    # Fonctions à implémenter dans la scroll_frame
    def boardMotion(self, parent):
        frame1 = tk.Frame(parent,background="#F5F5F5")
        frame1.pack(fill='x')
        tk.Label(frame1,text='Tableau de bord', font=('Roboto', 20, 'bold'),
                 background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        frame2 = tk.Frame(parent,background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2,text='Bienvenue dans votre application de facturation', font=('Roboto', 12, 'bold'),
                 background='#F5F5F5', foreground='gray').pack(side='left')
        
        frame3 = tk.Frame(parent,background="#F5F5F5")
        frame3.pack(fill='x',padx=20,pady=20)

        for i in range(4):
            frame3.columnconfigure(i,weight=1)
        frame3.rowconfigure(0,weight=1)

        # Les petits frames de statisques
        underframe = tk.Frame(frame3,background='#F5F5F5',bd=1,relief='solid',width=50,padx=15,pady=15)

        underframe.rowconfigure(0,weight=1)
        underframe.rowconfigure(1,weight=1)

        stats = {
            'Total clients' :statis.total_clients(),
            'Produits' : statis.total_products,
            'Cartes de réduction' : statis.total_discount_cards ,
            'CA Total' : statis.total_revenue 
        }

        for col_index, (label, value) in enumerate(stats.items()):
            underframe = tk.Frame(frame3, background='white', bd=1, relief='solid', padx=15, pady=15)
            underframe.grid(column=col_index, row=0, sticky='nsew', padx=10)

            # Stat title
            title_label = tk.Label(underframe, text=label, bg='white', font=('Roboto', 10), fg='#333')
            title_label.pack(anchor='center', pady=(10, 0))
        
            # Stat number
            number_label = tk.Label(underframe, text=value, bg='white', font=('Roboto', 16, 'bold'))
            number_label.pack(anchor='ne')

    def historyMotion(self,parent):
        frame1 = tk.Frame(parent, background="#F5F5F5")
        frame1.pack(fill='both')
        tk.Label(frame1, text='Historiques des ventes', font=('Roboto', 20, 'bold'),
                 background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        frame2 = tk.Frame(parent, background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2, text="Observez ici l'historique des ventes effectuées", font=('Roboto', 12, 'bold'),
                 background='#F5F5F5', foreground='gray').pack(side='left')

        # Conteneur principal blanc
        frame3 = tk.Frame(parent, bg="white", padx=20, pady=20)
        frame3.pack(fill='both', pady=20)

        # En-têtes de colonnes
        historyMenu = [
            "numero_facture", "date", "code_client", "nom_client", "produits",
            "quantites", "prix_unitaire", "total_ht", "remise", "tva", "total_ttc"
        ]
        headers = [
            "N° Facture", "Date", "Code Client", "Nom Client", "Produits",
            "Quantités", "Prix Unitaire", "Total HT", "Remise", "TVA", "Total TTC"
        ]

        # Exemple de données
        historyStats = [
            {
                'numero_facture': "POO123",
                'date': "2025-07-21",
                'code_client': "C001",
                'nom_client': "Big mum",
                'produits': 'gâteau',
                'quantites': 5,
                'prix_unitaire': 500,
                'total_ht': 2500,
                'remise': "0%",
                'tva': "18%",
                'total_ttc': 2950
            },
            {
                'numero_facture': "POO124",
                'date': "2025-07-20",
                'code_client': "C002",
                'nom_client': "Luffy",
                'produits': 'bonbon',
                'quantites': 10,
                'prix_unitaire': 100,
                'total_ht': 1000,
                'remise': "5%",
                'tva': "18%",
                'total_ttc': 1113
            }
        ]

        #line
        table = tk.Frame(frame3, bg='white')
        table.pack(fill='both', expand=True)

        # Affichage des en-têtes
        for col, header in enumerate(headers):
            tk.Label(table, text=header, font=('Roboto', 10, 'bold'),
                     bg='white', fg='gray', padx=8, pady=6, anchor='w').grid(row=0, column=col, sticky='ew')

        # Ligne de séparation
        tk.Frame(table, height=1, bg='#ddd').grid(row=1, column=0, columnspan=len(headers), sticky='ew', pady=(2, 5))

        # Affichage des lignes de données
        for row_index, row in enumerate(historyStats, start=2):
            for col_index, key in enumerate(historyMenu):
                value = row.get(key, "")
                tk.Label(table, text=value, width=150, font=('Roboto', 10),
                         bg='white', fg='black', padx=8, pady=4, anchor='w').grid(row=row_index, column=col_index, sticky='ew')

        # Ajustement des colonnes pour un affichage responsive
        for col in range(len(headers)):
            table.grid_columnconfigure(col, weight=1)

    def fileMotion(self, parent):

        color_set={
            'buttonsbg':'#c1c1c1'
        }
        frame1=tk.Frame(parent, background='#F5F5F5')
        frame1.pack(fill='x')
        tk.Label(frame1, text='Consultation des données', font=('Roboto', 20, 'bold'),
        background='#F5F5F5', foreground='black').pack(side='left')

        frame2=tk.Frame(parent, background='#F5F5F5')
        frame2.pack(fill='x')
        tk.Label(frame2, text='Consultez vos clients, produits et cartes de réductions.', font=('Roboto', 10),
        foreground='gray',bg='#F5F5F5').pack(side='left')

        frame3 = tk.Frame(parent, pady=20,bg='#F5F5F5')
        frame3.pack(fill="x")

        frame4 = tk.Frame(parent, pady=40)

        for i in range(3):
            frame3.grid_columnconfigure(i, weight=1)
            

        btnManager=[
            {
                'content':'Clients',
                'function': lambda: self.renderFileContent(frame4, 'Liste des clients', ['code_client', 'nom', 'contact', 'IFU'],Client().getallClients()) 
            },
            {
                'content':'Produits',
                'function': lambda: self.renderFileContent(frame4, 'Liste des produits', ['code_produit', 'libelle', 'prix_unitaire'], Products().getAllProducts())
            },
            {
                'content':'Cartes de réductions',
                'function': lambda: self.renderFileContent(frame4, 'Liste des cartes de réductions', ['Code_client', 'Nom', 'Contact', 'IFU'], [])
            }
        ]

        for i in range(3):
            btn = tk.Button(frame3, text=btnManager[i]['content'], bg=color_set['buttonsbg'], fg='black', font=('Roboto', 12), relief='raised', pady=10, padx=5, cursor='hand2', command=btnManager[i]['function'] )
            btn.grid(row=0, column=i, sticky="nsew")

        
        frame4.pack( fill='x')

        tk.Label(frame4, text="Cliquez sur un button pour voir le contenu du fichier correspondant.", font=('Roboto', 15, 'bold'),
        foreground='black').pack(fill='x')
        



    def renderFileContent(self, starterFrame, headerMessage, header,  content):

        for frame in starterFrame.winfo_children():
            frame.destroy();
        
        starterFrame.pack(fill='x')
        starterFrame.configure(padx=5,pady=5)

        if not isinstance(header, list):      
            return 'Un tableau avec les clés du fichier est attendu.'

        if not isinstance(content, list) or len(content) == 0 :
            tk.Label(starterFrame, text='Aucun contenu.', foreground='gray', pady=5, font=('Roboto', 20, 'bold')).pack(anchor='center')
            return;

        headerZone=tk.Frame(starterFrame, pady=10)
        headerZone.pack(fill='x', anchor='w')

        tk.Label(headerZone, text=headerMessage, font=('Roboto', 20 , 'bold'), foreground='black', anchor='w', justify='left').pack(fill='x')
        headerZone=tk.Frame(starterFrame, pady=10)
        headerZone.pack(fill='x', anchor='w')

        # tk.Label(headerZone, text=headerMessage, font=('Roboto', 20 , 'bold'), foreground='black', pady=10, anchor='w', justify='left').pack(fill='x')

        frame=tk.Frame(starterFrame,pady=10,padx=10)
        frame.pack(fill='x', anchor='w',padx=20,pady=20)

        for i in range(len(header)):
            frame.grid_columnconfigure(i, weight=1)
            tk.Label(frame, text=header[i], foreground='gray', pady=10, font=('Roboto', 12)).grid(row=0, column=i, sticky='nsew')
            tk.Label(frame, text=header[i], foreground='gray', pady=10, font=('Roboto', 12)).grid(row=0, column=i, sticky='nsew')

        for i in range(len(content)):
            for j in range(len(header)):
                tk.Label(frame, text=content[i][header[j]], foreground='black', pady=5, font=('Roboto', 15)).grid(row=i+1, column=j, sticky='nsew')

    def factureMotion(self, parent):
        # Variables pour gérer l'état des radio buttons et des champs
        if not hasattr(self, 'client_type_var'):
            self.client_type_var = tk.StringVar(value="nouveau")
    
        # Header
        frame1 = tk.Frame(parent, background="#F5F5F5")
        frame1.pack(fill='x')
        tk.Label(frame1, text='Générer une facture', font=('Roboto', 20, 'bold'),
                background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        
        frame2 = tk.Frame(parent, background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2, text='Créez une nouvelle facture pour vos clients', font=('Roboto', 12, 'bold'),
                background='#F5F5F5', foreground='gray').pack(side='left')
        
        # Container principal
        main_container = tk.Frame(parent, background="#F5F5F5")
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configuration des colonnes
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=0)
        
        # Colonne gauche - Formulaire
        left_column = tk.Frame(main_container, background="#F5F5F5")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Colonne droite - Résumé
        right_column = tk.Frame(main_container, background="white", padx=20, pady=20, 
                            highlightbackground="#CCC", highlightthickness=1)
        right_column.grid(row=0, column=1, sticky="ns", padx=(20, 0))
        
        # === SECTION TYPE DE CLIENT ===
        type_client_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                    highlightbackground="#CCC", highlightthickness=1)
        type_client_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(type_client_frame, text="Type de client", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
        
        # Radio buttons
        radio_frame = tk.Frame(type_client_frame, bg="white")
        radio_frame.pack(anchor="w")
        
        client_existant_radio = tk.Radiobutton(radio_frame, text="Client existant", 
                                            variable=self.client_type_var, value="existant",
                                            bg="white", font=("Roboto", 11),
                                            command=lambda: self.update_client_form(parent))
        client_existant_radio.pack(anchor="w", pady=2)
        
        nouveau_client_radio = tk.Radiobutton(radio_frame, text="Nouveau client", 
                                            variable=self.client_type_var, value="nouveau",
                                            bg="white", font=("Roboto", 11),
                                            command=lambda: self.update_client_form(parent))
        nouveau_client_radio.pack(anchor="w", pady=2)
        
        # === SECTION INFORMATIONS CLIENT ===
        self.client_info_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                        highlightbackground="#CCC", highlightthickness=1)
        self.client_info_frame.pack(fill="x", pady=(0, 20))
        
        # Cette section sera mise à jour selon le type de client sélectionné
        self.create_client_form()
        
        # === SECTION PRODUITS ===
        produits_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                highlightbackground="#CCC", highlightthickness=1)
        produits_frame.pack(fill="both", expand=True)
        
        tk.Label(produits_frame, text="Produits sélectionnés", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 5))
        
        tk.Label(produits_frame, text="Ajoutez des produits à votre facture", font=("Roboto", 10), 
                bg="white", fg="gray").pack(anchor="w", pady=(0, 15))
        
        # Table des produits
        table_frame = tk.Frame(produits_frame, bg="white")
        table_frame.pack(fill="both", expand=True)
        
        # Headers
        headers = ["Code\nProduit", "Libellé", "Quantité", "Prix", "Total", ""]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Roboto', 9, 'bold'),
                    bg='white', fg='gray', padx=10, anchor='w').grid(row=0, column=col, sticky='ew', pady=5)
        
        # Ligne de séparation
        tk.Frame(table_frame, height=1, bg='#ddd').grid(row=1, column=0, columnspan=6, sticky='ew', pady=2)
        
        # Exemple de produit
        tk.Label(table_frame, text="P001", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=0, sticky='ew', pady=8)
        tk.Label(table_frame, text="Ordinateur\nportable", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=1, sticky='ew', pady=8)
        tk.Label(table_frame, text="1", font=('Roboto', 10), bg='white', 
                padx=10, anchor='center').grid(row=2, column=2, sticky='ew', pady=8)
        tk.Label(table_frame, text="€800", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=3, sticky='ew', pady=8)
        tk.Label(table_frame, text="€800", font=('Roboto', 10, 'bold'), bg='white', 
                padx=10, anchor='w').grid(row=2, column=4, sticky='ew', pady=8)
        
        # Bouton supprimer
        delete_btn = tk.Button(table_frame, text="🗑", bg='white', fg='red', 
                            font=('Roboto', 12), relief='flat', cursor='hand2')
        delete_btn.grid(row=2, column=5, sticky='e', padx=10, pady=8)
        
        # Bouton ajouter ligne produit
        add_product_btn = tk.Button(produits_frame, text="+ Ajouter ligne produit", 
                                bg='#f8f9fa', fg='black', font=('Roboto', 10), 
                                relief='solid', borderwidth=1, cursor='hand2', pady=10)
        add_product_btn.pack(fill='x', pady=(15, 0))
        
        # === RÉSUMÉ DE LA FACTURE (Colonne droite) ===
        tk.Label(right_column, text="Résumé de la facture", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 20))
        
        # Détails financiers
        details = [
            ("Total HT:", "€800.00"),
            ("Remise appliquée:", "-€40.00", "green"),
            ("TVA (18%):", "€136.80"),
            ("Total TTC:", "€896.80", "bold")
        ]
        
        for item in details:
            detail_frame = tk.Frame(right_column, bg="white")
            detail_frame.pack(fill="x", pady=5)
            
            label = item[0]
            value = item[1]
            style = item[2] if len(item) > 2 else "normal"
            
            tk.Label(detail_frame, text=label, font=("Roboto", 11), bg="white", 
                    anchor="w").pack(side="left")
            
            if style == "green":
                tk.Label(detail_frame, text=value, font=("Roboto", 11), bg="white", 
                        fg="green", anchor="e").pack(side="right")
            elif style == "bold":
                tk.Label(detail_frame, text=value, font=("Roboto", 14, "bold"), bg="white", 
                        anchor="e").pack(side="right")
            else:
                tk.Label(detail_frame, text=value, font=("Roboto", 11), bg="white", 
                        anchor="e").pack(side="right")
        
        # Bouton générer PDF
        generate_btn = tk.Button(right_column, text="📄 Générer PDF", bg="black", fg="white",
                                font=("Roboto", 11, "bold"), padx=20, pady=15, 
                                relief="flat", cursor="hand2")
        generate_btn.pack(fill='x', pady=(30, 0))

    def create_client_form(self):
        """Crée le formulaire client selon le type sélectionné"""
        # Nettoie le frame
        for widget in self.client_info_frame.winfo_children():
            widget.destroy()
        
        if self.client_type_var.get() == "nouveau":
            # Formulaire nouveau client
            tk.Label(self.client_info_frame, text="Informations du nouveau client", 
                    font=("Roboto", 16, "bold"), bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
            
            # Ligne avec Nom et Contact
            info_row = tk.Frame(self.client_info_frame, bg="white")
            info_row.pack(fill="x", pady=(0, 15))
            info_row.columnconfigure(0, weight=1)
            info_row.columnconfigure(1, weight=1)
            
            # Nom
            nom_frame = tk.Frame(info_row, bg="white")
            nom_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
            tk.Label(nom_frame, text="Nom", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            nom_entry = tk.Entry(nom_frame, font=("Roboto", 10), relief="solid", bd=1)
            nom_entry.pack(fill="x", pady=(5, 0))
            nom_entry.insert(0, "Nom du client")
            nom_entry.config(fg="gray")
            
            # Contact
            contact_frame = tk.Frame(info_row, bg="white")
            contact_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
            tk.Label(contact_frame, text="Contact", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            contact_entry = tk.Entry(contact_frame, font=("Roboto", 10), relief="solid", bd=1)
            contact_entry.pack(fill="x", pady=(5, 0))
            contact_entry.insert(0, "Numéro de téléphone")
            contact_entry.config(fg="gray")
            
            # IFU
            ifu_frame = tk.Frame(self.client_info_frame, bg="white")
            ifu_frame.pack(fill="x", pady=(0, 10))
            tk.Label(ifu_frame, text="IFU", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            ifu_entry = tk.Entry(ifu_frame, font=("Roboto", 10), relief="solid", bd=1)
            ifu_entry.pack(fill="x", pady=(5, 0))
            ifu_entry.insert(0, "Numéro IFU")
            ifu_entry.config(fg="gray")
            
        else:
            # Sélection client existant
            tk.Label(self.client_info_frame, text="Sélectionner un client existant", 
                    font=("Roboto", 16, "bold"), bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
            
            # Liste déroulante des clients
            clients_frame = tk.Frame(self.client_info_frame, bg="white")
            clients_frame.pack(fill="x")
            
            tk.Label(clients_frame, text="Client", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            
            # Simule une liste déroulante (combobox)
            client_var = tk.StringVar(value="Sélectionner un client...")
            client_menu = tk.OptionMenu(clients_frame, client_var, 
                                    "Entreprise ABC", "Société XYZ", "Sarl Martin")
            client_menu.config(font=("Roboto", 10), relief="solid", bd=1, bg="white")
            client_menu.pack(fill="x", pady=(5, 0))

    def update_client_form(self, parent):
        """Met à jour le formulaire client quand le type change"""
        self.create_client_form()
    
    def factureMotion(self, parent):
        # Variables pour gérer l'état des radio buttons et des champs
        if not hasattr(self, 'client_type_var'):
            self.client_type_var = tk.StringVar(value="nouveau")
        
        # Header
        frame1 = tk.Frame(parent, background="#F5F5F5")
        frame1.pack(fill='x')
        tk.Label(frame1, text='Générer une facture', font=('Roboto', 20, 'bold'),
                background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        
        frame2 = tk.Frame(parent, background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2, text='Créez une nouvelle facture pour vos clients', font=('Roboto', 12, 'bold'),
                background='#F5F5F5', foreground='gray').pack(side='left')
        
        # Container principal
        main_container = tk.Frame(parent, background="#F5F5F5")
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configuration des colonnes
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=0)
        
        # Colonne gauche - Formulaire
        left_column = tk.Frame(main_container, background="#F5F5F5")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Colonne droite - Résumé
        right_column = tk.Frame(main_container, background="white", padx=20, pady=20, 
                            highlightbackground="#CCC", highlightthickness=1)
        right_column.grid(row=0, column=1, sticky="ns", padx=(20, 0))
        
        # SECTION TYPE DE CLIENT 
        type_client_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                    highlightbackground="#CCC", highlightthickness=1)
        type_client_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(type_client_frame, text="Type de client", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
        
        # Radio buttons
        radio_frame = tk.Frame(type_client_frame, bg="white")
        radio_frame.pack(anchor="w")
        
        client_existant_radio = tk.Radiobutton(radio_frame, text="Client existant", 
                                            variable=self.client_type_var, value="existant",
                                            bg="white", font=("Roboto", 11),
                                            command=lambda: self.update_client_form(parent))
        client_existant_radio.pack(anchor="w", pady=2)
        
        nouveau_client_radio = tk.Radiobutton(radio_frame, text="Nouveau client", 
                                            variable=self.client_type_var, value="nouveau",
                                            bg="white", font=("Roboto", 11),
                                            command=lambda: self.update_client_form(parent))
        nouveau_client_radio.pack(anchor="w", pady=2)
        
        # === SECTION INFORMATIONS CLIENT ===
        self.client_info_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                        highlightbackground="#CCC", highlightthickness=1)
        self.client_info_frame.pack(fill="x", pady=(0, 20))
        
        # Cette section sera mise à jour selon le type de client sélectionné
        self.create_client_form()
        
        # === SECTION PRODUITS ===
        produits_frame = tk.Frame(left_column, bg="white", padx=20, pady=20, 
                                highlightbackground="#CCC", highlightthickness=1)
        produits_frame.pack(fill="both", expand=True)
        
        tk.Label(produits_frame, text="Produits sélectionnés", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 5))
        
        tk.Label(produits_frame, text="Ajoutez des produits à votre facture", font=("Roboto", 10), 
                bg="white", fg="gray").pack(anchor="w", pady=(0, 15))
        
        # Table des produits
        table_frame = tk.Frame(produits_frame, bg="white")
        table_frame.pack(fill="both", expand=True)
        
        # Headers
        headers = ["Code\nProduit", "Libellé", "Quantité", "Prix", "Total", ""]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Roboto', 9, 'bold'),
                    bg='white', fg='gray', padx=10, anchor='w').grid(row=0, column=col, sticky='ew', pady=5)
        
        # Ligne de séparation
        tk.Frame(table_frame, height=1, bg='#ddd').grid(row=1, column=0, columnspan=6, sticky='ew', pady=2)
        
        # Exemple de produit
        tk.Label(table_frame, text="P001", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=0, sticky='ew', pady=8)
        tk.Label(table_frame, text="Ordinateur\nportable", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=1, sticky='ew', pady=8)
        tk.Label(table_frame, text="1", font=('Roboto', 10), bg='white', 
                padx=10, anchor='center').grid(row=2, column=2, sticky='ew', pady=8)
        tk.Label(table_frame, text="€800", font=('Roboto', 10), bg='white', 
                padx=10, anchor='w').grid(row=2, column=3, sticky='ew', pady=8)
        tk.Label(table_frame, text="€800", font=('Roboto', 10, 'bold'), bg='white', 
                padx=10, anchor='w').grid(row=2, column=4, sticky='ew', pady=8)
        
        # Bouton supprimer
        delete_btn = tk.Button(table_frame, text="🗑", bg='white', fg='red', 
                            font=('Roboto', 12), relief='flat', cursor='hand2')
        delete_btn.grid(row=2, column=5, sticky='e', padx=10, pady=8)
        
        # Bouton ajouter ligne produit
        add_product_btn = tk.Button(produits_frame, text="+ Ajouter ligne produit", 
                                bg='#f8f9fa', fg='black', font=('Roboto', 10), 
                                relief='solid', borderwidth=1, cursor='hand2', pady=10)
        add_product_btn.pack(fill='x', pady=(15, 0))
        
        # === RÉSUMÉ DE LA FACTURE (Colonne droite) ===
        tk.Label(right_column, text="Résumé de la facture", font=("Roboto", 16, "bold"), 
                bg="white", anchor="w").pack(anchor="w", pady=(0, 20))
        
        # Détails financiers
        details = [
            ("Total HT:", "€800.00"),
            ("Remise appliquée:", "-€40.00", "green"),
            ("TVA (18%):", "€136.80"),
            ("Total TTC:", "€896.80", "bold")
        ]
        
        for item in details:
            detail_frame = tk.Frame(right_column, bg="white")
            detail_frame.pack(fill="x", pady=5)
            
            label = item[0]
            value = item[1]
            style = item[2] if len(item) > 2 else "normal"
            
            tk.Label(detail_frame, text=label, font=("Roboto", 11), bg="white", 
                    anchor="w").pack(side="left")
            
            if style == "green":
                tk.Label(detail_frame, text=value, font=("Roboto", 11), bg="white", 
                        fg="green", anchor="e").pack(side="right")
            elif style == "bold":
                tk.Label(detail_frame, text=value, font=("Roboto", 14, "bold"), bg="white", 
                        anchor="e").pack(side="right")
            else:
                tk.Label(detail_frame, text=value, font=("Roboto", 11), bg="white", 
                        anchor="e").pack(side="right")
        
        # Bouton générer PDF
        generate_btn = tk.Button(right_column, text="📄 Générer PDF", bg="black", fg="white",
                                font=("Roboto", 11, "bold"), padx=20, pady=15, 
                                relief="flat", cursor="hand2")
        generate_btn.pack(fill='x', pady=(30, 0))

    def create_client_form(self):
        """Crée le formulaire client selon le type sélectionné"""
        # Nettoie le frame
        for widget in self.client_info_frame.winfo_children():
            widget.destroy()
        
        if self.client_type_var.get() == "nouveau":
            # Formulaire nouveau client
            tk.Label(self.client_info_frame, text="Informations du nouveau client", 
                    font=("Roboto", 16, "bold"), bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
            
            # Ligne avec Nom et Contact
            info_row = tk.Frame(self.client_info_frame, bg="white")
            info_row.pack(fill="x", pady=(0, 15))
            info_row.columnconfigure(0, weight=1)
            info_row.columnconfigure(1, weight=1)
            
            # Nom
            nom_frame = tk.Frame(info_row, bg="white")
            nom_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
            tk.Label(nom_frame, text="Nom", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            nom_entry = tk.Entry(nom_frame, font=("Roboto", 10), relief="solid", bd=1)
            nom_entry.pack(fill="x", pady=(5, 0))
            nom_entry.config(fg="black")
            
            # Contact
            contact_frame = tk.Frame(info_row, bg="white")
            contact_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
            tk.Label(contact_frame, text="Contact", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            contact_entry = tk.Entry(contact_frame, font=("Roboto", 10), relief="solid", bd=1)
            contact_entry.pack(fill="x", pady=(5, 0))
            contact_entry.config(fg="black")
            
            # IFU
            ifu_frame = tk.Frame(self.client_info_frame, bg="white")
            ifu_frame.pack(fill="x", pady=(0, 10))
            tk.Label(ifu_frame, text="IFU", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            ifu_entry = tk.Entry(ifu_frame, font=("Roboto", 10), relief="solid", bd=1)
            ifu_entry.pack(fill="x", pady=(5, 0))
            
            ifu_entry.config(fg="black")
            
        else:
            # Sélection client existant
            tk.Label(self.client_info_frame, text="Sélectionner un client existant", 
                    font=("Roboto", 16, "bold"), bg="white", anchor="w").pack(anchor="w", pady=(0, 15))
            
            # Liste déroulante des clients
            clients_frame = tk.Frame(self.client_info_frame, bg="white")
            clients_frame.pack(fill="x")
            
            tk.Label(clients_frame, text="Client", font=("Roboto", 10, "bold"), bg="white").pack(anchor="w")
            
            # Simule une liste déroulante (combobox)
            client_var = tk.StringVar(value="Sélectionner un client...")
            client_menu = tk.OptionMenu(clients_frame, client_var, 
                                    "Entreprise ABC", "Société XYZ", "Sarl Martin")
            client_menu.config(font=("Roboto", 10), relief="solid", bd=1, bg="white")
            client_menu.pack(fill="x", pady=(5, 0))

    def update_client_form(self, parent):
        """Met à jour le formulaire client quand le type change"""
        self.create_client_form()

    def productMotion(self, parent):
        frame1 = tk.Frame(parent,background="#F5F5F5")
        frame1.pack(fill='x')
        tk.Label(frame1,text='Ajouter un produit', font=('Roboto', 20, 'bold'),
                    background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        frame2 = tk.Frame(parent,background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2,text='Ajoutez un nouveau produit à votre catalogue', font=('Roboto', 12, 'bold'),
                    background='#F5F5F5', foreground='gray').pack(side='left')
            
        frame3 = tk.Frame(parent,background="#F5F5F5")
        frame3.pack(fill='x',padx=20,pady=20)
        form_frame = tk.Frame(frame3, bg="white", padx=20, pady=20, highlightbackground="#CCC", highlightthickness=1)
        form_frame.pack(pady=30, padx=30, fill="both")

            #  Titre
        titre = tk.Label(form_frame, text="Nouveau produit", font=("Roboto", 16, "bold"), bg="white", anchor="w")
        titre.pack(anchor="w")

        soustitre = tk.Label(form_frame, text="Remplissez les informations du produit", font=("Roboto", 10),
                                bg="white", fg="gray", pady=10)
        soustitre.pack(anchor="w")
         
            # Libellé 
        self.libelle_label = tk.Label(form_frame, text="Libellé", font=("Roboto", 9, "bold"), bg="white", anchor="w")
        self.libelle_label.pack(anchor="w", pady=(5, 0))

        self.libelle_input = tk.Text(form_frame, height=1, font=("Roboto", 10), bd=1, relief="solid")
        self.libelle_input.pack(fill='x', pady=(0, 10))

            # Prix unitaire
        self.prix_label = tk.Label(form_frame, text="Prix unitaire", font=("Roboto", 9, "bold"), bg="white", anchor="w")
        self.prix_label.pack(anchor="w", pady=(5, 0))

        self.prix_input = tk.Text(form_frame, height=1, font=("Roboto", 10), bd=1, relief="solid")
        self.prix_input.pack(fill='x', pady=(0, 15))

            # Bouton Ajouter
        ajouter_btn = tk.Button(form_frame, text=" +  Ajouter le produit", bg="black", fg="white",
                                    font=("Roboto", 10, "bold"), padx=10, pady=10, relief="flat",command= self.createProduct ,cursor="hand2")
        ajouter_btn.pack(fill='x')

    def createProduct(self):
        product = Products(self.libelle_input.get('1.0',tk.END),self.prix_input.get('1.0',tk.END))
        messagebox.showinfo('Création dun produit',message='le produit '+ self.libelle_input.get('1.0',tk.END) +' a été créer !')
        self.show_section(self.productMotion)
        

    def StatisquesMotion(self, parent):
        frame1 = tk.Frame(parent,background="#F5F5F5")
        frame1.pack(fill='x')
        tk.Label(frame1,text='Statistiques de ventes', font=('Roboto', 20, 'bold'),
                 background='#F5F5F5', foreground='#1C1C1C').pack(side='left')
        frame2 = tk.Frame(parent,background="#F5F5F5")
        frame2.pack(fill='x')
        tk.Label(frame2,text='Analysez vos performances commerciales', font=('Roboto', 12, 'bold'),
                 background='#F5F5F5', foreground='gray').pack(side='left')
        
        frame3 = tk.Frame(parent,background="#F5F5F5")
        frame3.pack(fill='x',padx=20,pady=20)

        # variables de statisques
        salesStats ={
            'produits le plus vendu' : 'Ordinateur portable',
            'Meilleur client' : 'Entreprise ABC',
            "Chiffre d'affaires total" : '$15,420'
        }

        for col_index, (label, value) in enumerate(salesStats.items()):
            underframe = tk.Frame(frame3, background='white', bd=1, relief='solid', padx=15, pady=15)
            underframe.grid(column=col_index, row=0, sticky='nsew', padx=10)

            # Stat title
            title_label = tk.Label(underframe, text=label, bg='white', font=('Roboto', 11), fg='#333')
            title_label.pack(anchor='w', pady=(10, 0))
        
            # Stat number
            number_label = tk.Label(underframe, text=value, bg='white', font=('Roboto', 16, 'bold'))
            number_label.pack(anchor='ne')

        frame4 =tk.Frame(parent,bg='white',height=5,padx=20, pady=20)
        frame4.pack(fill='both', padx=20, pady=20)
        # Titre
        tk.Label(frame4, text="Répartition des ventes par client", bg='white',
                font=('Roboto', 14, 'bold'), anchor='w').pack(fill='x', pady=(0, 10))

        # Données dictionnaire
        clientStats = {
            'Entreprise ABC': {'commande': 12, 'ca': '€8,500'},
            'Société XYZ': {'commande': 8, 'ca': '€4,200'},
            'Sarl Martin': {'commande': 5, 'ca': '€2,720'},
        }

        # En-têtes
        headers = ["Client", "Nombre de commandes", "Chiffre d'affaires"]
        table = tk.Frame(frame4, bg='white')
        table.pack(fill='both')

        for col, header in enumerate(headers):
            tk.Label(table, text=header, font=('Roboto', 10, 'bold'),
                    bg='white', fg='gray', padx=10, anchor='w').grid(row=0, column=col, sticky='ew')

        # Ligne horizontale sous les entêtes
        tk.Frame(table, height=1, bg='#ddd').grid(row=1, column=0, columnspan=3, sticky='ew', pady=(2, 5))

        # Ajout des lignes de données depuis le dictionnaire
        for row_index, (client, data) in enumerate(clientStats.items(), start=2):
            tk.Label(table, text=client, font=('Roboto', 10),
                    bg='white', fg='black', padx=10, anchor='w').grid(row=row_index, column=0, sticky='ew', pady=4)

            tk.Label(table, text=data['commande'], font=('Roboto', 10),
                    bg='white', fg='black', padx=10, anchor='w').grid(row=row_index, column=1, sticky='ew', pady=4)

            tk.Label(table, text=data['ca'], font=('Roboto', 10, 'bold'),
                    bg='white', fg='black', padx=10, anchor='w').grid(row=row_index, column=2, sticky='ew', pady=4)
        


    def on_click(self, section_function, clicked_button):
        # Met à jour le style des boutons
        for btn in self.sidebar_buttons:
            btn.config(background='black', foreground='white')
        clicked_button.config(background='white', foreground='black')

        # Switch les section de la scroll_frame
        self.show_section(section_function)

    # Gestion du scroll gérer par l'IA
    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_to_mousewheel(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))

    def _unbind_from_mousewheel(self, canvas):
        canvas.unbind_all("<MouseWheel>")

FacturationApp()
# print(statis.total_revenue())