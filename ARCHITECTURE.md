# Architecture du Projet

## Squelette

Facturation-Analyse-Ventes-Python/
├── main.py # Point d'entrée principal
├── menu.py # Affichage et gestion du menu principal
├── controllers/ # Logique métier (gestion clients, produits, factures)
│ ├── client_controller.py(exemple)
│ ├── produit_controller.py(exemple)
│ ├── facture_controller.py(exemple)
│ └── reduction_controller.py(exemple)
├── models/ # Représentation des entités (POO ou dictionnaires organisés)
│ ├── client.py(exemple)
│ ├── produit.py(exemple)
│ ├── facture.py(exemple)
│ └── reduction.py(exemple)
├── utils/ # Fonctions utilitaires
│ ├── excel_service.py(exemple)
│ ├── pdf_service.py(exemple)
│ └── utils.py(exemple)
├── data/ # Fichiers Excel d'entrée et de mise à jour
│ ├── Clients.xlsx
│ ├── Produits.xlsx
│ └── CartesReduction.xlsx
├── exports/ # Dossier de sortie pour les factures PDF générées
└── README.md # Documentation

## Rôles des modules

main.py : boucle principale du programme, appelle le menu, redirige vers les fonctionnalités.

menu.py : gère l'affichage des options et l'entrée utilisateur.

controllers/ : logique fonctionnelle liée à chaque "ressource" (client, produit, facture...).

models/ : classes représentant les entités (Client, Produit...), ou simples fonctions de mapping.

utils/ : fonctions utilitaires

exports/ : factures PDF générées, historiques éventuels.
