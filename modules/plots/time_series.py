
# modules/plots/time_series.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def run_simple(df):
    """Interface Streamlit pour série temporelle simple"""
    st.subheader("⏱️ Série Temporelle Simple")
    
    st.info("""
    💡 **Visualisez l'évolution d'une variable dans le temps :**
    - 📅 **Données temporelles** = Dates, mois, années, périodes
    - 📈 **Tendances** = Évolution dans le temps
    - 🔍 **Patterns** = Saisonnalité, cycles, points clés
    """)
    
    # Détection automatique des colonnes
    date_candidates = [col for col in df.columns 
                      if any(keyword in col.lower() for keyword in 
                            ['date', 'time', 'jour', 'année', 'year', 'month', 'jour', 'timestamp'])]
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if not date_candidates or not numeric_columns:
        st.error("❌ Colonnes de date ou numériques manquantes dans le dataset")
        return
    
    # Sélection des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        date_col = st.selectbox("Colonne de date/temps :", date_candidates, key="ts_simple_date")
        st.write(f"*Exemple: {df[date_col].iloc[0] if len(df) > 0 else 'Aucune donnée'}*")
    
    with col2:
        value_col = st.selectbox("Colonne des valeurs :", numeric_columns, key="ts_simple_value")
        if len(df) > 0:
            min_val = df[value_col].min()
            max_val = df[value_col].max()
            st.write(f"*Plage: {min_val:.2f} à {max_val:.2f}*")
    
    # Options d'affichage
    st.subheader("🎨 Options de visualisation")
    
    col3, col4 = st.columns(2)
    
    with col3:
        line_style = st.selectbox("Style de ligne :", ["-", "--", "-.", ":"], key="ts_line_style")
        marker_style = st.selectbox("Marqueur :", ["o", "s", "^", "D", "v", "none"], key="ts_marker")
        color = st.color_picker("Couleur principale", "#1f77b4", key="ts_color")
    
    with col4:
        show_grid = st.checkbox("Afficher la grille", True, key="ts_grid")
        show_trend = st.checkbox("Ligne de tendance", False, key="ts_trend")
        smooth_data = st.checkbox("Lissage des données", False, key="ts_smooth")
        if smooth_data:
            window_size = st.slider("Intensité du lissage", 3, 21, 5, 2, key="ts_smooth_window")
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        col5, col6 = st.columns(2)
        
        with col5:
            line_width = st.slider("Épaisseur de ligne", 1.0, 5.0, 2.0, key="ts_line_width")
            marker_size = st.slider("Taille marqueurs", 2, 10, 4, key="ts_marker_size")
        
        with col6:
            show_confidence = st.checkbox("Bandes de confiance", False, key="ts_confidence")
            if show_confidence:
                confidence_level = st.slider("Niveau confiance (%)", 80, 99, 95, key="ts_conf_level")
    
    # Génération du graphique
    if st.button("📈 Générer la série temporelle", type="primary", key="ts_generate"):
        try:
            # Préparation des données
            df_clean = df[[date_col, value_col]].copy()
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            df_clean = df_clean.dropna().sort_values(date_col)
            
            if df_clean.empty:
                st.error("❌ Aucune donnée valide après conversion des dates")
                return
            
            if len(df_clean) < 2:
                st.error("❌ Insuffisamment de points de données pour une série temporelle")
                return
            
            # Création du graphique
            fig, ax = plt.subplots(figsize=(12, 6))
            
            dates = df_clean[date_col]
            values = df_clean[value_col]
            
            # Lissage si demandé
            if smooth_data and len(df_clean) > window_size:
                try:
                    y_smooth = signal.savgol_filter(values, 
                                                   window_length=min(window_size, len(df_clean)//2*2-1), 
                                                   polyorder=2)
                    ax.plot(dates, y_smooth, linestyle=line_style, color=color, 
                           linewidth=line_width, label=f"{value_col} (lissé)")
                    # Données originales en transparence
                    if marker_style != "none":
                        ax.plot(dates, values, linestyle='', marker=marker_style, 
                               markersize=marker_size, color=color, alpha=0.3,
                               label=f"{value_col} (original)")
                except:
                    st.warning("⚠️ Lissage impossible - affichage des données brutes")
                    smooth_data = False
            
            if not smooth_data:
                # Données normales
                if marker_style != "none":
                    ax.plot(dates, values, linestyle=line_style, marker=marker_style, 
                           color=color, linewidth=line_width, markersize=marker_size, 
                           label=value_col)
                else:
                    ax.plot(dates, values, linestyle=line_style, color=color, 
                           linewidth=line_width, label=value_col)
            
            # Ligne de tendance
            if show_trend and len(df_clean) > 1:
                x_numeric = pd.to_numeric(dates)
                z = np.polyfit(x_numeric, values, 1)
                p = np.poly1d(z)
                trend_line = p(x_numeric)
                ax.plot(dates, trend_line, "r--", alpha=0.8, linewidth=2, label="Tendance linéaire")
                
                # Calcul pente
                slope = z[0] * (x_numeric.max() - x_numeric.min()) / (len(x_numeric) * 86400000000000)  # pente par jour
                st.info(f"📈 **Pente de tendance** : {slope:.6f} unités/jour")
            
            # Bande de confiance
            if show_confidence and len(df_clean) > 2:
                mean = values.mean()
                std = values.std()
                confidence = (100 - confidence_level) / 100
                z_score = 2.0  # Approximation pour 95%
                
                upper_bound = mean + z_score * std
                lower_bound = mean - z_score * std
                
                ax.fill_between(dates, lower_bound, upper_bound, alpha=0.2, color=color,
                               label=f"Intervalle de confiance {confidence_level}%")
            
            ax.set_title(f"Série temporelle : {value_col}", fontsize=14, fontweight='bold')
            ax.set_xlabel(date_col, fontsize=12)
            ax.set_ylabel(value_col, fontsize=12)
            ax.legend()
            
            if show_grid:
                ax.grid(True, alpha=0.3)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            # Statistiques détaillées
            show_advanced_stats = st.checkbox("📊 Afficher les statistiques avancées", True)
            if show_advanced_stats:
                display_time_series_stats(df_clean, date_col, value_col)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération : {str(e)}")
            st.info("💡 Vérifiez le format de vos dates et valeurs numériques")

def run_multiple(df):
    """Interface Streamlit pour séries temporelles multiples"""
    st.subheader("⏱️ Séries Temporelles Multiples")
    
    st.info("""
    💡 **Comparez plusieurs variables dans le temps :**
    - 🔄 **Comparaisons** = Évolutions parallèles
    - 📊 **Corrélations** = Relations entre séries
    - 🎨 **Visualisation** = Couleurs distinctes pour chaque série
    """)
    
    # Détection automatique des colonnes
    date_candidates = [col for col in df.columns 
                      if any(keyword in col.lower() for keyword in 
                            ['date', 'time', 'jour', 'année', 'year', 'month'])]
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if not date_candidates or len(numeric_columns) < 2:
        st.error("❌ Colonnes de date ou multiples colonnes numériques manquantes")
        return
    
    # Sélection des colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        date_col = st.selectbox("Colonne de date/temps :", date_candidates, key="ts_multi_date")
    
    with col2:
        value_cols = st.multiselect("Colonnes à comparer :", numeric_columns, 
                                   default=numeric_columns[:min(3, len(numeric_columns))],
                                   key="ts_multi_values")
    
    if not value_cols:
        st.warning("⚠️ Sélectionnez au moins une colonne numérique")
        return
    
    # Options d'affichage
    st.subheader("🎨 Options de visualisation")
    
    col3, col4 = st.columns(2)
    
    with col3:
        line_style = st.selectbox("Style de ligne :", ["-", "--", "-.", ":"], key="ts_multi_line")
        show_grid = st.checkbox("Afficher la grille", True, key="ts_multi_grid")
        normalize = st.checkbox("Normaliser les données", False, key="ts_multi_norm")
    
    with col4:
        chart_type = st.radio("Type de graphique :", 
                             ["Lignes", "Aires empilées", "Lignes + Points"], 
                             key="ts_multi_type")
        show_correlation = st.checkbox("Matrice de corrélation", True, key="ts_multi_corr")
    
    # Génération du graphique
    if st.button("📊 Générer les séries multiples", type="primary", key="ts_multi_generate"):
        try:
            # Préparation des données
            cols_to_keep = [date_col] + value_cols
            df_clean = df[cols_to_keep].copy()
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            df_clean = df_clean.dropna().sort_values(date_col)
            
            if df_clean.empty:
                st.error("❌ Aucune donnée valide après conversion des dates")
                return
            
            # Normalisation si demandée
            if normalize:
                for col in value_cols:
                    df_clean[col] = (df_clean[col] - df_clean[col].mean()) / df_clean[col].std()
            
            # Création du graphique
            fig, ax = plt.subplots(figsize=(14, 8))
            
            dates = df_clean[date_col]
            colors = plt.cm.Set3(np.linspace(0, 1, len(value_cols)))
            
            if chart_type == "Aires empilées":
                ax.stackplot(dates, [df_clean[col] for col in value_cols], 
                           labels=value_cols, colors=colors, alpha=0.7)
            else:
                for i, col in enumerate(value_cols):
                    if chart_type == "Lignes + Points":
                        ax.plot(dates, df_clean[col], linestyle=line_style, marker='o',
                               color=colors[i], linewidth=2, markersize=4, label=col)
                    else:
                        ax.plot(dates, df_clean[col], linestyle=line_style,
                               color=colors[i], linewidth=2, label=col)
            
            title = f"Séries temporelles multiples"
            if normalize:
                title += " (données normalisées)"
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel(date_col, fontsize=12)
            ax.set_ylabel("Valeurs" + (" (normalisées)" if normalize else ""), fontsize=12)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            if show_grid:
                ax.grid(True, alpha=0.3)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            # Matrice de corrélation
            if show_correlation and len(value_cols) > 1:
                st.subheader("📈 Matrice de Corrélation")
                corr_matrix = df_clean[value_cols].corr()
                
                fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
                im = ax_corr.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
                
                # Ajouter les valeurs dans les cases
                for i in range(len(value_cols)):
                    for j in range(len(value_cols)):
                        text = ax_corr.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                          ha="center", va="center", color="black", fontweight='bold')
                
                ax_corr.set_xticks(range(len(value_cols)))
                ax_corr.set_yticks(range(len(value_cols)))
                ax_corr.set_xticklabels(value_cols, rotation=45)
                ax_corr.set_yticklabels(value_cols)
                ax_corr.set_title("Matrice de Corrélation", fontweight='bold')
                
                plt.colorbar(im, ax=ax_corr)
                plt.tight_layout()
                st.pyplot(fig_corr)
                plt.close(fig_corr)
            
            # Statistiques comparatives
            display_multi_series_stats(df_clean, date_col, value_cols)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération : {str(e)}")

def display_time_series_stats(df, date_col, value_col):
    """Affiche les statistiques détaillées d'une série temporelle"""
    st.subheader("📊 Analyse Statistique")
    
    values = df[value_col]
    dates = df[date_col]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Période couverte", 
                 f"{dates.min().strftime('%d/%m/%Y')} au {dates.max().strftime('%d/%m/%Y')}")
        st.metric("Durée totale", f"{(dates.max() - dates.min()).days} jours")
        st.metric("Nombre de points", len(df))
    
    with col2:
        st.metric("Valeur moyenne", f"{values.mean():.2f}")
        st.metric("Écart-type", f"{values.std():.2f}")
        st.metric("Coefficient variation", f"{(values.std()/values.mean()*100):.1f}%")
    
    with col3:
        growth = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0]) * 100
        st.metric("Croissance totale", f"{growth:.1f}%")
        st.metric("Valeur maximale", f"{values.max():.2f}")
        st.metric("Valeur minimale", f"{values.min():.2f}")
    
    # Analyse de tendance
    if len(df) > 1:
        st.subheader("📈 Analyse de Tendance")
        
        # Régression linéaire
        x_numeric = pd.to_numeric(dates)
        slope, intercept = np.polyfit(x_numeric, values, 1)
        daily_slope = slope * 86400000000000  # Conversion en unités par jour
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.write("**Tendance linéaire:**")
            st.write(f"- Pente : {daily_slope:.6f} unités/jour")
            st.write(f"- Direction : {'↗️ Hausse' if daily_slope > 0 else '↘️ Baisse' if daily_slope < 0 else '➡️ Stable'}")
        
        with col_t2:
            # Volatilité
            returns = values.pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) if len(returns) > 1 else 0  # Volatilité annualisée
            st.write("**Volatilité:**")
            st.write(f"- Volatilité : {volatility:.2%}" if volatility > 0 else "- Volatilité : N/A")

def display_multi_series_stats(df, date_col, value_cols):
    """Affiche les statistiques comparatives des séries multiples"""
    st.subheader("📊 Statistiques Comparatives")
    
    stats_data = []
    for col in value_cols:
        values = df[col]
        stats_data.append({
            'Série': col,
            'Moyenne': f"{values.mean():.2f}",
            'Écart-type': f"{values.std():.2f}",
            'Min': f"{values.min():.2f}",
            'Max': f"{values.max():.2f}",
            'Croissance': f"{((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100):.1f}%" if len(values) > 1 else "N/A"
        })
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True)

# Fonctions originales conservées pour compatibilité
def plot_time_series(df, x_col, y_col, title="Série temporelle", xlabel=None, ylabel=None):
    """
    Trace une série temporelle simple.
    - df : DataFrame Pandas
    - x_col : colonne pour l'axe des X (dates ou périodes)
    - y_col : colonne pour l'axe des Y (valeurs numériques)
    """
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Colonnes {x_col} ou {y_col} introuvables dans le DataFrame")

    if not pd.api.types.is_datetime64_any_dtype(df[x_col]):
        df[x_col] = pd.to_datetime(df[x_col], errors="coerce")

    plt.figure(figsize=(10, 5))
    plt.plot(df[x_col], df[y_col], marker="o", linestyle="-", color="blue")
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.grid(True)
    plt.tight_layout()
    return plt

def plot_time_series_multi(df, x_col, y_cols, title="Séries temporelles multiples", xlabel=None, ylabel=None):
    """
    Trace plusieurs séries temporelles sur une même figure.
    - df : DataFrame Pandas
    - x_col : colonne pour l'axe des X (dates ou périodes)
    - y_cols : liste de colonnes pour l'axe des Y
    """
    if x_col not in df.columns:
        raise ValueError(f"Colonne {x_col} introuvable dans le DataFrame")

    for col in y_cols:
        if col not in df.columns:
            raise ValueError(f"Colonne {col} introuvable dans le DataFrame")

    if not pd.api.types.is_datetime64_any_dtype(df[x_col]):
        df[x_col] = pd.to_datetime(df[x_col], errors="coerce")

    plt.figure(figsize=(10, 5))
    for col in y_cols:
        plt.plot(df[x_col], df[col], marker="o", linestyle="-", label=col)

    plt.title(title)
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else "Valeurs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt