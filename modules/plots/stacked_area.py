# modules/plots/stacked_area.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def plot_stacked_area_plotly(df, x_col, y_columns, title="Surfaces Empilées"):
    """Version Plotly - Stacked Area Chart interactif"""
    fig = px.area(df, x=x_col, y=y_columns, 
                  title=title,
                  labels={x_col: x_col, 'value': 'Valeur'},
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title="Valeur cumulée",
        hovermode='x unified'
    )
    return fig

def plot_stacked_area_matplotlib(df, x_col, y_columns, title="Surfaces Empilées"):
    """Version Matplotlib - Stacked Area Chart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Trier par la colonne x si elle est numérique ou date
    if pd.api.types.is_numeric_dtype(df[x_col]):
        df_sorted = df.sort_values(x_col)
    else:
        df_sorted = df.copy()
    
    # Créer le stacked area plot
    ax.stackplot(df_sorted[x_col], [df_sorted[col] for col in y_columns],
                 labels=y_columns, alpha=0.8)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel("Valeur cumulée")
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("📈 Tableau des Surfaces Empilées")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("💡 Les surfaces empilées montrent l'évolution temporelle de plusieurs séries avec leur contribution cumulative")
    
    # Sélection des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Colonne pour l'axe X (généralement temporelle)
        x_column = st.selectbox(
            "Colonne pour l'axe X (date/temps):",
            options=df.columns.tolist(),
            key="stacked_x"
        )
    
    with col2:
        # Colonnes pour l'axe Y (valeurs numériques)
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        y_columns = st.multiselect(
            "Colonnes à empiler (valeurs numériques):",
            options=numeric_columns,
            default=numeric_columns[:3] if len(numeric_columns) >= 3 else numeric_columns,
            key="stacked_y"
        )
    
    # Options d'affichage
    col3, col4 = st.columns(2)
    
    with col3:
        chart_library = st.radio(
            "Bibliothèque de visualisation:",
            ["Plotly (Interactif)", "Matplotlib"],
            key="stacked_lib"
        )
    
    with col4:
        title = st.text_input("Titre du graphique:", "Surfaces Empilées", key="stacked_title")
    
    # Génération du graphique
    if st.button("📊 Générer le Tableau des Surfaces Empilées", type="primary"):
        if not x_column:
            st.error("❌ Veuillez sélectionner une colonne pour l'axe X")
            return
        
        if len(y_columns) < 2:
            st.error("❌ Veuillez sélectionner au moins 2 colonnes numériques à empiler")
            return
        
        try:
            # Nettoyage des données
            df_clean = df[[x_column] + y_columns].dropna()
            
            if df_clean.empty:
                st.error("❌ Aucune donnée valide après nettoyage")
                return
            
            # Conversion de la colonne x en datetime si possible
            if not pd.api.types.is_numeric_dtype(df_clean[x_column]):
                try:
                    df_clean[x_column] = pd.to_datetime(df_clean[x_column])
                except:
                    pass
            
            # Génération du graphique
            if chart_library == "Plotly (Interactif)":
                fig = plot_stacked_area_plotly(df_clean, x_column, y_columns, title)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques
                st.subheader("📊 Statistiques des Séries")
                stats_df = df_clean[y_columns].describe()
                st.dataframe(stats_df)
                
            else:  # Matplotlib
                fig = plot_stacked_area_matplotlib(df_clean, x_column, y_columns, title)
                st.pyplot(fig)
                plt.close(fig)
                
                # Téléchargement des données préparées
                csv = df_clean.to_csv(index=False)
                st.download_button(
                    label="💾 Télécharger les données préparées (CSV)",
                    data=csv,
                    file_name="stacked_area_data.csv",
                    mime="text/csv"
                )
            
            # Informations sur les données
            with st.expander("ℹ️ Informations sur les données"):
                st.write(f"**Dimensions:** {df_clean.shape[0]} lignes × {df_clean.shape[1]} colonnes")
                st.write(f"**Période couverte:** {df_clean[x_column].min()} à {df_clean[x_column].max()}")
                st.write(f"**Séries affichées:** {', '.join(y_columns)}")
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération du graphique: {str(e)}")
            st.info("💡 Conseil: Vérifiez que votre colonne X est de type date ou numérique")

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Année': [2010, 2011, 2012, 2013, 2014, 2015],
        'Ventes_A': [100, 120, 150, 180, 200, 220],
        'Ventes_B': [80, 90, 110, 130, 150, 170],
        'Ventes_C': [60, 70, 85, 95, 110, 125]
    })
    run(sample_data)