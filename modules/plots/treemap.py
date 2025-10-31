
# modules/plots/treemap.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import squarify  # Pour la version matplotlib

def plot_treemap_plotly(df, path_columns, value_column, title="Treemap", color_column=None):
    """Version Plotly - Treemap interactif"""
    if color_column:
        fig = px.treemap(df, 
                        path=path_columns,
                        values=value_column,
                        color=color_column,
                        title=title,
                        color_continuous_scale='Viridis')
    else:
        fig = px.treemap(df, 
                        path=path_columns,
                        values=value_column,
                        title=title)
    
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def plot_treemap_matplotlib(df, path_columns, value_column, title="Treemap"):
    """Version Matplotlib - Treemap avec squarify"""
    # Préparer les données pour squarify
    if len(path_columns) == 1:
        # Une seule hiérarchie
        df_grouped = df.groupby(path_columns[0])[value_column].sum().reset_index()
        labels = [f"{row[path_columns[0]]}\n{row[value_column]:.0f}" 
                 for _, row in df_grouped.iterrows()]
        sizes = df_grouped[value_column].values
    else:
        # Hiérarchie multiple - on utilise le dernier niveau
        last_level = path_columns[-1]
        df_grouped = df.groupby(last_level)[value_column].sum().reset_index()
        labels = [f"{row[last_level]}\n{row[value_column]:.0f}" 
                 for _, row in df_grouped.iterrows()]
        sizes = df_grouped[value_column].values
    
    # Créer le treemap
    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=0.8, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axis('off')  # Enlever les axes
    
    plt.tight_layout()
    return fig

def plot_sunburst_plotly(df, path_columns, value_column, title="Sunburst"):
    """Sunburst - Alternative au treemap"""
    fig = px.sunburst(df, 
                     path=path_columns,
                     values=value_column,
                     title=title)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def prepare_treemap_data(df, theme):
    """Prépare les données selon le thème sélectionné"""
    if theme == "Géographie":
        # Structure typique : Continent > Pays > Ville > Valeur
        st.info("🌍 Structure recommandée: Continent > Pays > Ville > Population/Surface")
        return ["Continent", "Pays", "Ville"], "Population"
    
    elif theme == "Finances":
        # Structure typique : Département > Catégorie > Sous-catégorie > Budget
        st.info("💰 Structure recommandée: Département > Catégorie > Sous-catégorie > Budget")
        return ["Département", "Catégorie", "Sous-catégorie"], "Budget"
    
    elif theme == "Démographie":
        # Structure typique : Région > Ville > Quartier > Population
        st.info("👥 Structure recommandée: Région > Ville > Quartier > Population")
        return ["Région", "Ville", "Quartier"], "Population"
    
    elif theme == "Climat":
        # Structure typique : Continent > Pays > Type > Donnée climatique
        st.info("🌡️ Structure recommandée: Continent > Pays > Type > Émission/Consommation")
        return ["Continent", "Pays", "Type"], "Valeur"
    
    else:
        # Mode manuel
        return None, None

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("🗺️ Treemap - Visualisation Hiérarchique")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("""
    💡 **Le Treemap** visualise les données hiérarchiques par des rectangles :
    - 📐 **Surface** = Proportionnelle aux valeurs
    - 🎨 **Couleurs** = Peuvent représenter une autre dimension
    - 📊 **Hiérarchie** = Structure arborescente des données
    - 👁️ **Comparaisons** = Facile de comparer les proportions
    """)
    
    # Sélection du thème
    theme = st.selectbox(
        "Choisissez un thème ou mode manuel:",
        ["Mode Manuel", "Géographie", "Finances", "Démographie", "Climat"],
        key="treemap_theme"
    )
    
    if theme == "Mode Manuel":
        # Mode manuel - l'utilisateur choisit tout
        st.write("**Configuration manuelle des données:**")
        
        # Colonnes pour la hiérarchie
        st.subheader("📁 Structure Hiérarchique")
        st.write("Sélectionnez les colonnes dans l'ordre hiérarchique (du plus général au plus spécifique):")
        
        hierarchy_cols = st.multiselect(
            "Colonnes hiérarchiques (ordre important):",
            options=df.columns.tolist(),
            key="treemap_hierarchy"
        )
        
        # Colonne des valeurs
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        value_column = st.selectbox(
            "Colonne des valeurs (numérique):",
            options=numeric_columns,
            key="treemap_value"
        )
        
        # Colonne pour les couleurs (optionnelle)
        color_option = st.checkbox("Utiliser une colonne pour les couleurs", key="treemap_color_opt")
        color_column = None
        if color_option:
            color_column = st.selectbox(
                "Colonne pour les couleurs:",
                options=df.columns.tolist(),
                key="treemap_color"
            )
    
    else:
        # Mode thématique - suggestions automatiques
        suggested_hierarchy, suggested_value = prepare_treemap_data(df, theme)
        
        st.write(f"**Configuration pour le thème: {theme}**")
        
        # Hiérarchie
        st.subheader("📁 Structure Hiérarchique")
        hierarchy_cols = st.multiselect(
            "Colonnes hiérarchiques:",
            options=df.columns.tolist(),
            default=[col for col in suggested_hierarchy if col in df.columns],
            key="treemap_hierarchy"
        )
        
        # Valeurs
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        value_column = st.selectbox(
            "Colonne des valeurs:",
            options=numeric_columns,
            index=numeric_columns.index(suggested_value) if suggested_value in numeric_columns else 0,
            key="treemap_value"
        )
        
        # Couleurs
        color_option = st.checkbox("Utiliser une colonne pour les couleurs", key="treemap_color_opt")
        color_column = None
        if color_option:
            color_column = st.selectbox(
                "Colonne pour les couleurs:",
                options=df.columns.tolist(),
                key="treemap_color"
            )
    
    # Options de visualisation
    st.subheader("🎨 Options de Visualisation")
    col1, col2 = st.columns(2)
    
    with col1:
        chart_type = st.radio(
            "Type de visualisation:",
            ["Treemap", "Sunburst"],
            key="treemap_type"
        )
        
        chart_library = st.radio(
            "Bibliothèque:",
            ["Plotly (Interactif)", "Matplotlib"],
            key="treemap_lib"
        )
    
    with col2:
        title = st.text_input("Titre du graphique:", f"Treemap - {theme}", key="treemap_title")
        show_data = st.checkbox("Afficher les données préparées", value=True)
    
    # Génération du graphique
    if st.button("🗺️ Générer le Treemap", type="primary"):
        if not hierarchy_cols or not value_column:
            st.error("❌ Veuillez sélectionner au moins une colonne hiérarchique et une colonne de valeurs")
            return
        
        try:
            # Nettoyage des données
            cols_to_keep = hierarchy_cols + [value_column]
            if color_column:
                cols_to_keep.append(color_column)
            
            df_clean = df[cols_to_keep].dropna()
            
            if df_clean.empty:
                st.error("❌ Aucune donnée valide après nettoyage")
                return
            
            # Vérifier que la colonne des valeurs est numérique
            if not pd.api.types.is_numeric_dtype(df_clean[value_column]):
                st.error("❌ La colonne des valeurs doit être numérique")
                return
            
            # Génération du graphique
            if chart_library == "Plotly (Interactif)":
                if chart_type == "Treemap":
                    fig = plot_treemap_plotly(df_clean, hierarchy_cols, value_column, title, color_column)
                else:  # Sunburst
                    fig = plot_sunburst_plotly(df_clean, hierarchy_cols, value_column, title)
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:  # Matplotlib
                if chart_type == "Treemap":
                    fig = plot_treemap_matplotlib(df_clean, hierarchy_cols, value_column, title)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("❌ Sunburst non disponible avec Matplotlib. Utilisez Plotly.")
            
            # Données préparées
            if show_data:
                st.subheader("📊 Données Préparées")
                
                # Agrégation pour montrer la structure
                if len(hierarchy_cols) > 1:
                    aggregation = df_clean.groupby(hierarchy_cols)[value_column].agg(['sum', 'count']).reset_index()
                    aggregation.columns = hierarchy_cols + ['Total', 'Nombre d\'éléments']
                    st.dataframe(aggregation)
                else:
                    st.dataframe(df_clean)
                
                # Statistiques
                st.subheader("📈 Statistiques")
                col_stat1, col_stat2 = st.columns(2)
                
                with col_stat1:
                    st.write(f"**{value_column}:**")
                    stats = df_clean[value_column].describe()
                    st.dataframe(stats)
                
                with col_stat2:
                    st.write("**Structure:**")
                    st.write(f"Niveaux hiérarchiques: {len(hierarchy_cols)}")
                    st.write(f"Total des éléments: {len(df_clean)}")
                    st.write(f"Valeur totale: {df_clean[value_column].sum():.2f}")
            
            # Informations éducatives
            with st.expander("🎓 Guide d'Interprétation du Treemap"):
                st.markdown(f"""
                **Comment lire ce Treemap ({theme}):**
                
                📐 **Surfaces:** 
                - Plus grand = plus de {value_column.lower()}
                - Comparaison visuelle facile des proportions
                
                📁 **Hiérarchie:**
                - Niveaux: {' > '.join(hierarchy_cols)}
                - Cliquez pour zoomer (Plotly)
                
                💡 **Insights pour {theme}:**
                - Identifiez les plus gros contributeurs
                - Repérez les déséquilibres
                - Analysez la structure hiérarchique
                """)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")
            st.info("💡 Conseil: Vérifiez que votre structure hiérarchique est logique")

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Continent': ['Europe']*6 + ['Amérique']*4,
        'Pays': ['France', 'France', 'Allemagne', 'Allemagne', 'Italie', 'Italie', 
                'USA', 'USA', 'Canada', 'Canada'],
        'Ville': ['Paris', 'Lyon', 'Berlin', 'Munich', 'Rome', 'Milan',
                 'NYC', 'LA', 'Toronto', 'Vancouver'],
        'Population': [2000000, 500000, 3500000, 1500000, 2800000, 1300000,
                      8000000, 4000000, 2700000, 600000]
    })
    run(sample_data)