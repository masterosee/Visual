
import streamlit as st
import matplotlib.pyplot as plt

def run(df):
    st.subheader("☁️ Nuage de points")

    colonnes_numeriques = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colonnes_numeriques) < 2:
        st.error("Il faut au moins deux colonnes numériques pour un scatter plot.")
        return

    x_col = st.selectbox("Colonne pour l’axe X :", colonnes_numeriques, key="scatter_x")
    y_col = st.selectbox("Colonne pour l’axe Y :", colonnes_numeriques, key="scatter_y")

    fig, ax = plt.subplots()
    ax.scatter(df[x_col], df[y_col], alpha=0.6, color="teal")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"Nuage de points : {x_col} vs {y_col}")
    st.pyplot(fig)
