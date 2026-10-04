# Import des librairies
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page : titre de l'onglet et affichage sur toute la largeur
st.set_page_config(page_title="GlobalShop Direct - Segmentation RFM", layout="wide")

# Chargement du dataset RFM avec les segments
rfm = pd.read_csv("rfm_segments.csv", index_col="CustomerID")

# Ordre d'affichage des segments, du plus rentable au moins actif
ordre_segments = ["Champions", "Occasionnels", "Nouveaux clients", "Inactifs"]

# Couleur fixe pour chaque segment, identique sur tous les graphiques
couleurs = {
    "Champions": "#2ca02c",
    "Occasionnels": "#1f77b4",
    "Nouveaux clients": "#ff7f0e",
    "Inactifs": "#d62728",
}

# Part de chaque segment dans la clientèle (en %), utilisée dans les commentaires
parts = (rfm["Segment"].value_counts(normalize=True) * 100).round(1)

# Menu de navigation dans le panneau de gauche
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisissez une page :",
    [
        "Accueil",
        "Indicateurs clés",
        "Répartition des segments",
        "Visualisation PCA",
        "Comparaison des segments",
        "Personas marketing",
    ],
)

# Rappel visible sur toutes les pages, dans le panneau de gauche
st.sidebar.markdown("---")
st.sidebar.write(f"**Clients analysés** : {len(rfm)}")
st.sidebar.write("**Période** : du 01/12/2010 au 09/12/2011")
st.sidebar.write("**Modèle** : K-means, 4 segments")


# ----------------------------------------------------------------
# Page 1 : Accueil
# ----------------------------------------------------------------
if page == "Accueil":
    # Titre du dashboard
    st.title("GlobalShop Direct : Segmentation clients RFM")

    # Présentation du dashboard
    st.write("Ce dashboard présente la segmentation des clients de GlobalShop Direct, construite à partir de la méthode RFM et du clustering K-means.")
    st.write("**Récence** : nombre de jours entre le dernier achat du client et la fin de la période.")
    st.write("**Fréquence** : nombre de commandes passées sur la période.")
    st.write("**Montant** : total dépensé sur la période, en livres sterling (£).")
    st.write("**Période d'analyse** : du 1er décembre 2010 au 9 décembre 2011 (un peu plus d'un an).")
    st.info("Utilisez le menu de gauche pour naviguer entre les pages.")


# ----------------------------------------------------------------
# Page 2 : Indicateurs clés (cartes KPI)
# ----------------------------------------------------------------
elif page == "Indicateurs clés":
    # Filtre par segment dans le panneau de gauche
    choix = st.sidebar.selectbox("Filtrer par segment :", ["Tous les clients"] + ordre_segments)

    # Sélection des clients correspondant au choix
    if choix == "Tous les clients":
        donnees = rfm
    else:
        donnees = rfm[rfm["Segment"] == choix]

    # Titre de la page
    st.header(f"Indicateurs clés : {choix}")

    # 4 cartes côte à côte
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de clients", len(donnees))
    col2.metric("Récence médiane", f"{donnees['Recence'].median():.0f} jours")
    col3.metric("Fréquence médiane", f"{donnees['Frequence'].median():.0f} commandes")
    col4.metric("Montant médian", f"{donnees['Montant'].median():.0f} £")

    # Commentaire sous les cartes
    st.caption("Valeurs médianes calculées sur la période du 1er décembre 2010 au 9 décembre 2011.")
    st.caption("La médiane est utilisée car quelques clients aux valeurs très élevées faussent la moyenne.")


# ----------------------------------------------------------------
# Page 3 : Répartition des segments
# ----------------------------------------------------------------
elif page == "Répartition des segments":
    # Titre de la page
    st.header("Répartition des clients par segment")

    # Nombre de clients dans chaque segment, dans l'ordre choisi
    repartition = rfm["Segment"].value_counts().reindex(ordre_segments)

    # Création du graphique en barres, large et peu haut pour tenir sur une vue
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.bar(repartition.index, repartition.values, color=[couleurs[s] for s in repartition.index])
    ax.set_ylabel("Nombre de clients")

    # Affichage du nombre de clients au-dessus de chaque barre
    for i, valeur in enumerate(repartition.values):
        ax.text(i, valeur, str(valeur), ha="center", va="bottom")

    # Affichage du graphique
    st.pyplot(fig)

    # Commentaire sous le graphique
    st.caption(f"Les Inactifs forment le segment le plus important ({parts['Inactifs']} % des clients).")
    st.caption(f"Les Champions ne représentent que {parts['Champions']} % des clients.")


# ----------------------------------------------------------------
# Page 4 : Visualisation PCA
# ----------------------------------------------------------------
elif page == "Visualisation PCA":
    # Filtre par segment dans le panneau de gauche
    choix = st.sidebar.selectbox("Filtrer par segment :", ["Tous les clients"] + ordre_segments)

    # Sélection des clients correspondant au choix
    if choix == "Tous les clients":
        donnees = rfm
    else:
        donnees = rfm[rfm["Segment"] == choix]

    # Titre de la page
    st.header(f"Segments en 2D (PCA) : {choix}")

    # Nuage de points des clients sélectionnés, coloré par segment
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.scatterplot(x=donnees["PCA1"], y=donnees["PCA2"], hue=donnees["Segment"], palette=couleurs, s=15, ax=ax)
    ax.set_xlabel("PCA Component 1")
    ax.set_ylabel("PCA Component 2")

    # Affichage du graphique
    st.pyplot(fig)

    # Commentaire sous le graphique
    st.caption("Chaque point représente un client. Les segments occupent des zones distinctes, des Inactifs (à gauche) aux Champions (à droite).")
    st.caption("Les deux composantes principales expliquent environ 94 % de la variance des données RFM.")


# ----------------------------------------------------------------
# Page 5 : Comparaison des segments (boxplots)
# ----------------------------------------------------------------
elif page == "Comparaison des segments":
    # Titre de la page
    st.header("Comparaison des segments")

    # Métriques à comparer et titres des graphiques
    colonnes = ["Recence", "Frequence", "Montant"]
    titres = ["Récence (jours)", "Fréquence (commandes)", "Montant (£)"]

    # Création de la figure avec 3 graphiques côte à côte, large et peu haute
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), layout="constrained")

    # Un boxplot par métrique, avec un boxplot par segment
    for col, titre, ax in zip(colonnes, titres, axs.flat):
        sns.boxplot(x=rfm["Segment"], y=rfm[col], order=ordre_segments, palette=couleurs, ax=ax)
        ax.set_title(titre)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.tick_params(axis="x", rotation=20)

    # Échelle logarithmique pour la fréquence et le montant, pour rendre les boxplots lisibles
    axs[1].set_yscale("log")
    axs[2].set_yscale("log")

    # Affichage du graphique
    st.pyplot(fig)

    # Commentaire sous le graphique
    st.caption("Les Champions se distinguent par une récence faible, une fréquence et un montant élevés. Les Inactifs ont la récence la plus élevée.")
    
# ----------------------------------------------------------------
# Page 6 : Personas marketing
# ----------------------------------------------------------------
elif page == "Personas marketing":
    # Titre de la page
    st.header("Personas marketing")

    # Médianes RFM par segment, arrondies à l'entier, dans l'ordre choisi
    personas = rfm.groupby("Segment")[["Recence", "Frequence", "Montant"]].median().round(0).astype(int).reindex(ordre_segments)

    # Ajout du nombre de clients par segment
    personas["Effectif"] = rfm["Segment"].value_counts()

    # Ajout de la part de chaque segment dans la clientèle (en %)
    personas["Part (%)"] = parts

    # Action marketing recommandée pour chaque segment
    actions = {
        "Champions": "Fidélisation et offres premium (programme VIP, avantages exclusifs)",
        "Occasionnels": "Offres personnalisées et programme de points pour augmenter la fréquence",
        "Nouveaux clients": "Accueil et incitation à un deuxième achat (réduction sur la prochaine commande)",
        "Inactifs": "Campagne de relance peu coûteuse (offre promotionnelle)",
    }

    # Ajout de l'action recommandée dans le tableau
    personas["Action recommandée"] = personas.index.map(actions)

    # Noms de colonnes plus lisibles pour l'équipe marketing
    personas = personas.rename(columns={
        "Recence": "Récence médiane (jours)",
        "Frequence": "Fréquence médiane (commandes)",
        "Montant": "Montant médian (£)",
    })

    # Affichage du tableau sur toute la largeur, avec retour à la ligne dans les cellules
    st.table(personas)

    # Commentaire sous le tableau
    