# GlobalShop Direct : Segmentation clients RFM

Projet réalisé en binôme dans le cadre de la formation Data Analyst Simplon.

## Introduction

Ce projet propose une segmentation comportementale des clients de la plateforme e-commerce **GlobalShop Direct**, à partir de leur historique d'achats. La segmentation repose sur la méthode **RFM** (Récence, Fréquence, Montant) et sur des algorithmes de clustering (K-means et clustering hiérarchique).

Les résultats sont restitués dans un **dashboard Streamlit**, destiné aux équipes marketing, qui permet de consulter les caractéristiques de chaque segment et les actions recommandées.

## Contexte et problématique

La direction marketing de GlobalShop Direct souhaite mieux connaître ses clients pour adapter ses actions commerciales : fidéliser les meilleurs clients, relancer les clients inactifs et encourager les nouveaux clients à revenir.

**Problématique** : comment regrouper les clients en segments homogènes, à partir de leurs achats, pour cibler les actions marketing ?

## Données

Jeu de données **Online Retail**, issu de l'UCI Machine Learning Repository :

- 541 909 transactions d'un site de vente en ligne britannique ;
- période : du 1er décembre 2010 au 9 décembre 2011 ;
- montants en livres sterling (£).

Source : https://archive.ics.uci.edu/dataset/352/online+retail

Le fichier de données brutes n'est pas inclus dans ce dépôt en raison de sa taille. Il est téléchargeable à l'adresse ci-dessus.

## La méthode RFM

Chaque client est décrit par trois indicateurs :

- **Récence** : nombre de jours depuis son dernier achat ;
- **Fréquence** : nombre de commandes passées sur la période ;
- **Montant** : total dépensé sur la période.

## Démarche

### Activité 2 : Feature engineering RFM et prétraitement

1. **Exploration des données** : dimensions, valeurs manquantes, valeurs aberrantes, annulations.
2. **Nettoyage** : suppression des annulations, des lignes sans identifiant client (environ 25 % des transactions), des prix nuls et des doublons.
3. **Feature engineering** : calcul de la Récence, de la Fréquence et du Montant pour **4 338 clients**.
4. **Prétraitement** : transformation logarithmique (`np.log1p`) pour réduire la forte asymétrie des distributions, puis standardisation.

### Activité 3 : Clustering, PCA et profilage

1. **K-means** : choix du nombre de clusters par la méthode de l'Elbow (K = 4).
2. **Clustering hiérarchique** : dendrogramme (méthode de Ward), 5 clusters.
3. **Comparaison des deux méthodes** et choix du modèle retenu.
4. **PCA** : visualisation des clusters en 2D, avec 94 % de variance expliquée.
5. **Personas marketing** : nom et profil de chaque segment, actions recommandées.

### Activité 4 : Dashboard Streamlit

Restitution des résultats dans un dashboard interactif.

## Modèle retenu

Nous avons retenu **K-means avec 4 clusters** :

- 4 segments simples à présenter et à exploiter par les équipes marketing ;
- des segments plus équilibrés qu'avec le clustering hiérarchique ;
- une correspondance directe avec des personas RFM classiques.

Le clustering hiérarchique a apporté un éclairage complémentaire : il a permis d'identifier, parmi les meilleurs clients, une élite de 343 clients particulièrement rentables.

## Segments obtenus

Valeurs médianes sur la période étudiée :

| Segment | Clients | Récence | Fréquence | Montant | Action recommandée |
|---|---|---|---|---|---|
| Champions | 701 (16 %) | 8 jours | 10 commandes | 3 719 £ | Fidélisation et offres premium |
| Occasionnels | 1 182 (27 %) | 51 jours | 4 commandes | 1 374 £ | Offres personnalisées, programme de points |
| Nouveaux clients | 872 (20 %) | 19 jours | 2 commandes | 419 £ | Incitation à un deuxième achat |
| Inactifs | 1 583 (37 %) | 184 jours | 1 commande | 304 £ | Campagne de relance peu coûteuse |

## Dashboard Streamlit

Le dashboard comporte 6 pages :

- **Accueil** : présentation du projet et des indicateurs RFM ;
- **Indicateurs clés** : cartes KPI, avec un filtre par segment ;
- **Répartition des segments** : nombre de clients par segment ;
- **Visualisation PCA** : projection des clients en 2D, avec un filtre par segment ;
- **Comparaison des segments** : boxplots de la Récence, de la Fréquence et du Montant par segment ;
- **Personas marketing** : profil de chaque segment et action recommandée.

Lien du dashboard en ligne : *(à compléter après le déploiement)*

## Contenu du dépôt

- `OnlineretailActivité2.ipynb` : nettoyage, construction et prétraitement du dataset RFM
- `OnlineretailActivité3.ipynb` : clustering, PCA et définition des personas
- `app.py` : dashboard Streamlit
- `rfm.csv` et `rfm_scaled.csv` : datasets produits par l'activité 2, utilisés par l'activité 3
- `rfm_segments.csv` : dataset RFM avec les segments, utilisé par le dashboard
- `requirements.txt` : librairies nécessaires au dashboard

## Lancer le dashboard en local

```
pip install -r requirements.txt
streamlit run app.py
```

## Limites

- Les clients sans identifiant (environ 25 % des transactions) n'ont pas pu être segmentés.
- Les données datent de 2010-2011 : la segmentation devra être mise à jour avec des données récentes.
- Les segments découpent un ensemble continu de clients : un client situé à la frontière entre deux segments a un profil intermédiaire.

## Auteurs

- *(Mouna, Ilyes et Brice)*