

# modules/plots/heatmap.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap_plotly(df, title="Carte Thermique"):
    """Version Plotly - Heatmap interactif"""
    fig = px.imshow(df,
                    title=title,
                    aspect="auto",
                    color_continuous_scale='Viridis',
                    labels=dict(x="Colonnes", y="Lignes", color="Valeur"))
    
    fig.update_layout(
        xaxis_title="Colonnes",
        yaxis_title="Lignes"
    )
    return fig

def plot_heatmap_matplotlib(df, title="Carte Thermique"):
    """Version Matplotlib - Heatmap classique"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Créer la heatmap
    im = ax.imshow(df.values, cmap='viridis', aspect='auto')
    
    # Configurer les axes
    ax.set_xticks(range(len(df.columns)))
    ax.set_yticks(range(len(df.index)))
    ax.set_xticklabels(df.columns, rotation=45, ha='right')
    ax.set_yticklabels(df.index)
    
    # Ajouter la barre de couleur
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Valeurs')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Ajouter les valeurs dans les cellules si le dataset n'est pas trop grand
    if len(df) <= 20 and len(df.columns) <= 10:
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                text = ax.text(j, i, f'{df.iloc[i, j]:.2f}',
                              ha="center", va="center", 
                              color="white" if df.iloc[i, j] > np.median(df.values) else "black",
                              fontsize=8)
    
    plt.tight_layout()
    return fig

def plot_correlation_heatmap(df, title="Matrice de Corrélation"):
    """Heatmap spécifique pour les matrices de corrélation"""
    # Calculer la matrice de corrélation
    corr_matrix = df.corr()
    
    fig = px.imshow(corr_matrix,
                    title=title,
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    labels=dict(x="Variables", y="Variables", color="Corrélation"))
    
    # Ajouter les valeurs de corrélation
    annotations = []
    for i, row in enumerate(corr_matrix.index):
        for j, col in enumerate(corr_matrix.columns):
            annotations.append(
                dict(
                    x=j, y=i,
                    text=f'{corr_matrix.iloc[i, j]:.2f}',
                    showarrow=False,
                    font=dict(color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black')
                )
            )
    
    fig.update_layout(annotations=annotations)
    return fig

def prepare_data_for_heatmap(df, x_col, y_col, value_col):
    """Prépare les données au format pivot pour heatmap"""
    if x_col and y_col and value_col:
        # Format pivot standard
        pivot_df = df.pivot_table(
            index=y_col, 
            columns=x_col, 
            values=value_col, 
            aggfunc='mean'
        )
        return pivot_df.fillna(0)
    else:
        # Utiliser directement les colonnes numériques
        return df.select_dtypes(include=['number'])

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("🔥 Carte Thermique")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("""
    💡 **La carte thermique** visualise les données à travers des couleurs :
    - 🎨 **Couleurs** = Intensité des valeurs
    - 📊 **Matrices** = Idéal pour les corrélations et données tabulaires
    - 🔍 **Patterns** = Identifie rapidement les tendances et anomalies
    """)
    
    # Sélection du type de heatmap
    heatmap_type = st.radio(
        "Type de carte thermique:",
        ["Heatmap Standard", "Matrice de Corrélation"],
        key="heatmap_type"
    )
    
    if heatmap_type == "Heatmap Standard":
        st.write("**Configuration des données:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Colonne pour les lignes
            all_columns = df.columns.tolist()
            y_column = st.selectbox(
                "Colonne pour les lignes (Y):",
                options=[''] + all_columns,
                key="heatmap_y"
            )
        
        with col2:
            # Colonne pour les colonnes
            x_column = st.selectbox(
                "Colonne pour les colonnes (X):",
                options=[''] + all_columns,
                key="heatmap_x"
            )
        
        with col3:
            # Colonne pour les valeurs
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            value_column = st.selectbox(
                "Colonne des valeurs:",
                options=[''] + numeric_columns,
                key="heatmap_value"
            )
        
        # Si pas de configuration spécifique, utiliser toutes les colonnes numériques
        use_numeric_only = not (x_column and y_column and value_column)
        
        if use_numeric_only:
            st.info("ℹ️ Utilisation automatique de toutes les colonnes numériques")
    
    # Options d'affichage
    col4, col5 = st.columns(2)
    
    with col4:
        chart_library = st.radio(
            "Bibliothèque de visualisation:",
            ["Plotly (Interactif)", "Matplotlib"],
            key="heatmap_lib"
        )
    
    with col5:
        title = st.text_input("Titre du graphique:", 
                             "Matrice de Corrélation" if heatmap_type == "Matrice de Corrélation" else "Carte Thermique", 
                             key="heatmap_title")
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        normalize_data = st.checkbox("Normaliser les données (Z-score)", value=False)
        show_values = st.checkbox("Afficher les valeurs dans les cellules", value=True)
        color_scheme = st.selectbox(
            "Schéma de couleurs:",
            ["Viridis", "Plasma", "Inferno", "Magma", "RdBu", "Blues"],
            key="heatmap_colors"
        )
    
    # Génération du graphique
    if st.button("🔥 Générer la Carte Thermique", type="primary"):
        try:
            if heatmap_type == "Matrice de Corrélation":
                # Heatmap de corrélation
                numeric_df = df.select_dtypes(include=['number'])
                
                if numeric_df.empty:
                    st.error("❌ Aucune colonne numérique trouvée pour la matrice de corrélation")
                    return
                
                if len(numeric_df.columns) < 2:
                    st.error("❌ Au moins 2 colonnes numériques sont nécessaires pour la corrélation")
                    return
                
                fig = plot_correlation_heatmap(numeric_df, title)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques de corrélation
                st.subheader("📊 Matrice de Corrélation Numérique")
                corr_matrix = numeric_df.corr()
                st.dataframe(corr_matrix.style.background_gradient(cmap='viridis'))
                
            else:
                # Heatmap standard
                if use_numeric_only:
                    # Utiliser toutes les colonnes numériques
                    data_for_heatmap = df.select_dtypes(include=['number'])
                    if data_for_heatmap.empty:
                        st.error("❌ Aucune colonne numérique trouvée")
                        return
                else:
                    # Utiliser le format pivot
                    if not all([x_column, y_column, value_column]):
                        st.error("❌ Veuillez sélectionner les trois colonnes ou utiliser le mode automatique")
                        return
                    
                    data_for_heatmap = prepare_data_for_heatmap(df, x_column, y_column, value_column)
                
                # Normalisation si demandée
                if normalize_data:
                    data_for_heatmap = (data_for_heatmap - data_for_heatmap.mean()) / data_for_heatmap.std()
                
                if data_for_heatmap.empty:
                    st.error("❌ Aucune donnée valide pour la heatmap")
                    return
                
                # Génération du graphique
                if chart_library == "Plotly (Interactif)":
                    fig = plot_heatmap_plotly(data_for_heatmap, title)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = plot_heatmap_matplotlib(data_for_heatmap, title)
                    st.pyplot(fig)
                    plt.close(fig)
                
                # Informations sur les données
                st.subheader("📋 Données de la Heatmap")
                st.dataframe(data_for_heatmap)
                
                # Téléchargement des données
                csv = data_for_heatmap.to_csv()
                st.download_button(
                    label="💾 Télécharger les données (CSV)",
                    data=csv,
                    file_name="heatmap_data.csv",
                    mime="text/csv"
                )
            
            # Informations éducatives
            with st.expander("🎓 Comprendre les Cartes Thermiques"):
                st.markdown("""
                **Interprétation :**
                - 🔴 **Rouge/Chaud** = Valeurs élevées
                - 🔵 **Bleu/Froid** = Valeurs faibles
                - 📈 **Patterns** = Cherchez les clusters et gradients
                
                **Cas d'usage :**
                - Matrices de corrélation
                - Données de performance
                - Analyses temporelles
                - Données géospatiales
                """)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")
            st.info("💡 Conseil: Vérifiez que vos données sont numériques ou que le format pivot est possible")

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Mois': ['Jan', 'Jan', 'Fév', 'Fév', 'Mar', 'Mar'],
        'Produit': ['A', 'B', 'A', 'B', 'A', 'B'],
        'Ventes': [100, 150, 120, 130, 110, 160],
        'Profit': [20, 30, 25, 28, 22, 35]
    })
    run(sample_data)