# Système de Gestion de Facturation et d'Analyse des Ventes

## 🚀 Vue d'Ensemble du Projet

Ce projet est une application console/interface graphique conçue pour la gestion des opérations de facturation, la consultation de données clients et produits, et la génération de rapports de ventes. L'application utilise Python et ses bibliothèques clés pour offrir une solution efficace et structurée.

## ✨ Fonctionnalités Principales

L'application propose les fonctionnalités suivantes :

1. **Consultation de Données :**

   * Affichage des clients.
   * Affichage des produits.
   * Affichage des cartes de réduction.
2. **Génération de Factures :**

   * Gestion des nouveaux clients et des clients existants lors de la facturation.
   * Saisie des produits à facturer (code produit et quantité).
   * Récupération des données nécessaires depuis les fichiers Excel pour générer la facture.
   * Génération de factures au format PDF.
3. **Gestion des Produits :**

   * Permet d'ajouter un nouveau produit au fichier `Produits.xlsx`.
4. **Gestion des Cartes de Réduction :**

   * Création d'une carte de réduction pour le client lorsque le montant d'une facture se trouve dans une fourchette définie.
   * Aucune remise n'est appliquée sur la première facture d'un client.
   * Un client ne peut posséder qu'une seule carte de réduction.
5. **Statistiques sur les ventes :**
   Ajout de fonctionnalités pour analyser les données de ventes (ex: produit le plus vendu, total par client).
6. **Historique des factures :**
   Implémentation d'un système de suivi et d'archivage des factures générées.
7. **Interface graphique (GUI) :**
   Développement d'une interface utilisateur graphique (Tkinter).

## 🛠 Technologies Utilisées

Ce projet est développé en Python et utilise les bibliothèques suivantes :

* **Python 3.x**
* **Pandas :** Pour la manipulation des fichiers Excel via des DataFrames.
* **openpyxl / xlsxwriter :** Pour la gestion des fichiers Excel.
* **reportlab / fpdf / pdfkit :** Pour la génération de factures au format PDF.

## ⚙️ Structure des Données

L'application s'appuie sur trois fichiers Excel préexistants pour stocker les données :

* `Clients.xlsx` : Définit chaque client par un `code_client` (identifiant unique), un `nom`, un `contact`, et un `IFU` (Identifiant Fiscal Unique de 13 caractères).
* `Produits.xlsx` : Définit chaque produit par un `code_produit` (6 caractères), un `libelle`, et un `prix_unitaire`.
* `CartesReduction.xlsx` : Définit chaque carte de réduction par un `numero_carte` (chaîne numérique), un `code_client` (référence au client), et un `taux_reduction` (en pourcentage).

Les fichiers initiaux contiennent 10 produits et 2 clients.

## 🚀 Comment Démarrer

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/votre_utilisateur/tp-python.git
   cd tp-python
   ```
2. **Installer les dépendances :**
   Assurez-vous que Python 3 est installé. Ensuite, installez les bibliothèques requises :

   ```bash
   pip install pandas openpyxl reportlab # ou fpdf, ou pdfkit
   ```
3. **Lancer l'application :**

   ```bash
   python main.py # ou le nom de votre script principal
   ```

   L'application démarrera en mode console et affichera un menu principal.

## 🤝 Contributeurs

* [**AIHOUNHIN Eunock**](https://github.com/Eunock-web)
* [**ATOHOUN Andy**](https://github.com/e-mandy)
* [**BADAROU Mouwafic**](https://github.com/mouwaficbdr)
* [**OGOUDEDJI Seathiel**](https://github.com/seathiel-12)
* [**OKWUDIAFOR Wesley**](https://github.com/wesley-kami)

## 💡 Contribution

Ce projet est ouvert aux contributions. Pour toute idée d'amélioration, rapport de bug ou optimisation, veuillez ouvrir une *issue* ou soumettre une *pull request*.
