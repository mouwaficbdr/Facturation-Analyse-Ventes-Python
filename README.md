# Système de Gestion de Facturation et d'Analyse des Ventes

## 🚀 Vue d'Ensemble du Projet

Ce projet est une application console/interface graphique conçue pour la gestion des opérations de facturation, la consultation de données clients et produits, et la génération de rapports de ventes. L'application utilise Python et ses bibliothèques clés pour offrir une solution efficace et structurée.

## ✨ Fonctionnalités Principales

L'application propose les fonctionnalités suivantes :

1.  **Consultation de Données :**
    * [cite_start]Affichage des clients. [cite: 32]
    * [cite_start]Affichage des produits. [cite: 33]
    * [cite_start]Affichage des cartes de réduction. [cite: 34]

2.  **Génération de Factures :**
    * [cite_start]Gestion des nouveaux clients et des clients existants lors de la facturation. [cite: 37]
    * [cite_start]Saisie des produits à facturer (code produit et quantité). [cite: 39]
    * [cite_start]Récupération des données nécessaires depuis les fichiers Excel pour générer la facture. [cite: 40]
    * [cite_start]Génération de factures au format PDF. [cite: 46]

3.  **Gestion des Produits :**
    * [cite_start]Permet d'ajouter un nouveau produit au fichier `Produits.xlsx`. [cite: 43]

4.  **Gestion des Cartes de Réduction :**
    * [cite_start]Création d'une carte de réduction pour le client lorsque le montant d'une facture se trouve dans une fourchette définie. [cite: 62]
    * [cite_start]Aucune remise n'est appliquée sur la première facture d'un client. [cite: 64]
    * [cite_start]Un client ne peut posséder qu'une seule carte de réduction. [cite: 65]
  
5. **Statistiques sur les ventes :** Ajout de fonctionnalités pour analyser les données de ventes (ex: produit le plus vendu, total par client).
   
6. **Historique des factures :** Implémentation d'un système de suivi et d'archivage des factures générées.
   
7. **Interface graphique (GUI) :** Développement d'une interface utilisateur graphique`(Tkinter)`. 

## 🛠 Technologies Utilisées

Ce projet est développé en Python et utilise les bibliothèques suivantes :

* **Python 3.x**
* [cite_start]**Pandas :** Pour la manipulation des fichiers Excel via des DataFrames. [cite: 3, 60]
* [cite_start]**openpyxl / xlsxwriter :** Pour la gestion des fichiers Excel. [cite: 66]
* [cite_start]**reportlab / fpdf / pdfkit :** Pour la génération de factures au format PDF. [cite: 61]

## ⚙️ Structure des Données

[cite_start]L'application s'appuie sur trois fichiers Excel préexistants pour stocker les données[cite: 6]:

* [cite_start]`Clients.xlsx` : Définit chaque client par un `code_client` (identifiant unique), un `nom`, un `contact`, et un `IFU` (Identifiant Fiscal Unique de 13 caractères). [cite: 7, 9, 10, 11, 12, 13, 14]
* [cite_start]`Produits.xlsx` : Définit chaque produit par un `code_produit` (6 caractères), un `libelle`, et un `prix_unitaire`. [cite: 14, 15, 16, 17, 18]
* [cite_start]`CartesReduction.xlsx` : Définit chaque carte de réduction par un `numero_carte` (chaîne numérique), un `code_client` (référence au client), et un `taux_reduction` (en pourcentage). [cite: 19, 20, 21, 22, 23, 24]

[cite_start]Les fichiers initiaux contiennent 10 produits et 2 clients. [cite: 25, 26, 27]

## 🚀 Comment Démarrer

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/votre_utilisateur/tp-python.git](https://github.com/votre_utilisateur/tp-python.git)
    cd tp-python
    ```
2.  **Installer les dépendances :**
    Assurez-vous que Python 3 est installé. Ensuite, installez les bibliothèques requises :
    ```bash
    pip install pandas openpyxl reportlab # ou fpdf, ou pdfkit
    ```
3.  **Lancer l'application :**
    ```bash
    python main.py # ou le nom de votre script principal
    ```
    [cite_start]L'application démarrera en mode console et affichera un menu principal. [cite: 29]


## 👥 Contributeurs

* [mouwaficbdr](https://github.com/mouwaficbdr)
* [seathiel-12](https://github.com/seathiel-12)
* [e-mandy](https://github.com/e-mandy)
* [wesley-kami](https://github.com/wesley-kami)
* [Eunock-web](https://github.com/Eunock-web)

## 🤝 Contribution

Ce projet est ouvert aux contributions. Pour toute idée d'amélioration, rapport de bug ou optimisation, veuillez ouvrir une *issue* ou soumettre une *pull request*.
