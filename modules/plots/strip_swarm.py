
# modules/plots/strip_swarm.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def plot_strip_plot(df, x_col, y_col, title="Strip Plot", jitter=True):
    """Strip Plot - Points dispersés avec jitter"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Créer le strip plot manuellement avec jitter
    categories = df[x_col].unique()
    
    for i, category in enumerate(categories):
        category_data = df[df[x_col] == category][y_col].dropna()
        
        if not category_data.empty:
            # Ajouter du jitter aléatoire sur l'axe X
            x_pos = np.random.normal(i, 0.1, len(category_data))
            ax.scatter(x_pos, category_data, alpha=0.6, s=50, label=category)
    
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_swarm_plot(df, x_col, y_col, title="Swarm Plot"):
    """Swarm Plot - Points empilés sans chevauchement (version manuelle)"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    categories = df[x_col].unique()
    
    for i, category in enumerate(categories):
        category_data = df[df[x_col] == category][y_col].dropna().sort_values()
        
        if not category_data.empty:
            # Algorithme simple pour éviter les chevauchements
            x_positions = []
            for j, value in enumerate(category_data):
                # Position de base
                base_x = i
                # Petit décalage pour éviter les chevauchements
                offset = (j % 3 - 1) * 0.15
                x_positions.append(base_x + offset)
            
            ax.scatter(x_positions, category_data, alpha=0.6, s=40, label=category)
    
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_strip_swarm_plotly(df, x_col, y_col, title="Strip/Swarm Plot", plot_type="strip"):
    """Version Plotly - Strip/Swarm Plot interactif"""
    if plot_type == "strip":
        fig = px.strip(df, x=x_col, y=y_col, title=title, color=x_col)
    else:
        # Pour swarm plot avec Plotly, on utilise strip avec ajustement
        fig = px.strip(df, x=x_col, y=y_col, title=title, color=x_col)
        fig.update_traces(jitter=0.3)  # Plus de jitter pour ressembler à swarm
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True
    )
    return fig

def plot_comparison_strip_swarm(df, x_col, y_columns, title="Comparaison Strip/Swarm"):
    """Comparaison multiple avec strip/swarm plots"""
    # Préparer les données au format long
    df_melted = df.melt(id_vars=[x_col], value_vars=y_columns, 
                        var_name='Variable', value_name='Valeur')
    
    fig = px.strip(df_melted, x=x_col, y='Valeur', color='Variable',
                  title=title, facet_col='Variable', facet_col_wrap=2)
    
    fig.update_layout(showlegend=True)
    return fig

def plot_violin_strip_combo(df, x_col, y_col, title="Violin + Strip Plot"):
    """Combinaison Violin Plot + Strip Plot"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Violin plot
    categories = df[x_col].unique()
    data_by_category = [df[df[x_col] == cat][y_col].dropna() for cat in categories]
    
    parts = ax.violinplot(data_by_category, showmeans=False, showmedians=True)
    
    # Personnaliser les violons
    for pc in parts['bodies']:
        pc.set_facecolor('#1f77b4')
        pc.set_alpha(0.3)
    
    # Strip plot superposé
    for i, category in enumerate(categories):
        category_data = df[df[x_col] == category][y_col].dropna()
        if not category_data.empty:
            x_pos = np.random.normal(i+1, 0.1, len(category_data))
            ax.scatter(x_pos, category_data, alpha=0.6, s=30, color='red', edgecolors='black', linewidth=0.5)
    
    ax.set_xticks(range(1, len(categories) + 1))
    ax.set_xticklabels(categories)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def run(df):
    """Fonction principale pour Streamlit - CORRIGÉE"""
    st.subheader("🐝 Bandes & Essaims")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("""
    💡 **Bandes (Strip) & Essaims (Swarm) Plots** :
    - 📍 **Strip Plot** = Points dispersés avec jitter pour éviter les chevauchements
    - 🐝 **Swarm Plot** = Points empilés intelligemment sans chevauchement
    - 👁️ **Visualisation des points** = Montre chaque observation individuelle
    - 📊 **Distribution + Points** = Meilleure que les boxplots seuls
    """)
    
    # Sélection du type de plot
    plot_type = st.radio(
        "Type de visualisation:",
        ["Strip Plot", "Swarm Plot", "Strip/Swarm Multiple", "Violin + Strip Combo"],
        key="strip_swarm_type"
    )
    
    # Sélection des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Colonne catégorielle pour l'axe X
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if not categorical_columns:
            categorical_columns = df.columns.tolist()
        
        x_column = st.selectbox(
            "Colonne catégorielle (axe X):",
            options=categorical_columns,
            key="strip_x"
        )
    
    with col2:
        if plot_type == "Strip/Swarm Multiple":
            # Multiples colonnes numériques
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            y_columns = st.multiselect(
                "Variables numériques à comparer:",
                options=numeric_columns,
                default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns,
                key="strip_multi_y"
            )
        else:
            # Une seule colonne numérique
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            y_column = st.selectbox(
                "Colonne numérique (axe Y):",
                options=numeric_columns,
                key="strip_y"
            )
    
    # Options d'affichage
    col3, col4 = st.columns(2)
    
    with col3:
        chart_library = st.radio(
            "Bibliothèque de visualisation:",
            ["Matplotlib", "Plotly (Interactif)"],
            key="strip_lib"
        )
    
    with col4:
        title = st.text_input("Titre du graphique:", 
                             f"{plot_type}", 
                             key="strip_title")
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        show_stats = st.checkbox("Afficher les statistiques", value=True)
        show_data_points = st.checkbox("Afficher le nombre de points", value=True)
        
        if plot_type in ["Strip Plot", "Swarm Plot"]:
            point_size = st.slider("Taille des points:", 1, 10, 4)
            point_alpha = st.slider("Transparence des points:", 0.1, 1.0, 0.6)
    
    # Génération du graphique
    if st.button("🐝 Générer le Graphique", type="primary"):
        if plot_type == "Strip/Swarm Multiple":
            if not x_column or len(y_columns) < 1:
                st.error("❌ Veuillez sélectionner une colonne X et au moins une colonne Y")
                return
        else:
            if not x_column or not y_column:
                st.error("❌ Veuillez sélectionner les colonnes X et Y")
                return
        
        try:
            if plot_type == "Strip/Swarm Multiple":
                # Nettoyage des données
                cols_to_keep = [x_column] + y_columns
                df_clean = df[cols_to_keep].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique multiple
                if chart_library == "Plotly (Interactif)":
                    fig = plot_comparison_strip_swarm(df_clean, x_column, y_columns, title)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Pour matplotlib, créer une grille de subplots
                    n_plots = len(y_columns)
                    n_cols = min(2, n_plots)
                    n_rows = (n_plots + n_cols - 1) // n_cols
                    
                    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
                    if n_plots == 1:
                        axes = [axes]
                    else:
                        axes = axes.flatten()
                    
                    for i, y_col in enumerate(y_columns):
                        if i < len(axes):
                            categories = df_clean[x_column].unique()
                            
                            for j, category in enumerate(categories):
                                category_data = df_clean[df_clean[x_column] == category][y_col].dropna()
                                if not category_data.empty:
                                    x_pos = np.random.normal(j, 0.1, len(category_data))
                                    axes[i].scatter(x_pos, category_data, alpha=0.6, s=30, label=category)
                            
                            axes[i].set_xticks(range(len(categories)))
                            axes[i].set_xticklabels(categories, rotation=45)
                            axes[i].set_xlabel(x_column)
                            axes[i].set_ylabel(y_col)
                            axes[i].set_title(f"{y_col}")
                            axes[i].grid(True, alpha=0.3)
                            if i == 0:
                                axes[i].legend()
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                
            else:
                # Nettoyage des données
                df_clean = df[[x_column, y_column]].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique simple
                if chart_library == "Plotly (Interactif)":
                    plot_type_plotly = "strip" if plot_type == "Strip Plot" else "swarm"
                    fig = plot_strip_swarm_plotly(df_clean, x_column, y_column, title, plot_type_plotly)
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    if plot_type == "Strip Plot":
                        fig = plot_strip_plot(df_clean, x_column, y_column, title)
                    elif plot_type == "Swarm Plot":
                        fig = plot_swarm_plot(df_clean, x_column, y_column, title)
                    else:  # Violin + Strip Combo
                        fig = plot_violin_strip_combo(df_clean, x_column, y_column, title)
                    
                    st.pyplot(fig)
                    plt.close(fig)
            
            # Statistiques
            if show_stats:
                st.subheader("📊 Statistiques par Catégorie")
                
                if plot_type == "Strip/Swarm Multiple":
                    for y_col in y_columns:
                        st.write(f"**{y_col}:**")
                        stats = df_clean.groupby(x_column)[y_col].describe()
                        st.dataframe(stats)
                else:
                    stats = df_clean.groupby(x_column)[y_column].describe()
                    st.dataframe(stats)
            
            # Informations sur les points de données
            if show_data_points:
                st.subheader("🔢 Informations sur les Points")
                if plot_type == "Strip/Swarm Multiple":
                    total_points = len(df_clean)
                    st.write(f"**Total des points:** {total_points}")
                    for y_col in y_columns:
                        non_null = df_clean[y_col].count()
                        st.write(f"- {y_col}: {non_null} points valides")
                else:
                    category_counts = df_clean[x_column].value_counts()
                    st.write("**Points par catégorie:**")
                    for category, count in category_counts.items():
                        st.write(f"- {category}: {count} points")
            
            # Informations éducatives
            with st.expander("🎓 Comprendre les Bandes & Essaims"):
                st.markdown("""
                **Différence entre Strip et Swarm Plots:**
                
                **Strip Plot:**
                - 📍 Points dispersés aléatoirement (jitter)
                - ⚡ Rapide à générer
                - 🔍 Peut avoir des chevauchements
                - 📊 Bon pour les grands datasets
                
                **Swarm Plot:**
                - 🐝 Points empilés intelligemment
                - 🎯 Aucun chevauchement
                - ⏱️ Plus lent pour grands datasets
                - 👁️ Meilleure visualisation de la densité
                
                **Cas d'usage:**
                - Comparaison de distributions entre catégories
                - Détection d'outliers
                - Visualisation de petits à moyens datasets
                - Alternative aux boxplots/violins
                """)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")
            st.info("💡 Conseil: Vérifiez que vos données catégorielles ne sont pas trop nombreuses")

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Groupe': ['A']*20 + ['B']*20 + ['C']*20,
        'Valeur1': np.concatenate([
            np.random.normal(10, 2, 20),
            np.random.normal(15, 3, 20), 
            np.random.normal(12, 1.5, 20)
        ]),
        'Valeur2': np.concatenate([
            np.random.normal(20, 4, 20),
            np.random.normal(18, 2, 20),
            np.random.normal(22, 3, 20)
        ])
    })
    run(sample_data)