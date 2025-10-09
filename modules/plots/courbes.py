

import streamlit as st
import matplotlib.pyplot as plt

def run(df):
    st.subheader("📈 Courbes")

    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) == 0:
        st.error("Aucune colonne numérique trouvée pour tracer une courbe.")
        return

    x_col = st.selectbox("Colonne pour l’axe X :", df.columns, key="line_x")
    y_col = st.selectbox("Colonne pour l’axe Y :", colonnes_numeriques, key="line_y")

    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col], marker="o", linestyle="-", color="purple")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"Courbe de {y_col} en fonction de {x_col}")
    st.pyplot(fig)
