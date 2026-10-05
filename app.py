# Import des librairies
import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page : titre de l'onglet et affichage sur toute la largeur
st.set_page_config(page_title="GlobalShop Direct - Simulateur client", layout="wide")


# ----------------------------------------------------------------
# Préparation : données et centres des segments
# ----------------------------------------------------------------

# Chargement du dataset RFM avec les segments (produit par le notebook de l'activité 3)
rfm = pd.read_csv("rfm_segments.csv", index_col="CustomerID")

# Les 3 métriques RFM
colonnes = ["Recence", "Frequence", "Montant"]

# Même prétraitement que dans le notebook : transformation logarithmique
X_log = np.log1p(rfm[colonnes])

# Même prétraitement que dans le notebook : standardisation
# (même calcul que StandardScaler : on retire la moyenne, puis on divise par l'écart-type)
moyennes = X_log.mean()
ecarts_types = X_log.std(ddof=0)
X_scaled = (X_log - moyennes) / ecarts_types

# Centre de chaque segment : moyenne des clients du segment dans l'espace standardisé
# (ce sont les centres des clusters calculés par K-means)
centres = X_scaled.groupby(rfm["Segment"]).mean()

# Valeurs médianes de chaque segment, pour présenter le profil type
medianes = rfm.groupby("Segment")[colonnes].median()

# Nom affiché au singulier (on qualifie un seul client), description et action recommandée pour chaque segment
infos = {
    "Champions": {
        "nom": "Champion",
        "couleur": "#2ca02c",
        "profil": "Client qui achète récemment, souvent et beaucoup : un des clients les plus précieux.",
        "action": "Fidéliser : programme VIP, avantages exclusifs, offres premium.",
    },
    "Occasionnels": {
        "nom": "Occasionnel",
        "couleur": "#1f77b4",
        "profil": "Bon client, mais dont les achats sont espacés : fort potentiel de progression.",
        "action": "Faire commander plus souvent : offres personnalisées, programme de points.",
    },
    "Nouveaux clients": {
        "nom": "Nouveau client",
        "couleur": "#ff7f0e",
        "profil": "Client qui vient d'acheter, mais encore peu : l'enjeu est le deuxième achat.",
        "action": "Déclencher un deuxième achat : réduction sur la prochaine commande, e-mail de bienvenue.",
    },
    "Inactifs": {
        "nom": "Inactif",
        "couleur": "#d62728",
        "profil": "Client qui n'achète plus depuis longtemps et a peu dépensé : probablement perdu.",
        "action": "Relancer à faible coût : e-mail « vous nous manquez », offre promotionnelle.",
    },
}


# ----------------------------------------------------------------
# Interface du simulateur
# ----------------------------------------------------------------

# Titre et présentation
st.title("GlobalShop Direct : Simulateur de qualification client")
st.write("Saisissez le profil RFM d'un client pour connaître son segment et l'action marketing recommandée.")

# Trois colonnes : saisie à gauche, espace vide au milieu, résultat à droite
col_saisie, col_espace, col_resultat = st.columns([1, 0.3, 2])

with col_saisie:
    st.subheader("Profil du client")

    # Saisie de la récence (en jours)
    recence = st.number_input("Récence : jours depuis le dernier achat", min_value=1, max_value=1000, value=30, step=1)

    # Saisie de la fréquence (en nombre de commandes)
    frequence = st.number_input("Fréquence : nombre de commandes", min_value=1, max_value=500, value=3, step=1)

    # Saisie du montant (en livres sterling)
    montant = st.number_input("Montant : total dépensé (£)", min_value=1.0, max_value=500000.0, value=1000.0, step=50.0)

    # Bouton pour lancer la qualification
    lancer = st.button("Qualifier le client", type="primary")

with col_resultat:
    if lancer:
        # Mise en forme du client saisi, avec les mêmes colonnes que les données d'origine
        client = pd.DataFrame([[recence, frequence, montant]], columns=colonnes)

        # Même prétraitement que pour les autres clients : logarithme puis standardisation
        client_scaled = ((np.log1p(client) - moyennes) / ecarts_types).iloc[0]

        # Distance entre le client et le centre de chaque segment
        distances = np.sqrt(((centres - client_scaled) ** 2).sum(axis=1))

        # Comme K-means : le client appartient au segment dont le centre est le plus proche
        segment = distances.idxmin()
        info = infos[segment]

        # Affichage du segment, dans sa couleur
        st.subheader("Résultat")
        st.markdown(
            f"<h2 style='color:{info['couleur']}; margin-top:0'>{info['nom']}</h2>",
            unsafe_allow_html=True,
        )
        st.write(info["profil"])

        # Action marketing recommandée
        st.success(f"**Action recommandée** : {info['action']}")

        # Comparaison avec le client type du segment (valeurs médianes)
        st.write(f"**Profil type : {info['nom']}** (valeurs médianes du segment) :")
        c1, c2, c3 = st.columns(3)
        c1.metric("Récence médiane", f"{medianes.loc[segment, 'Recence']:.0f} jours")
        c2.metric("Fréquence médiane", f"{medianes.loc[segment, 'Frequence']:.0f} commandes")
        c3.metric("Montant médian", f"{medianes.loc[segment, 'Montant']:.0f} £")
    else:
        st.info("Renseignez le profil du client à gauche, puis cliquez sur « Qualifier le client ».")

# Rappel de la période et du modèle
st.caption("Segmentation K-means en 4 segments, construite sur 4 338 clients, du 1er décembre 2010 au 9 décembre 2011.")
