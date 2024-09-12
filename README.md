# Unification_des_Données

## Description
Unification_des_Données est un projet visant à unifier et à consolider des données personnelles provenant de plusieurs sources. Le projet utilise des techniques de traitement de données avancées, comme l'algorithme Soundex, pour identifier les correspondances potentielles entre les enregistrements malgré les variations d'orthographe dans les noms ou prénoms. Un modèle de machine learning est utilisé pour prédire si deux enregistrements représentent la même personne.

## Fonctionnalités
- **Chargement de fichiers CSV** : Téléversez des fichiers CSV contenant des informations personnelles pour effectuer l'unification.
- **Transformation Soundex** : Applique l'algorithme Soundex pour normaliser les noms et prénoms.
- **Recherche de correspondances** : Compare les enregistrements avec les données existantes pour trouver les correspondances possibles.
- **Prédiction de correspondances** : Utilise un modèle de machine learning pour prédire si deux enregistrements correspondent à la même personne.
- **Visualisation des données** : Visualise les résultats avec des graphiques pour les lieux, les sexes, et les dates de naissance.

## Prérequis
Avant de démarrer le projet, assurez-vous d'avoir installé les dépendances suivantes :
- Python 3.x
- pandas
- matplotlib
- streamlit
- scikit-learn
## Utilisation
1. Lancer l'application Streamlit :
    ```bash
    streamlit run app.py
    ```
2. Téléversez votre fichier CSV contenant les informations personnelles.
3. Utilisez le formulaire pour saisir les informations (nom, prénom, etc.) pour rechercher des correspondances et afficher les résultats.

## Structure du Projet
- `app.py` : Code principal pour exécuter l'application Streamlit.
- `creation_modele_unification_donnees.ipynb` : code de creation de model de classifaction
- `style.css` : Fichier CSS pour personnaliser l'interface utilisateur.
- `README.md` : Ce fichier de documentation.

## Contact
Pour toute question, veuillez contacter  à [chattichiheb35@gmail.com].
