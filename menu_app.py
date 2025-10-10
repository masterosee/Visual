# menu_app.py
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 🔥 CRITIQUE - évite les conflits de threads
import matplotlib.pyplot as plt
import plotly.express as px
from utils import cleaning
from modules.plots.time_series import plot_time_series, plot_time_series_multi

# ✅ VÉRIFICATION SIMPLIFIÉE
if 'user' not in st.session_state:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                padding: 25px; border-radius: 10px; color: white; text-align: center;'>
        <h2>🔐 Authentification Requise</h2>
        <p><strong>Vous devez vous connecter pour accéder à cette application</strong></p>
        <p>👉 <strong>Cliquez sur "Authentification" dans le menu de gauche</strong></p>
        <p>👉 <strong>Connectez-vous avec vos identifiants</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Vérifie si l'utilisateur est approuvé
from utils.db import load_users

@st.cache_data
def load_csv(file):
    """Charge un fichier CSV avec gestion d'encodage"""
    try:
        return pd.read_csv(file, encoding="latin1")
    except Exception:
        return pd.read_csv(file)

users = load_users()
user_row = users[users['username'].str.lower() == st.session_state['user'].lower()]

if user_row.empty or not user_row.iloc[0]['is_approved']:
    st.warning("⛔ Votre compte n'est pas encore approuvé.")
    st.stop()


def main():
    st.set_page_config(page_title="Visualisation Universelle", layout="wide")
    
    # ======== STYLE CSS COMPLET AVEC BACKGROUND ========
    st.markdown("""
    <style>
    /* Background principal de l'application */
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style pour le contenu principal */
    .block-container {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Style pour le sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        background-image: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style des headers */
    .css-10trblm {
        color: #2c3e50;
    }
    
    /* Style des radio buttons */
    .stRadio > div {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa;
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e9ecef;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
    }
    
    /* Style spécifique pour le bouton Export */
    div.stButton > button:first-child {
        background-color: #FFD700 !important;
        color: black !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 8px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #90EE90 !important;
        color: black !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    /* Style des file uploaders */
    .stFileUploader > div {
        background-color: white;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Style des dataframes */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    
    /* Amélioration de la lisibilité du texte */
    .css-18e3th9 {
        color: #000000;
    }
    
    /* Style pour les messages d'info */
    .stInfo {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 8px;
    }
    
    /* Style pour les messages de succès */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
    }
    
    /* Style pour les messages d'erreur */
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
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
            <div style="margin-left:15px; font-size:32px; font-weight:bold; color: #2c3e50;">Visualisation Universelle</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Bouton Export CORRIGÉ
        clicked = st.button("💾 Export", key="toggle_export")

    if clicked:
        st.session_state.show_export = not st.session_state.show_export

    # ======== MESSAGE LOREM ========
    st.write(
        "Une application modulaire qui transforme tout fichier CSV en graphique interactif, quel que soit le domaine. Elle s'adapte aux secteurs de l'économie, de la finance, de l'éducation, de la santé, de l'agriculture, de l'environnement, ou encore de la logistique. Grâce à sa compatibilité universelle avec tous les formats CSV, tous les secteurs d'activité et toutes les plateformes, elle s'intègre sans friction dans n'importe quel environnement professionnel. Son interface intuitive, son branding affirmé et sa structure optimisée en font un outil puissant pour les utilisateurs exigeants. "
    )

    # ======== MODULE EXPORT (AFFICHAGE CONDITIONNEL) ========
    if st.session_state.show_export:
        st.markdown("---")
        st.subheader("💾 Export / Sauvegarde de données")
        fichier_export = st.file_uploader("Importer un fichier CSV à exporter", type=["csv"], key="export_uploader")
        if fichier_export:
            try:
                df_export = load_csv(fichier_export)
                st.dataframe(df_export.head())
                csv = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Télécharger le fichier CSV",
                    data=csv,
                    file_name="export.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Erreur lors du chargement: {e}")
        else:
            st.info("Importez un fichier CSV pour activer l'exportation.")

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
                df = load_csv(fichier)
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
                df = load_csv(fichier)
                histogram.run(df)

        elif graphique == "Box Plot":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="box")
            if fichier:
                from modules.plots import boxplot
                df = load_csv(fichier)
                boxplot.run(df)

        elif graphique == "Nuage de points":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="scatter")
            if fichier:
                from modules.plots import scatter
                df = load_csv(fichier)
                scatter.run(df)

        elif graphique == "Courbes":
            fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="line")
            if fichier:
                from modules.plots import courbes
                df = load_csv(fichier)
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
            df = load_csv(fichier)
            if ts_type == "Série simple":
                fig = plot_time_series(df, "Date", "Confirmed", title="COVID-19 Confirmed Cases")
                st.pyplot(fig)
                plt.close(fig)  # 🔥 FERME LA FIGURE
            elif ts_type == "Séries multiples":
                fig = plot_time_series_multi(
                    df,
                    "Date",
                    ["Confirmed", "Deaths", "Recovered"],
                    title="COVID-19: Confirmed vs Deaths vs Recovered"
                )
                st.pyplot(fig)
                plt.close(fig)  # 🔥 FERME LA FIGURE
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
                df = load_csv(fichier)
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
                    plt.close(fig)  # 🔥 FERME LA FIGURE
                else:
                    st.warning("Colonnes 'Age' et 'Gender' introuvables.")

        # --- Climat ---
        with onglet[1]:
            st.write("🌡️ Graphiques climatiques")
            fichier = st.file_uploader("Importer un dataset climatique", type=["csv"], key="climat")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                if "Date" in df.columns and "Temperature" in df.columns:
                    fig, ax = plt.subplots()
                    ax.plot(pd.to_datetime(df["Date"]), df["Temperature"])
                    ax.set_title("Évolution de la température")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Température")
                    st.pyplot(fig)
                    plt.close(fig)  # 🔥 FERME LA FIGURE
                else:
                    st.warning("Colonnes 'Date' et 'Temperature' introuvables.")

        # --- Finances ---
        with onglet[2]:
            st.write("💹 Graphiques financiers (Car Sales)")
            fichier = st.file_uploader("Importer le dataset Car Sales", type=["csv"], key="carsales")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                if "Price" in df.columns and "Mileage" in df.columns:
                    fig, ax = plt.subplots()
                    ax.scatter(df["Mileage"], df["Price"], alpha=0.5)
                    ax.set_xlabel("Kilométrage")
                    ax.set_ylabel("Prix")
                    ax.set_title("Prix vs Kilométrage (Car Sales)")
                    st.pyplot(fig)
                    plt.close(fig)  # 🔥 FERME LA FIGURE
                else:
                    st.warning("Colonnes 'Price' et 'Mileage' introuvables.")

        # --- Géographie ---
        with onglet[3]:
            st.write("🗺️ Graphiques géographiques")
            fichier = st.file_uploader("Importer un dataset géographique", type=["csv"], key="geo")
            if fichier:
                df = load_csv(fichier)
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
                    # Plotly gère mieux la mémoire, pas besoin de close
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