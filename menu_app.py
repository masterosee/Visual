
# menu_app.py
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 🔥 CRITIQUE - évite les conflits de threads
import matplotlib.pyplot as plt
import plotly.express as px
from utils import cleaning
from modules.plots.time_series import run_simple, run_multiple

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


def section_telechargement_manuel():
    """Section élégante pour le téléchargement du manuel PDF"""
    st.markdown("---")
    
    # Style CSS pour le bouton
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
    
    # Carte avec composants Streamlit
    st.markdown('<div class="manuel-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="manuel-title">📚 Guide Complet d\'Utilisation</h3>', unsafe_allow_html=True)
    st.markdown('<p class="manuel-text">Téléchargez le <strong>Manuel de Visualisation Universelle</strong> pour maîtriser toutes les fonctionnalités de l\'application. Ce guide détaillé vous accompagne pas à pas dans la création de visualisations impactantes, le nettoyage de données avancé et l\'exportation de vos résultats.</p>', unsafe_allow_html=True)
    
    # Bouton de téléchargement avec style personnalisé
    try:
        with open("assets/Manuel_Visualisation_Universelle.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        # Style pour le bouton de téléchargement
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
    st.set_page_config(
        page_title="Visualisation Universelle", 
        layout="centered",  # ✅ Optimisé pour mobile
        initial_sidebar_state="auto"
    )
    
    # ======== STYLE CSS COMPLET AVEC SUPPORT MOBILE ========
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
    
<<<<<<< HEAD
    /* Style pour le bouton PDF */
    .download-btn-pdf {
        background: #FFD700 !important;
        color: black !important;
        padding: 15px 30px !important;
        text-decoration: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        display: inline-block !important;
        border: 2px solid #FFD700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    .download-btn-pdf:hover {
        background: #90EE90 !important;
        color: black !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        border-color: #90EE90 !important;
=======
    /* ======== STYLES MOBILE ======== */
    @media (max-width: 768px) {
        /* Adapter le contenu principal */
        .main .block-container {
            padding: 1rem;
            margin-top: 0.5rem;
        }
        
        /* Agrandir les boutons */
        div.stButton > button {
            width: 100% !important;
            padding: 12px !important;
            font-size: 16px !important;
        }
        
        /* Adapter les file uploaders */
        .stFileUploader > div {
            padding: 15px;
        }
        
        /* Adapter les colonnes */
        .row-widget.stColumns {
            flex-direction: column;
        }
        
        /* Réduire la taille du logo */
        svg {
            width: 100px !important;
            height: auto !important;
        }
        
        /* Adapter la taille du titre */
        .css-10trblm {
            font-size: 24px !important;
        }
        
        /* Agrandir les radios et selects */
        .stRadio > div {
            padding: 8px;
        }
        
        .stSelectbox > div > div {
            padding: 10px;
        }
        
        /* Simplifier le header */
        .css-1v0mbdj {
            flex-direction: column;
            text-align: center;
        }
    }
    
    /* Pour les très petits écrans */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .css-10trblm {
            font-size: 20px !important;
        }
        
        /* Réduire encore le logo */
        svg {
            width: 80px !important;
        }
>>>>>>> 9efcac9f50789b947bd04cd31bce189ce6bd735e
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
        <div style="display:flex; align-items:center; justify-content:center;">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="120" height="62" viewBox="0 0 500 260">
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
            <div style="margin-left:15px; font-size:28px; font-weight:bold; color: #2c3e50;">Visualisation Universelle</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Bouton Export
        clicked = st.button("💾 Export", key="toggle_export")

    if clicked:
        st.session_state.show_export = not st.session_state.show_export

    # ======== MESSAGE LOREM ========
    st.write(
        "Une application modulaire qui transforme tout fichier CSV en graphique interactif, quel que soit le domaine. Elle s'adapte aux secteurs de l'économie, de la finance, de l'éducation, de la santé, de l'agriculture, de l'environnement, ou encore de la logistique."
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
        
        # Ajout de la section téléchargement manuel dans l'accueil
        section_telechargement_manuel()

    # === Nettoyage ===
    elif choix == "Nettoyage des données":
        st.subheader("🧹 Module de Nettoyage Avancé")
        
        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="clean")
        if fichier:
            try:
                # Chargement avec gestion d'erreurs
                df = load_csv(fichier)
                st.success(f"✅ Fichier chargé : {df.shape[0]} lignes × {df.shape[1]} colonnes")
                
                # Aperçu initial
                st.subheader("📋 Aperçu des données initiales")
                st.dataframe(df.head())
                
                # Options de nettoyage
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
                
                # Bouton de nettoyage
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
                            
                            # Résultats
                            st.subheader("🎉 Résultats du Nettoyage")
                            st.success("Nettoyage terminé avec succès !")
                            
                            # Aperçu des données nettoyées
                            st.subheader("📊 Aperçu des données nettoyées")
                            st.dataframe(df_clean.head())
                            
                            # Statistiques finales
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
                            
                            # Téléchargement
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
                from modules.plots import pyramid
                pyramid.run(df)


            # Les autres graphiques seront ajoutés au fur et à mesure
            else:
                st.info(f"Module {graphique} en cours de développement...")

        else:
            st.info("Veuillez importer un fichier CSV pour afficher les graphiques.")

    # === TimeSeries ===
    elif choix == "TimeSeries":
        st.subheader("⏱️ Menu TimeSeries")
        
        ts_type = st.radio(
            "Choisissez un type de série temporelle",
<<<<<<< HEAD
            ["Série simple", "Séries multiples", "🌿 Parcelle de Tiges"]
=======
            ["Série simple", "Séries multiples", "🌿 Parcelle de Tiges"],
            key="timeseries_type"
>>>>>>> 53072bd5f3f5b260c38666b61d38106d103b1645
        )

        fichier = st.file_uploader("Importer un fichier CSV", type=["csv"], key="timeseries")
        if fichier:
            df = load_csv(fichier)
            st.write("Aperçu des données :")
            st.dataframe(df.head())
            
            if ts_type == "Série simple":
                run_simple(df)
                
            elif ts_type == "Séries multiples":
                fig = plot_time_series_multi(
                    df,
                    "Date",
                    ["Confirmed", "Deaths", "Recovered"],
                    title="COVID-19: Confirmed vs Deaths vs Recovered"
                )
                st.pyplot(fig)
                plt.close(fig)  # 🔥 FERME LA FIGURE

                run_multiple(df)
                
            elif ts_type == "🌿 Parcelle de Tiges":
                from modules.plots import stem
                stem.run(df)
        else:
            st.info("Veuillez importer un fichier CSV pour afficher les séries temporelles.")

    # === Visualisation thématique ===
    elif choix == "Visualisation":
        st.subheader("📈 Visualisation thématique")
        onglet = st.tabs(["Démographie", "Climat", "Finances", "Géographie", "🗺️ Treemap"])

        # --- Démographie ---
        with onglet[0]:
            st.write("📊 Analyses Démographiques")
            st.info("Pyramides des âges et analyses de population")
            
            fichier = st.file_uploader("Importer un dataset démographique", type=["csv"], key="demo")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                
                # Utiliser notre module pyramide amélioré
                from modules.plots import pyramid
                pyramid.run(df)

        # --- Climat ---
        with onglet[1]:
            st.write("🌡️ Analyses Climatiques")
            st.info("Évolution des températures et données environnementales")
            
            fichier = st.file_uploader("Importer un dataset climatique", type=["csv"], key="climat")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                
                # Détection automatique des colonnes climatiques
                temp_cols = [col for col in df.columns if any(x in col.lower() for x in ['temp', 'temperature', 'chaleur'])]
                precip_cols = [col for col in df.columns if any(x in col.lower() for x in ['precip', 'pluie', 'rain'])]
                date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time', 'année'])]
                
                if temp_cols and date_cols:
                    col1, col2 = st.columns(2)
                    with col1:
                        date_col = st.selectbox("Colonne date :", date_cols, key="climate_date")
                    with col2:
                        data_col = st.selectbox("Donnée à analyser :", temp_cols + precip_cols, key="climate_data")
                    
                    if st.button("🌡️ Analyser les données climatiques", key="climate_analyze"):
                        run_simple(df)
                else:
                    st.warning("Colonnes de date ou données climatiques introuvables.")

        # --- Finances ---
        with onglet[2]:
            st.write("💹 Graphiques financiers")
            st.info("Analyse de données financières et commerciales")
            
            fichier = st.file_uploader("Importer un dataset financier", type=["csv"], key="carsales")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())
                
                # Options d'analyse financière
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time', 'année', 'month'])]
                
                if numeric_cols:
                    st.subheader("📈 Options d'analyse")
                    
                    analysis_type = st.radio(
                        "Type d'analyse :",
                        ["Série temporelle", "Comparaison multiple", "Corrélations"],
                        key="finance_analysis"
                    )
                    
                    if analysis_type == "Série temporelle" and date_cols:
                        col1, col2 = st.columns(2)
                        with col1:
                            date_col = st.selectbox("Colonne date :", date_cols, key="finance_date")
                        with col2:
                            value_col = st.selectbox("Variable financière :", numeric_cols, key="finance_value")
                        
                        if st.button("💹 Analyser la série financière", key="finance_analyze"):
                            run_simple(df)
                    
                    elif analysis_type == "Comparaison multiple":
                        selected_cols = st.multiselect(
                            "Variables à comparer :",
                            numeric_cols,
                            default=numeric_cols[:min(3, len(numeric_cols))],
                            key="finance_multi"
                        )
                        
                        if selected_cols and st.button("📊 Comparer les variables", key="finance_compare"):
                            if date_cols:
                                run_multiple(df)
                            else:
                                # Graphique de comparaison sans date
                                fig, ax = plt.subplots(figsize=(10, 6))
                                df[selected_cols].plot(kind='bar', ax=ax)
                                ax.set_title("Comparaison des variables financières")
                                ax.set_ylabel("Valeurs")
                                plt.xticks(rotation=45)
                                plt.tight_layout()
                                st.pyplot(fig)
                                plt.close(fig)
                    
                    elif analysis_type == "Corrélations":
                        if len(numeric_cols) > 1:
                            st.subheader("📈 Matrice de Corrélation")
                            corr_matrix = df[numeric_cols].corr()
                            
                            fig, ax = plt.subplots(figsize=(10, 8))
                            im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
                            
                            # Ajouter les valeurs dans les cases
                            for i in range(len(numeric_cols)):
                                for j in range(len(numeric_cols)):
                                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                            ha="center", va="center", color="black", fontweight='bold')
                            
                            ax.set_xticks(range(len(numeric_cols)))
                            ax.set_yticks(range(len(numeric_cols)))
                            ax.set_xticklabels(numeric_cols, rotation=45)
                            ax.set_yticklabels(numeric_cols)
                            ax.set_title("Matrice de Corrélation des Variables Financières", fontweight='bold')
                            
                            plt.colorbar(im, ax=ax)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
                        else:
                            st.warning("Pas assez de colonnes numériques pour une analyse de corrélation")
                
                else:
                    st.warning("Aucune colonne numérique trouvée pour l'analyse financière.")

        # --- Géographie ---
        with onglet[3]:
            st.write("🗺️ Graphiques géographiques")
            
            # Instructions détaillées
            st.info("""
            **📋 Format requis pour la carte :**
            - `Country` : Noms de pays en **ANGLAIS** (ex: "France", "Germany", "United States")
            - `Value` : Valeurs numériques pour la couleur
            - Optionnel : Autres colonnes numériques ou catégorielles
            """)
            
            # Exemple de données
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
                
                # Vérification des colonnes
                country_cols = [col for col in df.columns if 'country' in col.lower() or 'pays' in col.lower()]
                value_cols = df.select_dtypes(include=['number']).columns.tolist()
                
                if country_cols and value_cols:
                    st.success("✅ Colonnes détectées avec succès !")
                    
                    # Sélection des colonnes
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
                    
                    # Options de la carte
                    st.subheader("🎨 Options de la carte")
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        color_scale = st.selectbox(
                            "Échelle de couleurs:",
                            ["Viridis", "Plasma", "Inferno", "Magma", "Blues", "Reds", "Greens"]
                        )
                    
                    with col4:
                        map_title = st.text_input("Titre de la carte:", "Carte thématique par pays")
                    
                    # Génération de la carte
                    if st.button("🗺️ Générer la carte", type="primary"):
                        try:
                            # Nettoyage des données
                            df_clean = df[[country_column, value_column]].dropna()
                            
                            # Création de la carte
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
                            
                            # Statistiques
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

        # --- Treemap ---
        with onglet[4]:
            st.write("🗺️ Treemap Hiérarchique")
            fichier = st.file_uploader("Importer un dataset hiérarchique", type=["csv"], key="treemap")
            if fichier:
                df = load_csv(fichier)
                st.dataframe(df.head())

                from modules.plots import treemap
                treemap.run(df)


                from modules.plots import treemap
                treemap.run(df)

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
                st.info("Veuillez importer un CSV avec une structure hiérarchique (ex: Continent > Pays > Ville > Population)")

    st.markdown("---")
    
    # === CARTE MANUEL COMPLET AVEC BOUTON INTÉGRÉ ===
    try:
        import base64
        
        # Chemin vers votre PDF
        pdf_path = "assets/manuel_visualisation_universelle.pdf"
        
        # Lire le PDF
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        # Encoder en base64
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        
        # Carte complète avec bouton intégré
        st.markdown(f"""
        <style>
        .manual-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .manual-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .manual-subtitle {{
            font-size: 16px;
            margin-bottom: 25px;
            opacity: 0.9;
        }}
        .manual-btn {{
            background: #FFD700 !important;
            color: black !important;
            padding: 15px 30px !important;
            text-decoration: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            display: inline-block !important;
            border: 2px solid #FFD700 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
            cursor: pointer;
        }}
        .manual-btn:hover {{
            background: #90EE90 !important;
            color: black !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
            border-color: #90EE90 !important;
        }}
        </style>
        
        <div class="manual-card">
            <div class="manual-title">📕 MANUEL COMPLET</div>
            <div class="manual-subtitle">Guide d'utilisation détaillé de l'application</div>
            <a href="data:application/pdf;base64,{b64_pdf}" 
            download="manuel_visualisation_universelle.pdf"
            class="manual-btn">
            ⬇️ TÉLÉCHARGER LE GUIDE
            </a>
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    padding: 30px; border-radius: 15px; color: white; text-align: center;
                    margin: 20px 0;'>
            <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>❌ MANUEL INDISPONIBLE</div>
            <div style='font-size: 16px;'>Fichier PDF non trouvé : assets/manuel_visualisation_universelle.pdf</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    padding: 30px; border-radius: 15px; color: white; text-align: center;
                    margin: 20px 0;'>
            <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>❌ ERREUR</div>
            <div style='font-size: 16px;'>Erreur lors du chargement : {str(e)}</div>
        </div>
        """, unsafe_allow_html=True)

    # === COPYRIGHT EN BAS ===
    st.markdown("---")
    
    # === VOTRE COPYRIGHT ===
    st.markdown(
        """
        <div style='text-align: center; margin-top: 40px; padding: 20px; 
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-radius: 10px; border-left: 5px solid #FFD700;'>
            <p style='font-size: 1.1em; color: #2c3e50; font-weight: bold; margin: 0;'>
                © 2025 Visualisation Universelle - Ossiny B.
            </p>
            <p style='font-size: 0.9em; color: #7f8c8d; margin: 5px 0 0 0;'>
                Tous droits réservés | Application de visualisation de données avancée
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

