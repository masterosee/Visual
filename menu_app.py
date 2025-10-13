
# menu_app.py
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
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

def section_telechargement_manuel():
    """Section élégante pour le téléchargement du manuel PDF"""
    st.markdown("---")
    
    st.markdown("""
    <style>
    .manuel-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 30px;
        border: 2px solid #FFD700;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
        text-align: center;
    }
    .manuel-title {
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .manuel-text {
        color: #555;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="manuel-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="manuel-title">📚 Guide Complet d\'Utilisation</h3>', unsafe_allow_html=True)
    st.markdown('<p class="manuel-text">Téléchargez le <strong>Manuel de Visualisation Universelle</strong> pour maîtriser toutes les fonctionnalités de l\'application. Ce guide détaillé vous accompagne pas à pas dans la création de visualisations impactantes, le nettoyage de données avancé et l\'exportation de vos résultats.</p>', unsafe_allow_html=True)
    
    try:
        with open("assets/Manuel_Visualisation_Universelle.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        st.markdown("""
        <style>
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #FFD700 0%, #D4AF37 100%) !important;
            color: black !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 12px 30px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
            margin: 0 auto !important;
        }
        div.stDownloadButton > button:hover {
            background: linear-gradient(135deg, #90EE90 0%, #32CD32 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(144, 238, 144, 0.4) !important;
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Télécharger le Manuel",
            data=pdf_data,
            file_name="Manuel_Visualisation_Universelle.pdf",
            mime="application/pdf",
            key="manuel_download"
        )
        
    except FileNotFoundError:
        st.error("❌ Le fichier du manuel n'est pas disponible.")
        st.info("💡 Assurez-vous que le dossier 'assets' contient le fichier 'Manuel_Visualisation_Universelle.pdf'")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Visualisation Universelle", layout="wide")
    
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .block-container {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        background-image: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .css-10trblm {
        color: #2c3e50;
    }
    .stRadio > div {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
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
    .stFileUploader > div {
        background-color: white;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 20px;
    }
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    .css-18e3th9 {
        color: #000000;
    }
    .stInfo {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 8px;
    }
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
    }
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    if "show_export" not in st.session_state:
        st.session_state.show_export = False

    col1, col2 = st.columns([6, 1])
    with col1:
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
        clicked = st.button("💾 Export", key="toggle_export")

    if clicked:
        st.session_state.show_export = not st.session_state.show_export

    st.write(
        "Une application modulaire qui transforme tout fichier CSV en graphique interactif, quel que soit le domaine. Elle s'adapte aux secteurs de l'économie, de la finance, de l'éducation, de la santé, de l'agriculture, de l'environnement, ou encore de la logistique. Grâce à sa compatibilité universelle avec tous les formats CSV, tous les secteurs d'activité et toutes les plateformes, elle s'intègre sans friction dans n'importe quel environnement professionnel. Son interface intuitive, son branding affirmé et sa structure optimisée en font un outil puissant pour les utilisateurs exigeants. "
    )

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
        section_telechargement_manuel()

    # === Nettoyage ===
    elif choix == "Nettoyage des données":
        st.subheader("🧹 Module de Nettoyage Avancé")
        
        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="clean")
        if fichier:
            try:
                df = load_csv(fichier)
                st.success(f"✅ Fichier chargé : {df.shape[0]} lignes × {df.shape[1]} colonnes")
                
                st.subheader("📋 Aperçu des données initiales")
                st.dataframe(df.head())
                
                st.subheader("⚙️ Options de Nettoyage")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    missing_strategy = st.selectbox(
                        "Stratégie pour valeurs manquantes (numériques):",
                        ["mean", "median", "zero", "drop"],
                        help="Comment gérer les valeurs manquantes dans les colonnes numériques"
                    )
                    
                    remove_duplicates = st.checkbox("Supprimer les doublons", value=True)
                    convert_types = st.checkbox("Convertir les types automatiquement", value=True)
                
                with col2:
                    remove_outliers = st.checkbox("Supprimer les valeurs aberrantes", value=False)
                    if remove_outliers:
                        outlier_threshold = st.slider(
                            "Seuil pour valeurs aberrantes (IQR):",
                            min_value=1.0,
                            max_value=3.0,
                            value=1.5,
                            step=0.1,
                            help="Plus le seuil est élevé, moins de valeurs seront considérées comme aberrantes"
                        )
                    else:
                        outlier_threshold = 1.5
                
                if st.button("🚀 Lancer le Nettoyage Complet", type="primary"):
                    with st.spinner("Nettoyage en cours..."):
                        try:
                            df_clean = cleaning.prepare_dataset(
                                df,
                                missing_strategy=missing_strategy,
                                remove_duplicates_flag=remove_duplicates,
                                convert_types_flag=convert_types,
                                remove_outliers_flag=remove_outliers,
                                outlier_threshold=outlier_threshold
                            )
                            
                            st.subheader("🎉 Résultats du Nettoyage")
                            st.success("Nettoyage terminé avec succès !")
                            
                            st.subheader("📊 Aperçu des données nettoyées")
                            st.dataframe(df_clean.head())
                            
                            st.subheader("📈 Statistiques finales")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Lignes", df_clean.shape[0], 
                                         delta=df_clean.shape[0] - df.shape[0])
                            with col2:
                                st.metric("Colonnes", df_clean.shape[1])
                            with col3:
                                completeness = (1 - df_clean.isnull().sum().sum() / (df_clean.shape[0] * df_clean.shape[1])) * 100
                                st.metric("Complétude", f"{completeness:.1f}%")
                            
                            st.subheader("💾 Téléchargement")
                            csv = df_clean.to_csv(index=False)
                            st.download_button(
                                label="⬇️ Télécharger les données nettoyées (CSV)",
                                data=csv,
                                file_name="donnees_nettoyees.csv",
                                mime="text/csv",
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors du nettoyage : {str(e)}")
                            st.info("💡 Essayez de modifier les options de nettoyage ou vérifiez votre fichier")
            
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
                st.info("💡 Vérifiez que votre fichier CSV est valide et bien formaté")
        else:
            st.info("📁 Veuillez importer un fichier CSV pour commencer le nettoyage")

    # === Graphiques ===
    elif choix == "Graphiques":
        st.subheader("📊 Menu Graphiques")
        graphique = st.selectbox(
            "Choisissez un type de graphique",
            [
                "Histogramme", "Box Plot", "Nuage de points", "Courbes",
                "🔴 Diagramme circulaire", 
                "📊 Barres groupées",
                "📈 Surfaces empilées",
                "🎯 Violon",
                "🔥 Carte thermique",
                "🐝 Bandes & Essaims",
                "📐 Pyramide des âges"
            ]
        )

        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="graph_upload")
        
        if fichier:
            df = load_csv(fichier)
            st.write("Aperçu des données :")
            st.dataframe(df.head())

            if graphique == "Histogramme":
                from modules.plots import histogram
                histogram.run(df)

            elif graphique == "Box Plot":
                from modules.plots import boxplot
                boxplot.run(df)

            elif graphique == "Nuage de points":
                from modules.plots import scatter
                scatter.run(df)

            elif graphique == "Courbes":
                from modules.plots import courbes
                courbes.run(df)

            elif graphique == "🔴 Diagramme circulaire":
                from modules.plots import pie_chart
                pie_chart.run(df)

            elif graphique == "📊 Barres groupées":
                from modules.plots import barres_groupes
                barres_groupes.run(df)
            
            elif graphique == "📈 Surfaces empilées":
                from modules.plots import stacked_area
                stacked_area.run(df)
                
            elif graphique == "🎯 Violon":
                from modules.plots import violin
                violin.run(df)
            
            elif graphique == "🔥 Carte thermique":
                from modules.plots import heatmap
                heatmap.run(df)
                
            elif graphique == "🐝 Bandes & Essaims":
                from modules.plots import strip_swarm
                strip_swarm.run(df)

            elif graphique == "📐 Pyramide des âges":
                from modules.plots import pyramide_ages
                pyramide_ages.run(df)

            else:
                st.info(f"Module {graphique} en cours de développement...")

        else:
            st.info("Veuillez importer un fichier CSV pour afficher les graphiques.")

    # === TimeSeries ===
    elif choix == "TimeSeries":
        st.subheader("⏱️ Menu TimeSeries")
        ts_type = st.radio(
            "Choisissez un type de série temporelle",
            ["Série simple", "Séries multiples", "🌿 Parcelle de Tiges"]
        )

        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="timeseries")
        if fichier:
            df = load_csv(fichier)
            if ts_type == "Série simple":
                fig = plot_time_series(df, "Date", "Confirmed", title="COVID-19 Confirmed Cases")
                st.pyplot(fig)
                plt.close(fig)
            elif ts_type == "Séries multiples":
                fig = plot_time_series_multi(
                    df,
                    "Date",
                    ["Confirmed", "Deaths", "Recovered"],
                    title="COVID-19: Confirmed vs Deaths vs Recovered"
                )
                st.pyplot(fig)
                plt.close(fig)
            elif ts_type == "🌿 Parcelle de Tiges":
                from modules.plots import stem
                stem.run(df)
        else:
            st.info("Veuillez importer un fichier CSV pour afficher la série temporelle.")

    # === Visualisation thématique ===
    elif choix == "Visualisation":
        st.subheader("📈 Visualisation thématique")
        onglet = st.tabs(["Démographie", "Climat", "Finances", "Géographie", "🗺️ Treemap"])

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
                    plt.close(fig)
                else:
                    st.warning("Colonnes 'Age' et 'Gender' introuvables.")

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
                    plt.close(fig)
                else:
                    st.warning("Colonnes 'Date' et 'Temperature' introuvables.")

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
                    plt.close(fig)
                else:
                    st.warning("Colonnes 'Price' et 'Mileage' introuvables.")

        with onglet[3]:
            st.write("🗺️ Graphiques géographiques")
            
            st.info("""
            **📋 Format requis pour la carte :**
            - `Country` : Noms de pays en **ANGLAIS** (ex: "France", "Germany", "United States")
            - `Value` : Valeurs numériques pour la couleur
            - Optionnel : Autres colonnes numériques ou catégorielles
            """)
            
            with st.expander("📖 Exemple de format de données"):
                st.write("""
                | Country         | Value | Population | Category |
                |-----------------|-------|------------|----------|
                | France          | 85    | 67000000   | Europe   |
                | Germany         | 92    | 83000000   | Europe   |
                | United States   | 95    | 331000000  | Americas |
                | Japan           | 89    | 126000000  | Asia     |
                """)
            
            fichier = st.file_uploader("Importer un dataset géographique", type=["csv"], key="geo")
            
            if fichier:
                df = load_csv(fichier)
                st.subheader("📊 Aperçu des données")
                st.dataframe(df.head())
                
                country_cols = [col for col in df.columns if 'country' in col.lower() or 'pays' in col.lower()]
                value_cols = df.select_dtypes(include=['number']).columns.tolist()
                
                if country_cols and value_cols:
                    st.success("✅ Colonnes détectées avec succès !")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        country_column = st.selectbox(
                            "Colonne des pays:",
                            options=country_cols,
                            index=0
                        )
                    
                    with col2:
                        value_column = st.selectbox(
                            "Colonne des valeurs:",
                            options=value_cols,
                            index=0
                        )
                    
                    st.subheader("🎨 Options de la carte")
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        color_scale = st.selectbox(
                            "Échelle de couleurs:",
                            ["Viridis", "Plasma", "Inferno", "Magma", "Blues", "Reds", "Greens"]
                        )
                    
                    with col4:
                        map_title = st.text_input("Titre de la carte:", "Carte thématique par pays")
                    
                    if st.button("🗺️ Générer la carte", type="primary"):
                        try:
                            df_clean = df[[country_column, value_column]].dropna()
                            
                            fig = px.choropleth(
                                df_clean,
                                locations=country_column,
                                locationmode="country names",
                                color=value_column,
                                color_continuous_scale=color_scale,
                                title=map_title,
                                hover_name=country_column,
                                labels={value_column: 'Valeur'}
                            )
                            
                            fig.update_layout(
                                geo=dict(
                                    showframe=False,
                                    showcoastlines=True,
                                    projection_type='equirectangular'
                                )
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.subheader("📈 Statistiques des données")
                            col_stat1, col_stat2, col_stat3 = st.columns(3)
                            
                            with col_stat1:
                                st.metric("Pays représentés", df_clean[country_column].nunique())
                            
                            with col_stat2:
                                st.metric("Valeur moyenne", f"{df_clean[value_column].mean():.2f}")
                            
                            with col_stat3:
                                st.metric("Valeur max", f"{df_clean[value_column].max():.2f}")
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la génération de la carte: {str(e)}")
                            st.info("💡 Vérifiez que les noms de pays sont en anglais et correctement orthographiés")
                
                else:
                    if not country_cols:
                        st.error("❌ Aucune colonne de pays détectée. Cherche colonnes avec 'country' ou 'pays'")
                    if not value_cols:
                        st.error("❌ Aucune colonne numérique détectée pour les valeurs")
                    
                    st.info("""
                    **Colonnes détectées dans votre fichier:**
                    - Textuelles: {}
                    - Numériques: {}
                    """.format(
                        [col for col in df.columns if df[col].dtype == 'object'],
                        value_cols
                    ))
            
            else:
                st.info("📁 Veuillez importer un CSV avec des données géographiques")

        with onglet[4]:
            st.write("🗺️ Treemap Hiérarchique")
            fichier = st.file_uploader("Importer un dataset hiérarchique", type=["csv"], key="treemap")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                from modules.plots import treemap
                treemap.run(df)
            else:
                st.info("Veuillez importer un CSV avec une structure hiérarchique (ex: Continent > Pays > Ville > Population)")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 0.9em; color: green;'>"
        "© 2025 Ossiny B. Tous droits réservés."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
