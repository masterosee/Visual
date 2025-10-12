
# modules/plots/violin.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def plot_violin_plotly(df, x_col, y_col, title="Diagramme Violon"):
    """Version Plotly - Violin Plot interactif"""
    fig = px.violin(df, x=x_col, y=y_col, 
                    title=title,
                    box=True,  # Affiche la boîte à moustaches à l'intérieur
                    points="all",  # Affiche tous les points de données
                    color=x_col,
                    hover_data=df.columns)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=False
    )
    return fig

def plot_violin_seaborn(df, x_col, y_col, title="Diagramme Violon"):
    """Version Seaborn/Matplotlib - Violin Plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, inner="box", palette="Set2")
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    
    # Rotation des labels x si trop longs
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_violin_comparison(df, x_col, y_columns, title="Comparaison Violon Multiple"):
    """Version pour comparer plusieurs variables numériques"""
    # Préparer les données pour Plotly (format long)
    df_melted = df.melt(id_vars=[x_col], value_vars=y_columns, 
                        var_name='Variable', value_name='Valeur')
    
    fig = px.violin(df_melted, x=x_col, y='Valeur', color='Variable',
                    title=title, box=True, points=False,
                    facet_col='Variable', facet_col_wrap=2)
    
    fig.update_layout(showlegend=True)
    return fig

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("🎯 Diagramme Violon")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("""
    💡 **Le diagramme violon** combine :
    - 📊 **Box plot** (boîte à moustaches) 
    - 📈 **Densité de probabilité** (forme du violon)
    - 👁️ **Visualisation de la distribution** complète des données
    """)
    
    # Sélection du type de violon plot
    plot_type = st.radio(
        "Type de visualisation violon:",
        ["Violon Simple", "Violon Multiple (Comparaison)"],
        key="violon_type"
    )
    
    if plot_type == "Violon Simple":
        # Violon simple : une variable catégorielle vs une variable numérique
        col1, col2 = st.columns(2)
        
        with col1:
            # Colonne catégorielle pour l'axe X
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
            if not categorical_columns:
                categorical_columns = df.columns.tolist()  # Fallback sur toutes les colonnes
            
            x_column = st.selectbox(
                "Colonne catégorielle (axe X):",
                options=categorical_columns,
                key="violon_x"
            )
        
        with col2:
            # Colonne numérique pour l'axe Y
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            y_column = st.selectbox(
                "Colonne numérique (axe Y):",
                options=numeric_columns,
                key="violon_y"
            )
    
    else:  # Violon Multiple
        st.write("**Sélection des variables à comparer:**")
        
        # Colonne catégorielle pour grouper
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if not categorical_columns:
            categorical_columns = df.columns.tolist()
        
        x_column = st.selectbox(
            "Colonne pour grouper les données:",
            options=categorical_columns,
            key="violon_multi_x"
        )
        
        # Variables numériques à comparer
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        y_columns = st.multiselect(
            "Variables numériques à comparer:",
            options=numeric_columns,
            default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns,
            key="violon_multi_y"
        )
    
    # Options d'affichage
    col3, col4 = st.columns(2)
    
    with col3:
        chart_library = st.radio(
            "Bibliothèque de visualisation:",
            ["Plotly (Interactif)", "Seaborn/Matplotlib"],
            key="violon_lib"
        )
    
    with col4:
        title = st.text_input("Titre du graphique:", "Diagramme Violon", key="violon_title")
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        show_stats = st.checkbox("Afficher les statistiques descriptives", value=True)
        show_points = st.checkbox("Afficher les points de données", value=False)
    
    # Génération du graphique
    if st.button("🎯 Générer le Diagramme Violon", type="primary"):
        if plot_type == "Violon Simple":
            if not x_column or not y_column:
                st.error("❌ Veuillez sélectionner les colonnes X et Y")
                return
            
            try:
                # Nettoyage des données
                df_clean = df[[x_column, y_column]].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique
                if chart_library == "Plotly (Interactif)":
                    fig = plot_violin_plotly(df_clean, x_column, y_column, title)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = plot_violin_seaborn(df_clean, x_column, y_column, title)
                    st.pyplot(fig)
                    plt.close(fig)
                
                # Statistiques descriptives
                if show_stats:
                    st.subheader("📊 Statistiques Descriptives")
                    stats = df_clean.groupby(x_column)[y_column].describe()
                    st.dataframe(stats)
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
        
        else:  # Violon Multiple
            if not x_column or len(y_columns) < 2:
                st.error("❌ Veuillez sélectionner une colonne de groupe et au moins 2 variables numériques")
                return
            
            try:
                # Nettoyage des données
                cols_to_keep = [x_column] + y_columns
                df_clean = df[cols_to_keep].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique
                fig = plot_violin_comparison(df_clean, x_column, y_columns, title)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques comparatives
                if show_stats:
                    st.subheader("📊 Statistiques Comparatives")
                    for y_col in y_columns:
                        st.write(f"**{y_col}:**")
                        stats = df_clean.groupby(x_column)[y_col].describe()
                        st.dataframe(stats)
                        
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
        
        # Informations éducatives
        with st.expander("🎓 Comprendre le Diagramme Violon"):
            st.markdown("""
            **Comment interpréter un violon plot :**
            - 📏 **Largeur** = Fréquence des données à cette valeur
            - 📦 **Boîte blanche** = Quartiles (comme un box plot)
            - ● **Points** = Données individuelles (si activé)
            - 🎻 **Forme générale** = Distribution complète des données
            
            **Avantages :**
            - Montre la densité de probabilité
            - Compare plusieurs distributions
            - Identifie les multimodalities
            """)

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Category': ['A']*30 + ['B']*30 + ['C']*30,
        'Value1': np.concatenate([
            np.random.normal(10, 2, 30),
            np.random.normal(15, 3, 30), 
            np.random.normal(12, 1.5, 30)
        ]),
        'Value2': np.concatenate([
            np.random.normal(20, 4, 30),
            np.random.normal(18, 2, 30),
            np.random.normal(22, 3, 30)
        ])
    })
    run(sample_data)