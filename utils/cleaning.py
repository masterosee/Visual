# utils/cleaning.py

import pandas as pd
import numpy as np

# --- Colonnes ---
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Uniformise les noms de colonnes :
    - minuscules
    - espaces remplacés par '_'
    - suppression des espaces en trop
    """
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

# --- Valeurs manquantes ---
def handle_missing(df: pd.DataFrame, strategy: str = "drop", fill_value=None) -> pd.DataFrame:
    """
    Gère les valeurs manquantes selon la stratégie choisie :
    - "drop"   : supprime les lignes contenant des NaN
    - "mean"   : remplace par la moyenne (colonnes numériques uniquement)
    - "median" : remplace par la médiane (colonnes numériques uniquement)
    - "fill"   : remplace par une valeur donnée (fill_value)
    """
    df = df.copy()
    if strategy == "drop":
        return df.dropna()
    elif strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == "median":
        return df.fillna(df.median(numeric_only=True))
    elif strategy == "fill":
        return df.fillna(fill_value)
    else:
        raise ValueError(f"Stratégie inconnue: {strategy}")

# --- Doublons ---
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les lignes dupliquées."""
    return df.drop_duplicates()

# --- Types de données ---
def convert_types(df: pd.DataFrame, conversions: dict) -> pd.DataFrame:
    """
    Convertit les colonnes selon un mapping fourni.
    Exemple : {"date": "datetime64[ns]", "valeur": float}
    """
    df = df.copy()
    for col, dtype in conversions.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                raise ValueError(f"Impossible de convertir {col} en {dtype}: {e}")
    return df

# --- Pipeline complet ---
def prepare_dataset(df: pd.DataFrame,
                    missing_strategy: str = "drop",
                    fill_value=None,
                    conversions: dict = None) -> pd.DataFrame:
    """
    Pipeline de nettoyage standard :
    1. Nettoyage des colonnes
    2. Gestion des valeurs manquantes
    3. Suppression des doublons
    4. Conversion des types (optionnel)
    """
    df = clean_columns(df)
    df = handle_missing(df, strategy=missing_strategy, fill_value=fill_value)
    df = remove_duplicates(df)
    if conversions:
        df = convert_types(df, conversions)
    return df
