
# menu_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utils import cleaning
from modules.plots.time_series import plot_time_series, plot_time_series_multi

import streamlit as st

# Vérifie si l'utilisateur est connecté
if 'user' not in st.session_state:
    st.warning("🔒 Accès refusé. Veuillez vous connecter via la page Authentification.")
    st.stop()

# Vérifie si l'utilisateur est approuvé
from utils.db import load_users

users = load_users()
user_row = users[users['username'].str.lower() == st.session_state['user'].lower()]

if user_row.empty or not user_row.iloc[0]['is_approved']:
    st.warning("⛔ Votre compte n'est pas encore approuvé.")
    st.stop()


def main():
    st.set_page_config(page_title="Visualisation Universelle", layout="wide")
    st.markdown("""
    <style>
    /* Style uniquement pour le bouton Export */
    div.export-btn div.stButton > button {
        background-color: gold !important;   /* Or (état normal) */
        color: black !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        padding: 8px 20px;
    }
    div.export-btn div.stButton > button:hover {
        background-color: lightgreen !important; /* Vert clair (hover) */
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)


    # === Initialisation du toggle export dans session_state ===
    if "show_export" not in st.session_state:
        st.session_state.show_export = False

    # ======== TITRE AVEC LOGO ET BOUTON EXPORT ========
    col1, col2 = st.columns([6, 1])
    with col1:
        # Affichage du logo SVG + titre
        st.markdown("""
        <div style="display:flex; align-items:center;">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="150" height="78" viewBox="0 0 500 260">
                  <defs>
                    <linearGradient id="goldStroke" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#FFD700"/>
                      <stop offset="50%" stop-color="#E6C200"/>
                      <stop offset="100%" stop-color="#B8860B"/>
                    </linearGradient>
                    <radialGradient id="irisPink" cx="50%" cy="45%" r="60%">
                      <stop offset="0%" stop-color="#FF4FA3"/>
                      <stop offset="100%" stop-color="#D4145A"/>
                    </radialGradient>
                    <radialGradient id="pupilLime" cx="50%" cy="40%" r="60%">
                      <stop offset="0%" stop-color="#B9FF3B"/>
                      <stop offset="100%" stop-color="#42B300"/>
                    </radialGradient>
                    <linearGradient id="barGold" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#FFE066"/>
                      <stop offset="100%" stop-color="#B8860B"/>
                    </linearGradient>
                    <linearGradient id="barLime" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#C8FF4A"/>
                      <stop offset="100%" stop-color="#3AA300"/>
                    </linearGradient>
                    <linearGradient id="barPink" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#FF6FB8"/>
                      <stop offset="100%" stop-color="#B3155A"/>
                    </linearGradient>
                    <filter id="glow">
                      <feGaussianBlur stdDeviation="3.5" result="blur"/>
                      <feMerge>
                        <feMergeNode in="blur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                  </defs>
                  <g transform="translate(60,50)">
                    <path d="M0,80 C40,0 160,0 200,80 C160,160 40,160 0,80 Z" fill="none" stroke="url(#goldStroke)" stroke-width="10"/>
                    <circle cx="100" cy="80" r="32" fill="url(#irisPink)"/>
                    <circle cx="100" cy="80" r="14" fill="url(#pupilLime)"/>
                  </g>
                  <g transform="translate(300,40)">
                    <rect x="0" y="120" width="40" height="60" rx="8" fill="url(#barGold)"/>
                    <rect x="60" y="80" width="40" height="100" rx="8" fill="url(#barLime)"/>
                    <rect x="120" y="30" width="40" height="150" rx="8" fill="url(#barPink)"/>
                  </g>
                  <path d="M 300 120 C 340 70, 390 60, 440 40" fill="none" stroke="url(#goldStroke)" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>
                </svg>
            </div>
            <div style="margin-left:15px; font-size:32px; font-weight:bold;">Visualisation Universelle</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
    # Bouton Export avec wrapper pour appliquer le style CSS
        st.markdown('<div class="export-btn">', unsafe_allow_html=True)
    clicked = st.button("💾 Export", key="toggle_export")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        st.session_state.show_export = not st.session_state.show_export


    # ======== STYLE CSS POUR BOUTON EXPORT ========
    st.markdown(
        """
        <style>
        button[k="toggle_export"] {
            background-color: #D4AF37;
            color: black;
            padding: 8px 16px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.2s ease-in-out;
        }
        button[k="toggle_export"]:hover {
            background-color: #90EE90;
            transform: translateY(-2px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ======== MESSAGE LOREM ========
    st.write(
        "Une application modulaire qui transforme tout fichier CSV en graphique interactif, quel que soit le domaine. Elle s’adapte aux secteurs de l’économie, de la finance, de l’éducation, de la santé, de l’agriculture, de l’environnement, ou encore de la logistique. Grâce à sa compatibilité universelle avec tous les formats CSV, tous les secteurs d’activité et toutes les plateformes, elle s’intègre sans friction dans n’importe quel environnement professionnel. Son interface intuitive, son branding affirmé et sa structure optimisée en font un outil puissant pour les utilisateurs  exigeants. "
    )

    # ======== MODULE EXPORT (AFFICHAGE CONDITIONNEL) ========
    if st.session_state.show_export:
        st.markdown("---")
        st.subheader("💾 Export / Sauvegarde de données")
        fichier_export = st.file_uploader("Importer un fichier CSV à exporter", type=["csv"], key="export_uploader")
        if fichier_export:
            try:
                df_export = pd.read_csv(fichier_export, encoding="latin1")
            except Exception:
                df_export = pd.read_csv(fichier_export)
            st.dataframe(df_export.head())
            csv = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Télécharger le fichier CSV",
                data=csv,
                file_name="export.csv",
                mime="text/csv",
            )
        else:
            st.info("Importez un fichier CSV pour activer l’exportation.")

    # ======== MENU LATÉRAL ========
    choix = st.sidebar.radio(
        "Navigation",
        [
            "Accueil",
            "Nettoyage des données",
            "Graphiques",
            "TimeSeries",
            "Visualisation",
        ]
    )

    # === Accueil ===
    if choix == "Accueil":
        st.subheader("Bienvenue 👋")
        st.write("Choisissez une option dans le menu de gauche.")

    # === Nettoyage ===
    elif choix == "Nettoyage des données":
        st.subheader("🧹 Module de nettoyage")
        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="clean")
        if fichier:
            try:
                df = pd.read_csv(fichier, encoding="latin1")
                df_clean = cleaning.prepare_dataset(df, missing_strategy="mean")
                st.success("Nettoyage terminé ✅")
                st.write("Aperçu des données nettoyées :")
                st.dataframe(df_clean.head())
            except Exception as e:
                st.error(f"Erreur lors du nettoyage : {e}")

    # === Graphiques ===
    elif choix == "Graphiques":
        st.subheader("📊 Menu Graphiques")
        graphique = st.selectbox(
            "Choisissez un type de graphique",
            ["Histogramme", "Box Plot", "Nuage de points", "Courbes"]
        )

        if graphique == "Histogramme":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="hist")
            if fichier:
                from modules.plots import histogram
                df = pd.read_csv(fichier, encoding="latin1")
                histogram.run(df)

        elif graphique == "Box Plot":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="box")
            if fichier:
                from modules.plots import boxplot
                df = pd.read_csv(fichier, encoding="latin1")
                boxplot.run(df)

        elif graphique == "Nuage de points":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="scatter")
            if fichier:
                from modules.plots import scatter
                df = pd.read_csv(fichier, encoding="latin1")
                scatter.run(df)

        elif graphique == "Courbes":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="line")
            if fichier:
                from modules.plots import courbes
                df = pd.read_csv(fichier, encoding="latin1")
                courbes.run(df)

    # === TimeSeries ===
    elif choix == "TimeSeries":
        st.subheader("⏱️ Menu TimeSeries")
        ts_type = st.radio(
            "Choisissez un type de série temporelle",
            ["Série simple", "Séries multiples"]
        )

        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="timeseries")
        if fichier:
            df = pd.read_csv(fichier, encoding="latin1")
            if ts_type == "Série simple":
                fig = plot_time_series(df, "Date", "Confirmed", title="COVID-19 Confirmed Cases")
                st.pyplot(fig)
            elif ts_type == "Séries multiples":
                fig = plot_time_series_multi(
                    df,
                    "Date",
                    ["Confirmed", "Deaths", "Recovered"],
                    title="COVID-19: Confirmed vs Deaths vs Recovered"
                )
                st.pyplot(fig)
        else:
            st.info("Veuillez importer un fichier CSV pour afficher la série temporelle.")

    # === Visualisation thématique ===
    elif choix == "Visualisation":
        st.subheader("📈 Visualisation thématique")
        onglet = st.tabs(["Démographie", "Climat", "Finances", "Géographie"])

        # --- Démographie ---
        with onglet[0]:
            st.write("📊 Graphiques démographiques")
            fichier = st.file_uploader("Importer un dataset démographique", type=["csv"], key="demo")
            if fichier:
                df = pd.read_csv(fichier, encoding="latin1")
                st.dataframe(df.head())
                if "Age" in df.columns and "Gender" in df.columns:
                    fig, ax = plt.subplots()
                    df[df["Gender"] == "Male"]["Age"].hist(alpha=0.5, label="Male", bins=20)
                    df[df["Gender"] == "Female"]["Age"].hist(alpha=0.5, label="Female", bins=20)
                    ax.set_xlabel("Âge")
                    ax.set_ylabel("Nombre")
                    ax.set_title("Pyramide des âges simplifiée")
                    plt.legend()
                    st.pyplot(fig)
                else:
                    st.warning("Colonnes 'Age' et 'Gender' introuvables.")

        # --- Climat ---
        with onglet[1]:
            st.write("🌡️ Graphiques climatiques")
            fichier = st.file_uploader("Importer un dataset climatique", type=["csv"], key="climat")
            if fichier:
                df = pd.read_csv(fichier, encoding="latin1")
                st.dataframe(df.head())
                if "Date" in df.columns and "Temperature" in df.columns:
                    fig, ax = plt.subplots()
                    ax.plot(pd.to_datetime(df["Date"]), df["Temperature"])
                    ax.set_title("Évolution de la température")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Température")
                    st.pyplot(fig)
                else:
                    st.warning("Colonnes 'Date' et 'Temperature' introuvables.")

        # --- Finances ---
        with onglet[2]:
            st.write("💹 Graphiques financiers (Car Sales)")
            fichier = st.file_uploader("Importer le dataset Car Sales", type=["csv"], key="carsales")
            if fichier:
                df = pd.read_csv(fichier, encoding="latin1")
                st.dataframe(df.head())
                if "Price" in df.columns and "Mileage" in df.columns:
                    fig, ax = plt.subplots()
                    ax.scatter(df["Mileage"], df["Price"], alpha=0.5)
                    ax.set_xlabel("Kilométrage")
                    ax.set_ylabel("Prix")
                    ax.set_title("Prix vs Kilométrage (Car Sales)")
                    st.pyplot(fig)
                else:
                    st.warning("Colonnes 'Price' et 'Mileage' introuvables.")

        # --- Géographie ---
        with onglet[3]:
            st.write("🗺️ Graphiques géographiques")
            fichier = st.file_uploader("Importer un dataset géographique", type=["csv"], key="geo")
            if fichier:
                df = pd.read_csv(fichier, encoding="latin1")
                st.dataframe(df.head())
                if "Country" in df.columns and "Value" in df.columns:
                    fig = px.choropleth(
                        df,
                        locations="Country",
                        locationmode="country names",
                        color="Value",
                        color_continuous_scale="Viridis",
                        title="Carte thématique par pays"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Le dataset doit contenir les colonnes 'Country' et 'Value'.")
            else:
                st.info("Veuillez importer un CSV avec au moins 'Country' et 'Value'.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em; color: green;'>"
    "© 2025 Ossiny B. Tous droits réservés."
    "</div>",
    unsafe_allow_html=True
)


if __name__ == "__main__":
    main()
