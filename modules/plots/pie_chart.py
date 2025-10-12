

# modules/plots/pie_chart.py
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import streamlit as st

def plot_pie_matplotlib(df, category_col, value_col, title="Diagramme Circulaire"):
    """Version Matplotlib pour Streamlit"""
    fig, ax = plt.subplots(figsize=(8, 8))
    df_grouped = df.groupby(category_col)[value_col].sum()
    ax.pie(df_grouped.values, labels=df_grouped.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    return fig

def plot_pie_plotly(df, category_col, value_col, title="Diagramme Circulaire"):
    """Version Plotly pour interactivité"""
    df_grouped = df.groupby(category_col)[value_col].sum().reset_index()
    fig = px.pie(df_grouped, names=category_col, values=value_col, title=title)
    return fig

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("📊 Diagramme Circulaire")
    
    if df is not None and not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            category_col = st.selectbox("Colonne catégorie", df.columns, key="pie_cat")
        with col2:
            value_col = st.selectbox("Colonne valeurs", df.columns, key="pie_val")
        
        if st.button("Générer le diagramme circulaire"):
            if category_col and value_col:
                # Version Plotly
                fig = plot_pie_plotly(df, category_col, value_col)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Veuillez sélectionner les colonnes")
    else:
        st.warning("Veuillez charger un dataset valide")