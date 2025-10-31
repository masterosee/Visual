
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def run(df):
    st.subheader("☁️ Nuage de points")
    
    st.info("Explorez la relation entre deux variables numériques")

    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) < 2:
        st.error("❌ Il faut au moins deux colonnes numériques.")
        return

    # Sélection des variables
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("Colonne pour l'axe X :", colonnes_numeriques, key="scatter_x")
    
    with col2:
        y_col = st.selectbox("Colonne pour l'axe Y :", colonnes_numeriques, key="scatter_y")
    
    # Options avancées
    st.subheader("🎨 Personnalisation")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        color = st.color_picker("Couleur des points", "#1f77b4")
        alpha = st.slider("Transparence", 0.1, 1.0, 0.6)
    
    with col4:
        size = st.slider("Taille des points", 1, 100, 20)
        show_regression = st.checkbox("Ligne de régression")
    
    with col5:
        color_by = st.selectbox("Colorer par :", ["Aucun"] + list(df.select_dtypes(include=['object']).columns))
    
    # Préparation des données
    scatter_data = df[[x_col, y_col]].dropna()
    
    if color_by != "Aucun" and color_by in df.columns:
        scatter_data[color_by] = df[color_by]
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if color_by != "Aucun" and color_by in scatter_data.columns:
        # Scatter plot avec coloration catégorielle
        categories = scatter_data[color_by].unique()
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        for i, category in enumerate(categories):
            category_data = scatter_data[scatter_data[color_by] == category]
            ax.scatter(category_data[x_col], category_data[y_col], 
            c=[colors[i]], alpha=alpha, s=size, label=str(category))
        
        ax.legend(title=color_by)
    else:
        # Scatter plot simple
        ax.scatter(scatter_data[x_col], scatter_data[y_col], 
        alpha=alpha, color=color, s=size)
    
    # Ligne de régression
    if show_regression and len(scatter_data) > 1:
        z = np.polyfit(scatter_data[x_col], scatter_data[y_col], 1)
        p = np.poly1d(z)
        ax.plot(scatter_data[x_col], p(scatter_data[x_col]), "r--", alpha=0.8, linewidth=2)
        
        # Calcul du coefficient de corrélation
        correlation = scatter_data[x_col].corr(scatter_data[y_col])
        ax.text(0.05, 0.95, f'r = {correlation:.2f}', transform=ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=12)

    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(f"Nuage de points : {x_col} vs {y_col}", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Statistiques de corrélation
    if len(scatter_data) > 1:
        correlation = scatter_data[x_col].corr(scatter_data[y_col])
        st.metric("Coefficient de corrélation", f"{correlation:.3f}")