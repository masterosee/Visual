
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def run(df):
    st.subheader("📈 Courbes")
    
    st.info("Visualisez l'évolution d'une variable dans le temps ou selon une autre variable")

    # Détection automatique des colonnes de date
    date_candidates = [col for col in df.columns 
                if 'date' in col.lower() or 'time' in col.lower() or 'jour' in col.lower()]
    
    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    
    if len(colonnes_numeriques) == 0:
        st.error("❌ Aucune colonne numérique trouvée.")
        return

    # Sélection des variables
    col1, col2 = st.columns(2)
    
    with col1:
        if date_candidates:
            x_col = st.selectbox("Colonne pour l'axe X :", 
                                date_candidates + list(df.columns), 
                                key="line_x")
        else:
            x_col = st.selectbox("Colonne pour l'axe X :", df.columns, key="line_x")
    
    with col2:
        y_col = st.selectbox("Colonne pour l'axe Y :", colonnes_numeriques, key="line_y")
    
    # Options avancées
    st.subheader("🎨 Personnalisation")
    col3, col4 = st.columns(2)
    
    with col3:
        line_style = st.selectbox("Style de ligne :", 
            ["-", "--", "-.", ":", "none"])
        marker_style = st.selectbox("Style des points :",
            ["o", "s", "^", "D", "v", "none"])
        color = st.color_picker("Couleur de la ligne", "#1f77b4")
    
    with col4:
        line_width = st.slider("Épaisseur de ligne", 1.0, 5.0, 2.0)
        show_grid = st.checkbox("Afficher la grille", value=True)
        sort_data = st.checkbox("Trier par axe X", value=True)
    
    # Préparation des données
    plot_data = df[[x_col, y_col]].dropna()
    
    if sort_data:
        plot_data = plot_data.sort_values(by=x_col)
    
    # Conversion des dates si nécessaire
    if x_col in date_candidates:
        try:
            plot_data[x_col] = pd.to_datetime(plot_data[x_col])
        except:
            pass
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Tracer la courbe
    if marker_style != "none":
        ax.plot(plot_data[x_col], plot_data[y_col], 
                linestyle=line_style, marker=marker_style, 
                color=color, linewidth=line_width, markersize=4,
                markerfacecolor=color, markeredgecolor='white', markeredgewidth=0.5)
    else:
        ax.plot(plot_data[x_col], plot_data[y_col], 
                linestyle=line_style, color=color, linewidth=line_width)
    
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(f"Courbe : {y_col} en fonction de {x_col}", fontsize=14, fontweight='bold')
    
    if show_grid:
        ax.grid(True, alpha=0.3)
    
    # Rotation des labels X si trop longs
    if plot_data[x_col].dtype == 'object' and any(len(str(x)) > 10 for x in plot_data[x_col]):
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Statistiques
    if len(plot_data) > 0:
        st.subheader("📊 Statistiques de la série")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Nombre de points", len(plot_data))
            st.metric("Valeur min", f"{plot_data[y_col].min():.2f}")
        
        with col_stat2:
            st.metric("Valeur max", f"{plot_data[y_col].max():.2f}")
            st.metric("Moyenne", f"{plot_data[y_col].mean():.2f}")
        
        with col_stat3:
            if len(plot_data) > 1:
                trend = "↗️ Croissant" if plot_data[y_col].iloc[-1] > plot_data[y_col].iloc[0] else "↘️ Décroissant"
                st.metric("Tendance", trend)
                variation = ((plot_data[y_col].iloc[-1] - plot_data[y_col].iloc[0]) / plot_data[y_col].iloc[0]) * 100
                st.metric("Variation", f"{variation:.1f}%")