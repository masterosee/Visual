
# modules/plots/pyramid.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run(df):
    st.subheader("📐 Pyramide des Âges")
    
    # Instructions adaptées à n'importe quel dataset
    st.info("""
    **Configuration requise :**
    - Une colonne **numérique** pour l'âge (ex: 'Age', 'Âge', 'age')
    - Une colonne **catégorielle** pour le genre (ex: 'Gender', 'Sexe', 'Genre', 'Sex')
    """)
    
    # Détection automatique des colonnes potentielles
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Colonnes d'âge potentielles (avec priorité pour les noms évidents)
    age_candidates = []
    for col in df.columns:
        col_lower = col.lower()
        if any(age_word in col_lower for age_word in ['age', 'âge']):
            age_candidates.insert(0, col)  # Priorité
        elif col in numeric_cols:
            age_candidates.append(col)
    
    # Colonnes de genre potentielles
    gender_candidates = []
    for col in df.columns:
        col_lower = col.lower()
        if any(gender_word in col_lower for gender_word in ['gender', 'sexe', 'genre', 'sex']):
            gender_candidates.insert(0, col)  # Priorité
        elif col in text_cols and df[col].nunique() <= 5:  # Peu de valeurs uniques = potentiellement genre
            gender_candidates.append(col)
    
    # Si pas de candidats évidents, utiliser toutes les colonnes
    if not age_candidates and numeric_cols:
        age_candidates = numeric_cols
    if not gender_candidates and text_cols:
        gender_candidates = text_cols
    
    # Sélection des colonnes avec valeurs par défaut intelligentes
    col1, col2 = st.columns(2)
    
    with col1:
        age_col = st.selectbox(
            "Colonne des âges :", 
            options=age_candidates if age_candidates else df.columns.tolist(),
            index=0 if age_candidates else 0,
            help="Choisissez une colonne numérique contenant les âges"
        )
    
    with col2:
        gender_col = st.selectbox(
            "Colonne du genre :",
            options=gender_candidates if gender_candidates else df.columns.tolist(),
            index=0 if gender_candidates else 0,
            help="Choisissez une colonne avec les genres (ex: M/F, Homme/Femme, Male/Female)"
        )
    
    if age_col and gender_col:
        try:
            # Vérification des données
            st.write(f"**Colonne âge sélectionnée :** {age_col}")
            st.write(f"**Colonne genre sélectionnée :** {gender_col}")
            
            # Aperçu des valeurs uniques pour le genre
            unique_genders = df[gender_col].astype(str).unique()
            st.write(f"**Valeurs de genre détectées :** {', '.join(unique_genders)}")
            
            # Options de mapping flexible
            st.subheader("🔧 Configuration des genres")
            st.write("Associez chaque valeur à 'Homme' ou 'Femme' :")
            
            gender_mapping = {}
            for gender_val in unique_genders:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"`{gender_val}` →")
                with col_b:
                    mapped_val = st.selectbox(
                        f"Mapping pour {gender_val}",
                        ["Homme", "Femme", "Ignorer"],
                        key=f"map_{gender_val}"
                    )
                    if mapped_val != "Ignorer":
                        gender_mapping[gender_val.lower()] = mapped_val
            
            # Options d'affichage
            st.subheader("🎨 Personnalisation")
            
            col3, col4 = st.columns(2)
            with col3:
                bin_size = st.slider("Tranche d'âge (années) :", 1, 10, 5)
                max_age = st.number_input("Âge maximum :", min_value=10, max_value=120, value=80)
            
            with col4:
                color_male = st.color_picker("Couleur Hommes", "#1f77b4")
                color_female = st.color_picker("Couleur Femmes", "#ff7f0e")
            
            # Génération
            if st.button("📈 Générer la Pyramide", type="primary"):
                if not gender_mapping:
                    st.error("❌ Veuillez configurer le mapping des genres")
                else:
                    create_age_pyramid(df, age_col, gender_col, gender_mapping,
                                     bin_size, max_age, color_male, color_female)
                
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {str(e)}")
            st.info("💡 Vérifiez que vos colonnes contiennent des données valides")
    else:
        st.warning("⚠️ Sélectionnez les colonnes âge et genre pour continuer")

def create_age_pyramid(df, age_col, gender_col, gender_mapping, bin_size, max_age, color_male, color_female):
    """Crée une pyramide des âges adaptative"""
    
    # Nettoyage et préparation
    df_clean = df[[age_col, gender_col]].copy()
    df_clean[age_col] = pd.to_numeric(df_clean[age_col], errors='coerce')
    df_clean = df_clean.dropna()
    df_clean = df_clean[df_clean[age_col] <= max_age]
    
    # Application du mapping genre
    df_clean['gender_mapped'] = df_clean[gender_col].astype(str).str.lower().map(gender_mapping)
    df_clean = df_clean.dropna(subset=['gender_mapped'])
    
    if df_clean.empty:
        st.error("❌ Aucune donnée valide après le mapping des genres")
        return
    
    # Création des groupes d'âge
    df_clean['age_group'] = (df_clean[age_col] // bin_size) * bin_size
    
    # Agrégation
    pyramid_data = df_clean.groupby(['age_group', 'gender_mapped']).size().unstack(fill_value=0)
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 8))
    
    age_groups = pyramid_data.index
    
    # Hommes (gauche)
    if 'Homme' in pyramid_data.columns:
        male_data = -pyramid_data['Homme']
        ax.barh(age_groups, male_data, bin_size*0.8, 
                color=color_male, alpha=0.8, label='Hommes', edgecolor='white')
    
    # Femmes (droite)
    if 'Femme' in pyramid_data.columns:
        female_data = pyramid_data['Femme']
        ax.barh(age_groups, female_data, bin_size*0.8,
                color=color_female, alpha=0.8, label='Femmes', edgecolor='white')
    
    # Personnalisation
    ax.set_xlabel('Population', fontsize=12)
    ax.set_ylabel('Âge', fontsize=12)
    ax.set_title('Pyramide des Âges', fontsize=14, fontweight='bold')
    
    # Configuration des axes
    x_max = max(pyramid_data.max().max() if not pyramid_data.empty else 10, 10)
    ax.set_xlim(-x_max, x_max)
    
    x_ticks = np.arange(-x_max, x_max + 1, x_max // 5)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(abs(int(x))) for x in x_ticks])
    
    ax.axvline(0, color='black', linewidth=0.8)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)  # 🔥 FERME LA FIGURE POUR ÉVITER LES CONFLITS
    
    # Statistiques
    show_pyramid_stats(df_clean, age_col)

def show_pyramid_stats(df, age_col):
    """Affiche les statistiques adaptatives"""
    st.subheader("📊 Statistiques démographiques")
    
    total_pop = len(df)
    male_count = (df['gender_mapped'] == 'Homme').sum()
    female_count = (df['gender_mapped'] == 'Femme').sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Population analysée", total_pop)
    
    with col2:
        if male_count > 0:
            male_pct = (male_count / total_pop) * 100
            st.metric("Hommes", f"{male_count} ({male_pct:.1f}%)")
        else:
            st.metric("Hommes", "0")
    
    with col3:
        if female_count > 0:
            female_pct = (female_count / total_pop) * 100
            st.metric("Femmes", f"{female_count} ({female_pct:.1f}%)")
        else:
            st.metric("Femmes", "0")
    
    # Âges moyens
    if male_count > 0:
        avg_age_male = df[df['gender_mapped'] == 'Homme'][age_col].mean()
        st.write(f"**Âge moyen Hommes :** {avg_age_male:.1f} ans")
    
    if female_count > 0:
        avg_age_female = df[df['gender_mapped'] == 'Femme'][age_col].mean()
        st.write(f"**Âge moyen Femmes :** {avg_age_female:.1f} ans")