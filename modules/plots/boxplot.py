
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def run(df):
    st.subheader("📦 Box Plot")
    
    st.info("Visualisez la distribution et les valeurs aberrantes")

    # Colonnes numériques
    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) == 0:
        st.error("❌ Aucune colonne numérique trouvée.")
        return

    # Options
    col1, col2 = st.columns(2)
    
    with col1:
        colonne = st.selectbox("Choisissez une colonne :", colonnes_numeriques)
    
    with col2:
        orientation = st.radio("Orientation :", ["Vertical", "Horizontal"])
    
    # Tracer le boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = df[colonne].dropna()
    
    if orientation == "Vertical":
        box_plot = ax.boxplot(data, vert=True, patch_artist=True, 
                             boxprops=dict(facecolor='lightblue', alpha=0.7),
                             flierprops=dict(marker='o', markerfacecolor='red', markersize=5),
                             medianprops=dict(color='black', linewidth=2))
    else:
        box_plot = ax.boxplot(data, vert=False, patch_artist=True,
                             boxprops=dict(facecolor='lightblue', alpha=0.7),
                             flierprops=dict(marker='o', markerfacecolor='red', markersize=5),
                             medianprops=dict(color='black', linewidth=2))
    
    ax.set_title(f"Box Plot de {colonne}", fontsize=14, fontweight='bold')
    
    if orientation == "Vertical":
        ax.set_ylabel(colonne, fontsize=12)
    else:
        ax.set_xlabel(colonne, fontsize=12)
    
    ax.grid(True, alpha=0.3)
    
    # Statistiques détaillées
    if len(data) > 0:
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        st.subheader("📈 Statistiques détaillées")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Médiane", f"{data.median():.2f}")
            st.metric("Moyenne", f"{data.mean():.2f}")
        
        with col_stat2:
            st.metric("Q1 (25%)", f"{Q1:.2f}")
            st.metric("Q3 (75%)", f"{Q3:.2f}")
        
        with col_stat3:
            st.metric("IQR", f"{IQR:.2f}")
            st.metric("Valeurs aberrantes", f"{(data < (Q1 - 1.5*IQR)) | (data > (Q3 + 1.5*IQR))}.sum()")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)