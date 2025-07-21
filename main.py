from models.facture import FactureManager
import os

def test_ajouter_facture():
    """
    Test de la fonction ajouter_facture avec des données d'exemple.
    """
    print("=== Test de la fonction ajouter_facture ===\n")
    
    # 1. Créer une instance du gestionnaire
    facture_manager = FactureManager()
    
    # 2. Données de test
    numero_facture = "FACT001"
    remise = 10  # 10% de remise
    
    # Données du client
    client = {
        "code": "C001",
        "nom": "Entreprise Test SARL"
    }
    
    # Liste des produits
    produits = [
        {
            "code": "PROD001",
            "nom": "Ordinateur portable",
            "quantite": 2,
            "prix": 150000.00
        },
        {
            "code": "PROD002", 
            "nom": "Souris sans fil",
            "quantite": 5,
            "prix": 5000.00
        },
        {
            "code": "PROD003",
            "nom": "Clavier mécanique",
            "quantite": 3,
            "prix": 25000.00
        }
    ]
    
    print("Données de test :")
    print(f"- Numéro de facture : {numero_facture}")
    print(f"- Remise : {remise}%")
    print(f"- Client : {client['nom']} (Code: {client['code']})")
    print("\nProduits :")
    for i, prod in enumerate(produits, 1):
        print(f"  {i}. {prod['nom']} - Quantité: {prod['quantite']} - Prix: {prod['prix']} FCFA")
    
    print("\n" + "="*50)
    
    # 3. Appeler la fonction ajouter_facture
    print("\nAjout de la facture en cours...")
    resultat = facture_manager.ajouter_facture(numero_facture, remise, client, produits)
    
    # 4. Vérifier le résultat
    if resultat:
        print("✅ Facture ajoutée avec succès !")
        
        # 5. Vérifier que la facture a bien été ajoutée
        print("\nVérification de l'ajout...")
        factures_client = facture_manager.get_factures_client(client['code'])
        
        if factures_client:
            print(f"✅ {len(factures_client)} ligne(s) de facture trouvée(s) pour le client {client['code']}")
            
            # Afficher les détails de la facture ajoutée
            print("\nDétails de la facture ajoutée :")
            for ligne in factures_client:
                if ligne['numero_facture'] == numero_facture:
                    print(f"  - Produit: {ligne['produits']}")
                    print(f"  - Quantité: {ligne['quantites']}")
                    print(f"  - Prix unitaire: {ligne['prix_unitaire']} FCFA")
                    print(f"  - Total HT: {ligne['total_ht']} FCFA")
                    print(f"  - TVA: {ligne['tva']} FCFA")
                    print(f"  - Total TTC: {ligne['total_ttc']} FCFA")
                    print(f"  - Remise: {ligne['remise']}")
                    print("  ---")
        else:
            print("❌ Aucune facture trouvée pour ce client")
    else:
        print("❌ Erreur lors de l'ajout de la facture")
    
    print("\n=== Fin du test ===")

def test_ajouter_facture_avec_erreur():
    """
    Test avec des données invalides pour vérifier la gestion d'erreur.
    """
    print("\n=== Test avec données invalides ===")
    
    facture_manager = FactureManager()
    
    # Test avec un client invalide (sans clé 'code')
    client_invalide = {
        "nom": "Client sans code"
    }
    
    produits_test = [
        {
            "code": "PROD001",
            "quantite": 1,
            "prix": 1000.00
        }
    ]
    
    print("Test avec client invalide (sans code)...")
    resultat = facture_manager.ajouter_facture("FACT002", 5, client_invalide, produits_test)
    
    if not resultat:
        print("✅ Gestion d'erreur correcte - La facture n'a pas été ajoutée")
    else:
        print("❌ La gestion d'erreur n'a pas fonctionné comme attendu")

if __name__ == '_main_':
    # Test principal
    test_ajouter_facture()
    
    # Test avec erreur
    test_ajouter_facture_avec_erreur()