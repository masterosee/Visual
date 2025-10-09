
import streamlit as st
import matplotlib.pyplot as plt

def run(df):
    st.subheader("📊 Histogramme")

    # Choisir une colonne numérique
    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) == 0:
        st.error("Aucune colonne numérique trouvée dans le dataset.")
        return

    colonne = st.selectbox("Choisissez une colonne :", colonnes_numeriques)

    # Tracer l’histogramme
    fig, ax = plt.subplots()
    df[colonne].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
    ax.set_title(f"Histogramme de {colonne}")
    st.pyplot(fig)
