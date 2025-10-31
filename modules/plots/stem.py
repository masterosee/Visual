# modules/plots/stem.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def plot_stem_matplotlib(df, x_col, y_col, title="Parcelle de Tiges"):
    """Version Matplotlib - Stem Plot classique"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Trier les données par x_col si numérique
    if pd.api.types.is_numeric_dtype(df[x_col]):
        df_sorted = df.sort_values(x_col)
    else:
        df_sorted = df.copy()
    
    # Créer le stem plot
    markerline, stemlines, baseline = ax.stem(
        df_sorted[x_col], 
        df_sorted[y_col],
        linefmt='grey', 
        markerfmt='D', 
        basefmt=' '
    )
    
    # Personnaliser l'apparence
    plt.setp(markerline, markersize=6, color='red', markerfacecolor='red')
    plt.setp(stemlines, linewidth=1.5, color='blue', alpha=0.7)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True, alpha=0.3)
    
    # Rotation des labels x si catégoriels
    if not pd.api.types.is_numeric_dtype(df[x_col]):
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    return fig

def plot_stem_plotly(df, x_col, y_col, title="Parcelle de Tiges"):
    """Version Plotly - Stem Plot interactif"""
    # Trier les données
    if pd.api.types.is_numeric_dtype(df[x_col]):
        df_sorted = df.sort_values(x_col)
    else:
        df_sorted = df.copy()
    
    fig = go.Figure()
    
    # Ajouter les tiges
    for i, (x_val, y_val) in enumerate(zip(df_sorted[x_col], df_sorted[y_col])):
        fig.add_trace(go.Scatter(
            x=[x_val, x_val],
            y=[0, y_val],
            mode='lines',
            line=dict(color='blue', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Ajouter les marqueurs
    fig.add_trace(go.Scatter(
        x=df_sorted[x_col],
        y=df_sorted[y_col],
        mode='markers',
        marker=dict(color='red', size=8, symbol='diamond'),
        name=y_col,
        hovertemplate=f'<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True,
        hovermode='closest'
    )
    
    return fig

def plot_stem_multiple(df, x_col, y_columns, title="Parcelle de Tiges Multiples"):
    """Stem plot pour plusieurs séries"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Trier les données
    if pd.api.types.is_numeric_dtype(df[x_col]):
        df_sorted = df.sort_values(x_col)
    else:
        df_sorted = df.copy()
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    markers = ['o', 's', 'D', '^', 'v']
    
    for i, y_col in enumerate(y_columns):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        # Créer le stem plot pour chaque série
        markerline, stemlines, baseline = ax.stem(
            df_sorted[x_col], 
            df_sorted[y_col],
            linefmt=f'{color}-', 
            markerfmt=marker, 
            basefmt=' ',
            label=y_col
        )
        
        plt.setp(markerline, markersize=6, color=color, markerfacecolor=color)
        plt.setp(stemlines, linewidth=1.2, color=color, alpha=0.7)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel("Valeurs")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if not pd.api.types.is_numeric_dtype(df[x_col]):
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    return fig

def plot_stem_vertical_horizontal(df, x_col, y_col, orientation="vertical", title="Parcelle de Tiges"):
    """Stem plot vertical ou horizontal"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if orientation == "vertical":
        # Trier les données
        if pd.api.types.is_numeric_dtype(df[x_col]):
            df_sorted = df.sort_values(x_col)
        else:
            df_sorted = df.copy()
        
        markerline, stemlines, baseline = ax.stem(
            df_sorted[x_col], 
            df_sorted[y_col],
            linefmt='grey', 
            markerfmt='D', 
            basefmt=' '
        )
        
        plt.setp(markerline, markersize=6, color='red', markerfacecolor='red')
        plt.setp(stemlines, linewidth=1.5, color='blue', alpha=0.7)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
        if not pd.api.types.is_numeric_dtype(df[x_col]):
            plt.xticks(rotation=45)
    
    else:  # Horizontal
        # Trier les données
        if pd.api.types.is_numeric_dtype(df[y_col]):
            df_sorted = df.sort_values(y_col)
        else:
            df_sorted = df.copy()
        
        markerline, stemlines, baseline = ax.stem(
            df_sorted[y_col], 
            df_sorted[x_col],
            linefmt='grey', 
            markerfmt='D', 
            basefmt=' ',
            orientation='horizontal'
        )
        
        plt.setp(markerline, markersize=6, color='red', markerfacecolor='red')
        plt.setp(stemlines, linewidth=1.5, color='blue', alpha=0.7)
        
        ax.set_ylabel(x_col)
        ax.set_xlabel(y_col)
        
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            plt.yticks(rotation=45)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def run(df):
    """Fonction principale pour Streamlit"""
    st.subheader("🌿 Parcelle de Tiges")
    
    if df is None or df.empty:
        st.warning("📂 Veuillez charger un dataset valide")
        return
    
    st.info("""
    💡 **La parcelle de tiges (stem plot)** :
    - 📍 **Points discrets** = Marqueurs pour chaque valeur
    - 📏 **Lignes verticales** = Relient les points à l'axe de référence
    - 📊 **Données discrètes** = Idéal pour les séries temporelles, fréquences, distributions
    - 👁️ **Visualisation claire** = Montre l'amplitude et la position des points
    """)
    
    # Sélection du type de stem plot
    stem_type = st.radio(
        "Type de parcelle de tiges:",
        ["Stem Simple", "Stem Multiple", "Stem Horizontal"],
        key="stem_type"
    )
    
    # Sélection des colonnes de base
    col1, col2 = st.columns(2)
    
    with col1:
        # Colonne pour l'axe X (ou Y pour horizontal)
        x_column = st.selectbox(
            "Colonne catégorielle/numerique:",
            options=df.columns.tolist(),
            key="stem_x"
        )
    
    with col2:
        if stem_type == "Stem Multiple":
            # Multiples colonnes numériques
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            y_columns = st.multiselect(
                "Colonnes numériques à afficher:",
                options=numeric_columns,
                default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns,
                key="stem_multi_y"
            )
        else:
            # Une seule colonne numérique
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            y_column = st.selectbox(
                "Colonne numérique:",
                options=numeric_columns,
                key="stem_y"
            )
    
    # Options d'affichage
    col3, col4 = st.columns(2)
    
    with col3:
        chart_library = st.radio(
            "Bibliothèque de visualisation:",
            ["Matplotlib", "Plotly (Interactif)"],
            key="stem_lib"
        )
    
    with col4:
        title = st.text_input("Titre du graphique:", "Parcelle de Tiges", key="stem_title")
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        show_stats = st.checkbox("Afficher les statistiques", value=True)
        if stem_type != "Stem Multiple":
            orientation = st.radio(
                "Orientation:",
                ["vertical", "horizontal"],
                key="stem_orientation"
            )
    
    # Génération du graphique
    if st.button("🌿 Générer la Parcelle de Tiges", type="primary"):
        if stem_type == "Stem Simple":
            if not x_column or not y_column:
                st.error("❌ Veuillez sélectionner les colonnes X et Y")
                return
            
            try:
                # Nettoyage des données
                df_clean = df[[x_column, y_column]].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique
                if chart_library == "Plotly (Interactif)":
                    fig = plot_stem_plotly(df_clean, x_column, y_column, title)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    if stem_type == "Stem Horizontal":
                        fig = plot_stem_vertical_horizontal(df_clean, x_column, y_column, "horizontal", title)
                    else:
                        fig = plot_stem_matplotlib(df_clean, x_column, y_column, title)
                    st.pyplot(fig)
                    plt.close(fig)
                
                # Statistiques
                if show_stats:
                    st.subheader("📊 Statistiques")
                    col_stat1, col_stat2 = st.columns(2)
                    
                    with col_stat1:
                        st.write(f"**{y_column}:**")
                        stats = df_clean[y_column].describe()
                        st.dataframe(stats)
                    
                    with col_stat2:
                        st.write("**Valeurs uniques:**")
                        st.write(f"Nombre de points: {len(df_clean)}")
                        st.write(f"Valeur max: {df_clean[y_column].max():.2f}")
                        st.write(f"Valeur min: {df_clean[y_column].min():.2f}")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
        
        elif stem_type == "Stem Multiple":
            if not x_column or len(y_columns) < 1:
                st.error("❌ Veuillez sélectionner une colonne X et au moins une colonne Y")
                return
            
            try:
                # Nettoyage des données
                cols_to_keep = [x_column] + y_columns
                df_clean = df[cols_to_keep].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique
                fig = plot_stem_multiple(df_clean, x_column, y_columns, title)
                st.pyplot(fig)
                plt.close(fig)
                
                # Statistiques comparatives
                if show_stats:
                    st.subheader("📊 Statistiques Comparatives")
                    for y_col in y_columns:
                        st.write(f"**{y_col}:**")
                        stats = df_clean[y_col].describe()
                        st.dataframe(stats)
                        
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
        
        else:  # Stem Horizontal
            if not x_column or not y_column:
                st.error("❌ Veuillez sélectionner les colonnes")
                return
            
            try:
                # Nettoyage des données
                df_clean = df[[x_column, y_column]].dropna()
                
                if df_clean.empty:
                    st.error("❌ Aucune donnée valide après nettoyage")
                    return
                
                # Génération du graphique horizontal
                fig = plot_stem_vertical_horizontal(df_clean, x_column, y_column, "horizontal", title)
                st.pyplot(fig)
                plt.close(fig)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
        
        # Informations éducatives
        with st.expander("🎓 Comprendre les Parcelles de Tiges"):
            st.markdown("""
            **Cas d'usage typiques :**
            - 📡 **Signaux discrets** = Traitement du signal
            - 📊 **Séries temporelles** = Données à intervalles réguliers
            - 🔢 **Distributions de fréquences** = Histogrammes alternatifs
            - 📈 **Données d'amplitude** = Montre l'importance des valeurs
            
            **Avantages :**
            - Montre clairement chaque point de données
            - Facile à lire pour les données discrètes
            - Bon pour les comparaisons d'amplitude
            """)

if __name__ == "__main__":
    # Test avec des données exemple
    sample_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
        'Ventes': [100, 150, 120, 180, 200, 160],
        'Clients': [50, 70, 60, 80, 90, 75],
        'Temperature': [15, 18, 20, 22, 25, 28]
    })
    run(sample_data)