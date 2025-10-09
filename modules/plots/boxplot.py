

import streamlit as st
import matplotlib.pyplot as plt

def run(df):
    st.subheader("📦 Box Plot")

    # Colonnes numériques
    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) == 0:
        st.error("Aucune colonne numérique trouvée dans le dataset.")
        return

    colonne = st.selectbox("Choisissez une colonne :", colonnes_numeriques)

    # Tracer le boxplot
    fig, ax = plt.subplots()
    ax.boxplot(df[colonne].dropna(), vert=True, patch_artist=True)
    ax.set_title(f"Box Plot de {colonne}")
    st.pyplot(fig)
