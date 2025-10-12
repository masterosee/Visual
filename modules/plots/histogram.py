
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def run(df):
    st.subheader("📊 Histogramme")
    
    # Instructions
    st.info("Visualisez la distribution d'une variable numérique")
    
    # Colonnes numériques
    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) == 0:
        st.error("❌ Aucune colonne numérique trouvée dans le dataset.")
        return

    colonne = st.selectbox("Choisissez une colonne :", colonnes_numeriques)
    
    # Options avancées
    st.subheader("🎨 Personnalisation")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bins = st.slider("Nombre de barres :", 5, 100, 20)
    
    with col2:
        color = st.color_picker("Couleur des barres", "#1f77b4")
    
    with col3:
        show_stats = st.checkbox("Afficher les statistiques", value=True)
    
    # Tracer l'histogramme
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Nettoyage des données
    data = df[colonne].dropna()
    
    # Histogramme
    n, bins, patches = ax.hist(data, bins=bins, color=color, alpha=0.7, 
                              edgecolor='black', linewidth=0.5)
    
    ax.set_title(f"Histogramme de {colonne}", fontsize=14, fontweight='bold')
    ax.set_xlabel(colonne, fontsize=12)
    ax.set_ylabel("Fréquence", fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Statistiques
    if show_stats and len(data) > 0:
        stats_text = f"""Moyenne: {data.mean():.2f}
Médiane: {data.median():.2f}
Écart-type: {data.std():.2f}
Effectif: {len(data)}"""
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontfamily='monospace')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)