
# utils/cleaning.py - VERSION COMPLÈTEMENT RÉVISÉE

import pandas as pd
import numpy as np
import streamlit as st

def detect_data_types(df):
    """Détecte automatiquement les types de données avec plus de précision"""
    results = {
        'numeric': [],
        'categorical': [],
        'datetime': [],
        'text': [],
        'boolean': [],
        'problematic': []
    }
    
    for col in df.columns:
        # Nettoyer le nom de colonne d'abord
        col_clean = str(col).strip().lower().replace(" ", "_").replace("-", "_")
        
        # Vérifier les types pandas
        dtype = df[col].dtype
        
        # Numérique
        if pd.api.types.is_numeric_dtype(df[col]):
            results['numeric'].append(col)
        
        # Booléen
        elif pd.api.types.is_bool_dtype(df[col]):
            results['boolean'].append(col)
        
        # Date/Time
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            results['datetime'].append(col)
        
        # Catégoriel ou texte
        elif pd.api.types.is_object_dtype(df[col]):
            # Essayer de convertir en datetime
            try:
                pd.to_datetime(df[col], errors='raise')
                results['datetime'].append(col)
            except:
                # Vérifier si c'est catégoriel (peu de valeurs uniques)
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.1:  # Moins de 10% de valeurs uniques
                    results['categorical'].append(col)
                else:
                    results['text'].append(col)
        
        else:
            results['problematic'].append(col)
    
    return results

def clean_column_names(df):
    """Nettoie les noms de colonnes de manière plus robuste"""
    df_clean = df.copy()
    
    new_columns = []
    for col in df_clean.columns:
        # Conversion en string et nettoyage
        col_str = str(col).strip()
        
        # Remplacer les caractères problématiques
        col_clean = (col_str
                    .lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace(".", "_")
                    .replace(",", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace("%", "percent")
                    .replace("$", "usd")
                    .replace("€", "eur")
                    .replace("&", "and"))
        
        # Supprimer les underscores multiples
        while "__" in col_clean:
            col_clean = col_clean.replace("__", "_")
        
        # Supprimer les underscores en début/fin
        col_clean = col_clean.strip("_")
        
        # Si le nom est vide après nettoyage, utiliser un nom par défaut
        if not col_clean:
            col_clean = f"column_{len(new_columns)}"
        
        new_columns.append(col_clean)
    
    df_clean.columns = new_columns
    return df_clean

def handle_missing_values_advanced(df, numeric_strategy='mean', categorical_strategy='mode', custom_values=None):
    """Gestion avancée des valeurs manquantes"""
    df_clean = df.copy()
    data_types = detect_data_types(df_clean)
    
    missing_summary = df_clean.isnull().sum()
    total_missing = missing_summary.sum()
    
    if total_missing == 0:
        return df_clean, "Aucune valeur manquante détectée"
    
    st.info(f"🔍 {total_missing} valeurs manquantes détectées")
    
    # Traitement par type de données
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            missing_count = df_clean[col].isnull().sum()
            
            # Valeur personnalisée prioritaire
            if custom_values and col in custom_values:
                fill_value = custom_values[col]
                df_clean[col].fillna(fill_value, inplace=True)
                st.write(f"✅ {col}: {missing_count} valeurs → '{fill_value}'")
            
            # Numérique
            elif col in data_types['numeric']:
                if numeric_strategy == 'mean':
                    fill_value = df_clean[col].mean()
                elif numeric_strategy == 'median':
                    fill_value = df_clean[col].median()
                elif numeric_strategy == 'zero':
                    fill_value = 0
                elif numeric_strategy == 'drop':
                    df_clean = df_clean.dropna(subset=[col])
                    st.write(f"🗑️ {col}: {missing_count} lignes supprimées")
                    continue
                else:
                    fill_value = 0
                
                df_clean[col].fillna(fill_value, inplace=True)
                st.write(f"✅ {col}: {missing_count} valeurs → {fill_value:.2f}")
            
            # Catégoriel
            elif col in data_types['categorical']:
                if categorical_strategy == 'mode':
                    fill_value = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown'
                elif categorical_strategy == 'unknown':
                    fill_value = 'Unknown'
                elif categorical_strategy == 'drop':
                    df_clean = df_clean.dropna(subset=[col])
                    st.write(f"🗑️ {col}: {missing_count} lignes supprimées")
                    continue
                else:
                    fill_value = 'Unknown'
                
                df_clean[col].fillna(fill_value, inplace=True)
                st.write(f"✅ {col}: {missing_count} valeurs → '{fill_value}'")
            
            # Date
            elif col in data_types['datetime']:
                df_clean[col].fillna(pd.NaT, inplace=True)
                st.write(f"✅ {col}: {missing_count} dates → NaT")
            
            # Texte
            elif col in data_types['text']:
                df_clean[col].fillna('', inplace=True)
                st.write(f"✅ {col}: {missing_count} valeurs → ''")
            
            # Autres types
            else:
                df_clean[col].fillna('Unknown', inplace=True)
                st.write(f"✅ {col}: {missing_count} valeurs → 'Unknown'")
    
    remaining_missing = df_clean.isnull().sum().sum()
    message = f"🎉 Nettoyage terminé : {total_missing} → {remaining_missing} valeurs manquantes"
    
    return df_clean, message

def remove_duplicates_advanced(df, subset=None, keep='first'):
    """Suppression avancée des doublons"""
    before = len(df)
    
    if subset:
        df_clean = df.drop_duplicates(subset=subset, keep=keep)
    else:
        df_clean = df.drop_duplicates(keep=keep)
    
    after = len(df_clean)
    duplicates_removed = before - after
    
    if duplicates_removed > 0:
        st.success(f"🧹 {duplicates_removed} doublons supprimés")
    else:
        st.info("🔍 Aucun doublon détecté")
    
    return df_clean

def convert_data_types_advanced(df, conversions=None):
    """Conversion avancée des types de données"""
    df_clean = df.copy()
    data_types = detect_data_types(df_clean)
    
    # Conversions automatiques si aucune spécifiée
    if not conversions:
        conversions = {}
        
        # Dates
        for col in data_types['datetime']:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                conversions[col] = 'datetime'
            except:
                pass
        
        # Numériques avec virgules
        for col in data_types['text']:
            # Essayer de convertir les nombres avec virgules
            sample = df_clean[col].dropna().head(10)
            if not sample.empty:
                if sample.astype(str).str.replace(',', '.').str.match(r'^-?\d*\.?\d+$').any():
                    try:
                        df_clean[col] = pd.to_numeric(df_clean[col].astype(str).str.replace(',', '.'), errors='coerce')
                        conversions[col] = 'numeric'
                    except:
                        pass
    
    # Appliquer les conversions spécifiées
    if conversions:
        for col, target_type in conversions.items():
            if col in df_clean.columns:
                try:
                    if target_type == 'numeric':
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    elif target_type == 'datetime':
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    elif target_type == 'category':
                        df_clean[col] = df_clean[col].astype('category')
                    elif target_type == 'string':
                        df_clean[col] = df_clean[col].astype(str)
                    
                    st.write(f"🔧 {col} converti en {target_type}")
                except Exception as e:
                    st.warning(f"⚠️ Impossible de convertir {col} en {target_type}: {e}")
    
    return df_clean

def remove_outliers(df, columns=None, method='iqr', threshold=1.5):
    """Supprime les valeurs aberrantes"""
    if columns is None:
        data_types = detect_data_types(df)
        columns = data_types['numeric']
    
    if not columns:
        return df
    
    df_clean = df.copy()
    initial_count = len(df_clean)
    
    for col in columns:
        if col in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[col]):
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:  # Éviter division par zéro
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                before = len(df_clean)
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
                outliers_removed = before - len(df_clean)
                
                if outliers_removed > 0:
                    st.write(f"🎯 {col}: {outliers_removed} valeurs aberrantes supprimées")
    
    final_count = len(df_clean)
    total_removed = initial_count - final_count
    
    if total_removed > 0:
        st.success(f"📊 {total_removed} valeurs aberrantes supprimées au total")
    
    return df_clean

def prepare_dataset(df, missing_strategy="mean", remove_duplicates_flag=True, 
                   convert_types_flag=True, remove_outliers_flag=False, outlier_threshold=1.5):
    """
    Pipeline de nettoyage COMPLET et ROBUSTE
    """
    st.subheader("🔍 Analyse des données initiales")
    st.write(f"📊 Dimensions initiales : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    
    # 1. Nettoyage des noms de colonnes
    st.subheader("1. 🧹 Nettoyage des noms de colonnes")
    df_clean = clean_column_names(df)
    st.write("✅ Noms de colonnes standardisés")
    
    # 2. Détection des types de données
    st.subheader("2. 🔍 Analyse des types de données")
    data_types = detect_data_types(df_clean)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Colonnes numériques", len(data_types['numeric']))
    with col2:
        st.metric("Colonnes catégorielles", len(data_types['categorical']))
    with col3:
        st.metric("Colonnes date/heure", len(data_types['datetime']))
    
    # 3. Gestion des valeurs manquantes
    st.subheader("3. 🎯 Gestion des valeurs manquantes")
    df_clean, missing_message = handle_missing_values_advanced(
        df_clean, 
        numeric_strategy=missing_strategy,
        categorical_strategy='mode'
    )
    st.success(missing_message)
    
    # 4. Suppression des doublons
    if remove_duplicates_flag:
        st.subheader("4. 🧹 Suppression des doublons")
        df_clean = remove_duplicates_advanced(df_clean)
    
    # 5. Conversion des types
    if convert_types_flag:
        st.subheader("5. 🔧 Conversion des types de données")
        df_clean = convert_data_types_advanced(df_clean)
    
    # 6. Suppression des valeurs aberrantes
    if remove_outliers_flag:
        st.subheader("6. 📊 Suppression des valeurs aberrantes")
        df_clean = remove_outliers(df_clean, threshold=outlier_threshold)
    
    # Résumé final
    st.subheader("🎉 Résumé du nettoyage")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lignes initiales", df.shape[0])
        st.metric("Colonnes initiales", df.shape[1])
    with col2:
        st.metric("Lignes finales", df_clean.shape[0])
        st.metric("Colonnes finales", df_clean.shape[1])
    
    rows_removed = df.shape[0] - df_clean.shape[0]
    if rows_removed > 0:
        st.info(f"📉 {rows_removed} lignes supprimées pendant le nettoyage")
    
    return df_clean