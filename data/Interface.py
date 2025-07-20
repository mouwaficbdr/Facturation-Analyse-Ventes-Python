import tkinter as tk

class FacturationApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Application de Facturation")
        self.root.geometry("1000x600")
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
        quit_btn = tk.Button(header, text="Quitter l'application", fg="white", bg="#BF3F3F",
                             font=("Roboto", 11, "bold"), relief="solid", borderwidth=1, command=self.root.quit)
        quit_btn.pack(side="right", padx=15, pady=15)

    def create_body(self):
        self.bodyFrame.pack(fill="both", expand=True)

        self.bodyFrame.columnconfigure(0, weight=0)
        self.bodyFrame.columnconfigure(1, weight=1)
        self.bodyFrame.rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_board_container()
        self.show_section(self.StatisquesMotion)  

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
            'Total clients' : 3,
            'Produits' : 4,
            'Cartes de réduction' : 3,
            'CA Total' : '$1500' 
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

    def fileMotion(self, parent):
        tk.Label(parent, text='This is the file consulting section', font=('Roboto', 20, 'bold'),
                 background='#F5F5F5', foreground='black', width=100).pack()

    def factureMotion(self, parent):
        tk.Label(parent, text='This is the facture section', font=('Roboto', 20, 'bold'),
                 background='#F5F5F5', foreground='black', padx=10, width=300).pack(fill='x')

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

        # Code produit 
        code_label = tk.Label(form_frame, text="Code produit", font=("Roboto", 9, "bold"), bg="white", anchor="w")
        code_label.pack(anchor="w", pady=(5, 0))

        code_input = tk.Text(form_frame, height=1, font=("Roboto", 10), bd=1, relief="solid")
        code_input.pack(fill='x', pady=(0, 10))

        # Libellé 
        libelle_label = tk.Label(form_frame, text="Libellé", font=("Roboto", 9, "bold"), bg="white", anchor="w")
        libelle_label.pack(anchor="w", pady=(5, 0))

        libelle_input = tk.Text(form_frame, height=1, font=("Roboto", 10), bd=1, relief="solid")
        libelle_input.pack(fill='x', pady=(0, 10))

        # Prix unitaire
        prix_label = tk.Label(form_frame, text="Prix unitaire", font=("Roboto", 9, "bold"), bg="white", anchor="w")
        prix_label.pack(anchor="w", pady=(5, 0))

        prix_input = tk.Text(form_frame, height=1, font=("Roboto", 10), bd=1, relief="solid")
        prix_input.pack(fill='x', pady=(0, 15))

        # Bouton Ajouter
        ajouter_btn = tk.Button(form_frame, text=" +  Ajouter le produit", bg="black", fg="white",
                                font=("Roboto", 10, "bold"), padx=10, pady=10, relief="flat", cursor="hand2")
        ajouter_btn.pack(fill='x')

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
