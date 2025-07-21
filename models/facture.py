from weasyprint import HTML
import pandas as pd
from datetime import datetime
import os

class FactureManager:
    def __init__(self, data_folder="export"):
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


    def ajouter_facture(self, numero_facture, remise, client, produits):
        """
        Ajoute une facture à l'historique, une ligne par produit.
        :param numero_facture: Numéro unique de facture
        :param client: Dictionnaire contenant les infos client
        :param produits: Liste de dictionnaires des produits
        """
        try:
            lignes = []
            for p in produits:
                montant_ht = p['quantite'] * p['prix']
                montant_remise = montant_ht * (1 - remise/100)
                tva = montant_remise * 0.18
                montant_ttc = montant_remise + tva
                ligne = {
                    "numero_facture": numero_facture,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "code_client": client['code'],
                    "nom_client": client['nom'],
                    "produits": p['code'],
                    "quantites": p['quantite'],
                    "prix_unitaire": f"{p['prix']:.2f}",
                    "total_ht": f"{montant_ht:.2f}",
                    "remise": f"{remise}%",
                    "tva": f"{tva:.2f}",
                    "total_ttc": f"{montant_ttc:.2f}"
                }
                lignes.append(ligne)

            # Mise à jour du fichier
            df = pd.read_excel(self.INVOICES_FILE)
            df = pd.concat([df, pd.DataFrame(lignes)], ignore_index=True)
            df.to_excel(self.INVOICES_FILE, index=False)

            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la facture : {str(e)}")
            return False


    def get_historique_complet(self):
        """
        Retourne l'historique complet des factures sous forme d'une liste de dictionnaires.
        Si le fichier est vide, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            if df.empty:
                return []
            df = df.sort_values('date', ascending=False)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de la lecture de l'historique : {str(e)}")
            return []

    def get_factures_client(self, code_client):
        """
        Retourne l'historique des factures pour un client spécifique sous forme d'une liste de dictionnaires.
        Si aucune facture n'est trouvée ou en cas d'erreur, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            df_client = df[df['code_client'] == code_client]
            if df_client.empty:
                return []
            df_client = df_client.sort_values('date', ascending=False)
            return df_client.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de la recherche : {str(e)}")
            return []

    def get_facture_detaillee(self, numero_facture):
        """
        Retourne une facture spécifique sous forme d'une liste de dictionnaires (une seule ligne ou vide).
        Si la facture n'est pas trouvée ou en cas d'erreur, retourne une liste vide.
        """
        try:
            df = pd.read_excel(self.INVOICES_FILE)
            facture = df[df['numero_facture'] == numero_facture]
            if facture.empty:
                return []
            return facture.to_dict(orient='records')
        except Exception as e:
            print(f"\nErreur lors de l'affichage : {str(e)}")
            return []


    def generatePDF(self, code_client):
        client = self.get_factures_client(code_client)
        facture_html = f"""
            <!DOCTYPE html>
                <html lang="fr">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Facture</title>
                    </head>
                    <body>
                        <style>
                            body{{
                                margin: 0;
                                padding: 0;
                            }}

                            *{{
                                font-family: "Poppins", sans-serif;
                            }}

                            .container{{
                                background-color: white;
                            }}

                            header{{
                                display: flex;
                                justify-content: space-between;
                                align-items: flex-start;
                            }}

                            .entreprise img{{
                                width: 50px;
                                height: 50px;
                                object-fit: contain;
                            }}

                            .entreprise h1{{
                                text-transform: uppercase;
                                font-weight: bold;
                            }}

                            .entreprise p, .facture p{{
                                color: #4B5594;
                            }}

                            .facture h4{{
                                font-size: 30px;
                                background-color: #2463EB;
                                border-radius: 10px;
                                padding: 7px 8px;
                                color: white;
                                text-transform: uppercase;
                                width: fit-content;
                                margin-bottom: 0;
                            }}

                            .facture p span{{
                                font-weight: bold;
                            }}

                            .details_facture{{
                                display: flex;
                                width: 100%;
                                justify-content: center;
                                gap: 50px;
                                margin: 30px 0;
                            }}

                            .client h3, .paiement h3{{
                                font-weight: bold;
                                position: relative;
                                margin-left: 10px;
                            }}

                            .client h3::before, .paiement h3::before{{
                                content: "";
                                position: absolute;
                                top: 0;
                                left: -10px;
                                height: 100%;
                                width: 5px;
                            }}

                            .client h3::before{{
                                background-color: blue;
                            }}

                            .paiement h3::before{{
                                background-color: green;
                            }}

                            .paiement, .client{{
                                width: 40%;
                                padding: 5px 10px;
                                background-color: #F9FAFB;
                                border-radius: 20px;
                            }}

                            .details_produits{{
                                width: 100%;
                                margin-bottom: 20px;
                            }}

                            .details_produits h3{{
                                font-weight: bold;
                                margin-left: 15px;
                                position: relative;
                            }}

                            .details_produits h3::before{{
                                content: "";
                                position: absolute;
                                top: 0;
                                background-color: violet;
                                left: -10px;
                                height: 100%;
                                width: 5px;
                            }}

                            .details_produits table{{
                                width: 100%;
                                margin: auto;
                                border: 20px;
                                border: 1px solid black;
                                border-radius: 20px;
                                text-align: center;
                                overflow: hidden;
                            }}

                            table, thead, td{{
                                border-collapse: collapse;
                            }}

                            table td{{
                                padding: 20px;
                            }}

                            table tr{{
                                border: 1px solid rgb(237, 234, 234);
                            }}

                            table thead{{
                                background-color: #F9FAFB;
                                font-weight: bold;
                            }}

                            .montant_container{{
                                width: 100%;
                                display: flex;
                                justify-content: flex-end;
                                margin-bottom: 30px;
                            }}

                            .montant{{
                                width: 400px;
                                background-color: #F9FAFB;
                                padding: 30px;
                                border-radius: 15px;
                            }}
                            
                            .montant div{{
                                margin-bottom: 15px;
                                width: 100%;
                                display: flex;
                                justify-content: space-between;
                            }}
                            
                            .conditions{{
                                width: 100%;
                                margin: 30px 0;
                            }}

                            .conditions h3{{
                                position: relative;
                                margin-left: 15px;
                            }}

                            .conditions h3::before{{
                                content: "";
                                position: absolute;
                                background-color: orange;
                                height: 100%;
                                width: 5px;
                                left: -10px;
                            }}

                            .conditions div{{
                                width: 90%;
                                margin: auto;
                                background-color: #FEFCE8;
                                height: 100px;
                                border-radius: 20px;
                                padding: 5px 15px;
                            }}

                            .conditions div p{{
                                margin-left: 10px;
                            }}

                            .authors{{
                                display: grid;
                                flex-wrap: wrap;
                                grid-template-columns: repeat(3, 1fr);
                                grid-template-rows: repeat(1, 1fr);
                                gap: 20px;
                                margin-bottom: 20px;
                            }}

                            .authors div{{
                                text-align: center;
                            }}

                            .authors div p{{
                                color: #4a4b4b;
                            }}

                            .infos{{
                                font-size: 14px;
                                text-align: center;
                                margin-bottom: 70px;
                            }}

                            .remerciements{{
                                margin: auto;
                                width: 80%;
                                background-color: #4854EB;
                                text-align: center;
                                color: white;
                                font-size: 20px;
                                border-radius: 15px;
                                padding: 4px 0;
                            }}


                        </style>

                        <div class="container">
                            <header>
                                <div class="entreprise">
                                    <img src="wasw.png" alt="">
                                    <h1>We Are Still Weak</h1>
                                    <p>Equipage de développeur</p>
                                    <p>Cotonou, Bénin</p>
                                </div>
                                <div class="facture">
                                    <h4>FACTURE</h4>
                                    <p><span>Date : </span>{client[0].date}</p>
                                    <p><span>Echéance : </span>No way</p>
                                </div>
                            </header>
                            <hr>
                            <div class="details_facture">
                                <div class="client">
                                    <h3>Facturé à :</h3>
                                    <div>
                                        <h4>{client[0].nom_client}</h4>
                        
                                        <p><span>Code client : </span>{client[0].code_client}</p>
                                        <p><span>IFU : </span></p>
                                    </div>
                                </div>
                                <div>
                                </div>
                                <div class="paiement">
                                    <h3>Détails du paiement</h3>
                                    <div>
                                        <p><span>Conditions : </span></p>
                                        <p><span>Mode de paiement : </span>Cash</p>
                                        <p><span>Devise : </span>Franc CFA (XOF)</p>
                                    </div>
                                </div>
                            </div>
                            <div class="details_produits">
                                <h3>Détails de la facture</h3>
                                <table>
                                    <thead>
                                        <tr>
                                            <td>Description</td>
                                            <td>Quantité</td>
                                            <td>Prix Unitaire</td>
                                            <td>Montant HT</td>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Akassa congelé</td>
                                            <td>1</td>
                                            <td>2000</td>
                                            <td>2000 FCFA</td>
                                        </tr>
                                        <tr>
                                            <td>Akassa congelé</td>
                                            <td>1</td>
                                            <td>2000</td>
                                            <td>2000 FCFA</td>
                                        </tr>
                                        <tr>
                                            <td>Akassa congelé</td>
                                            <td>1</td>
                                            <td>2000</td>
                                            <td>2000 FCFA</td>
                                        </tr>
                                        <tr>
                                            <td>Akassa congelé</td>
                                            <td>1</td>
                                            <td>2000</td>
                                            <td>2000 FCFA</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="montant_container">
                                <div class="montant">
                                    <div>
                                        <strong>Sous-Total HT :</strong>
                                        <span>FCFA</span>
                                    </div>
                                    <div>
                                        <strong>TVA (18%) :</strong>
                                        <span>FCFA</span>
                                    </div>
                                    <div>
                                        <strong>Remise :</strong>
                                        <span>FCFA</span>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <div class="conditions">
                                <h3>Notes et Conditions</h3>
                                <div>
                                    <p>Merci de croire en nous. Le paiement n'est plus modifiable. Achetez de nouveaux produits si vous voulez une autre facture.</p>
                                </div>
                            </div>
                            <hr>
                            <div class="authors">
                                <div>
                                    <h4>BADAROU Mouwafic (u_gon_hate_me)</h4>
                                    <p>Chef de l'équipe</p>
                                    <p>+229 01 91 48 60 08</p>
                                </div>
                                <div>
                                    <h4>OGOUDEDJI Seathiel (lawer)</h4>
                                    <p>Membre de l'équipe</p>
                                    <p>+229 01 46 61 82 29</p>
                                </div>
                                <div>
                                    <h4>ATOHOUN Andy (emandy)</h4>
                                    <p>Membre de l'équipe</p>
                                    <p>+229 01 52 69 74 59</p>
                                </div>
                                <div>
                                    <h4>OKWUDIAFOR Wesley (wesley_kami)</h4>
                                    <p>Membre de l'équipe</p>
                                    <p>+229 01 90 40 88 06</p>
                                </div>
                                <div>
                                    <h4>AIHOUNHIN Eunok (erwin_smith)</h4>
                                    <p>Membre de l'équipe</p>
                                    <p>+229 01 97 37 79 80</p>
                                </div> 
                            </div>
                            <hr>
                            <p class="infos">Cette facture est générée électroniquement et ne nécessite pas de vérification. Vous prenez mais vous ne doutez pas. Ne nous contactez pas.</p>
                            <div class="remerciements">
                                <p>Merci pour la confiance !</p>
                                <p>Entreprise We Are Still Weak - "T'inquiète"</p>
                            </div>
                        </div>
                    </body>
                </html>
        """
        HTML(string=facture_html).write_pdf('./invoices/facture.pdf') 
    
    
    #Fonction pour les calcules
    def calcul_remise(self, total_ht, remise_pourcent):
        #Calcule le montant de la remise
        return total_ht * (remise_pourcent / 100)

    def montant_ht_apres_remise(self, total_ht, remise_pourcent):
        #Calcule le montant HT après remise.
        return total_ht - self.calcul_remise(total_ht, remise_pourcent)

    def montant_tva(self, THT_remise, tva_pourcent=18):
        #Calcule le montant de la TVA sur le HT après remise.
        return THT_remise * (tva_pourcent / 100)

    def montant_ttc(self, THT_remise, tva_pourcent=18):
        #Calcule le montant TTC (HT après remise + TVA).
        return THT_remise + self.montant_tva(THT_remise, tva_pourcent)
