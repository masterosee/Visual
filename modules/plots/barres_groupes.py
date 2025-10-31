

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def run(df):
    st.header("📊 Diagramme en Barres Groupées")
    
    # Vérification des colonnes disponibles
    if df.empty:
        st.warning("Le dataset est vide.")
        return
    
    st.write("Colonnes disponibles :", list(df.columns))
    
    # Sélection des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        colonne_categorie = st.selectbox(
            "Colonne pour les catégories (axe X) :",
            options=df.columns,
            index=0
        )
    
    with col2:
        colonnes_numeriques = df.select_dtypes(include=['number']).columns.tolist()
        if not colonnes_numeriques:
            st.error("Aucune colonne numérique trouvée dans le dataset.")
            return
        
        colonne_valeur = st.selectbox(
            "Colonne pour les valeurs (axe Y) :",
            options=colonnes_numeriques,
            index=0 if colonnes_numeriques else None
        )
    
    # Recherche d'une colonne pour le grouping (Hommes/Femmes, etc.)
    colonnes_grouping = [col for col in df.columns if col != colonne_categorie and col != colonne_valeur]
    
    if colonnes_grouping:
        colonne_grouping = st.selectbox(
            "Colonne pour le grouping (ex: Genre, Type) :",
            options=colonnes_grouping,
            index=0
        )
    else:
        st.warning("Aucune colonne supplémentaire trouvée pour le grouping.")
        return
    
    # Options d'affichage
    st.subheader("Options d'affichage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        orientation = st.radio(
            "Orientation :",
            ["Vertical", "Horizontal"]
        )
    
    with col2:
        type_graphique = st.radio(
            "Type de graphique :",
            ["Matplotlib", "Plotly (interactif)"]
        )
    
    # Génération du graphique
    if st.button("Générer le diagramme"):
        try:
            # Préparation des données
            data_grouped = df.groupby([colonne_categorie, colonne_grouping])[colonne_valeur].mean().reset_index()
            
            if type_graphique == "Matplotlib":
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Préparation des données pour matplotlib
                categories = data_grouped[colonne_categorie].unique()
                groups = data_grouped[colonne_grouping].unique()
                
                bar_width = 0.8 / len(groups)
                x_pos = range(len(categories))
                
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                
                for i, group in enumerate(groups):
                    group_data = data_grouped[data_grouped[colonne_grouping] == group]
                    values = [group_data[group_data[colonne_categorie] == cat][colonne_valeur].values[0] 
                             if cat in group_data[colonne_categorie].values else 0 
                             for cat in categories]
                    
                    if orientation == "Vertical":
                        positions = [x + i * bar_width for x in x_pos]
                        ax.bar(positions, values, bar_width, label=group, color=colors[i % len(colors)])
                    else:
                        positions = [x + i * bar_width for x in x_pos]
                        ax.barh(positions, values, bar_width, label=group, color=colors[i % len(colors)])
                
                # Configuration des axes
                if orientation == "Vertical":
                    ax.set_xlabel(colonne_categorie)
                    ax.set_ylabel(colonne_valeur)
                    ax.set_xticks([x + bar_width * (len(groups)-1)/2 for x in x_pos])
                    ax.set_xticklabels(categories, rotation=45)
                else:
                    ax.set_ylabel(colonne_categorie)
                    ax.set_xlabel(colonne_valeur)
                    ax.set_yticks([x + bar_width * (len(groups)-1)/2 for x in x_pos])
                    ax.set_yticklabels(categories)
                
                ax.set_title(f"Barres Groupées : {colonne_valeur} par {colonne_categorie} et {colonne_grouping}")
                ax.legend(title=colonne_grouping)
                ax.grid(axis='y', alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                
            else:  # Plotly
                if orientation == "Vertical":
                    fig = px.bar(
                        data_grouped,
                        x=colonne_categorie,
                        y=colonne_valeur,
                        color=colonne_grouping,
                        barmode='group',
                        title=f"Barres Groupées : {colonne_valeur} par {colonne_categorie} et {colonne_grouping}",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                else:
                    fig = px.bar(
                        data_grouped,
                        y=colonne_categorie,
                        x=colonne_valeur,
                        color=colonne_grouping,
                        barmode='group',
                        orientation='h',
                        title=f"Barres Groupées : {colonne_valeur} par {colonne_categorie} et {colonne_grouping}",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                
                fig.update_layout(
                    xaxis_title=colonne_valeur if orientation == "Vertical" else colonne_categorie,
                    yaxis_title=colonne_categorie if orientation == "Vertical" else colonne_valeur,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Affichage des données utilisées
            st.subheader("📋 Données utilisées")
            st.dataframe(data_grouped)
            
        except Exception as e:
            st.error(f"Erreur lors de la génération du graphique : {e}")
            st.info("Assurez-vous que les colonnes sélectionnées contiennent des données valides.")

def create_sample_data():
    """Crée des données d'exemple pour les barres groupées"""
    data = {
        'Domaine': ['Informatique', 'Informatique', 'Marketing', 'Marketing', 'Finance', 'Finance', 'RH', 'RH'],
        'Genre': ['Hommes', 'Femmes', 'Hommes', 'Femmes', 'Hommes', 'Femmes', 'Hommes', 'Femmes'],
        'Salaire': [45000, 42000, 38000, 37000, 52000, 48000, 35000, 34000],
        'Effectif': [120, 80, 90, 110, 70, 50, 60, 75]
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Test du module avec des données d'exemple
    sample_df = create_sample_data()
    run(sample_df)