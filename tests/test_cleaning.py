# tests/test_cleaning.py

import sys, os
# Ajoute la racine du projet au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from utils import cleaning

def run_tests():
    # Charger ton dataset "sale"
    df = pd.read_csv("dataset_sale.csv", encoding="latin1")



    print("=== Dataset brut ===")
    print(df)

    # 1. Nettoyage des colonnes
    df1 = cleaning.clean_columns(df)
    print("\n=== Colonnes nettoyées ===")
    print(df1.head())

    # 2. Gestion des valeurs manquantes (remplacement par la moyenne)
    df2 = cleaning.handle_missing(df1, strategy="mean")
    print("\n=== Valeurs manquantes gérées ===")
    print(df2.head())

    # 3. Suppression des doublons
    df3 = cleaning.remove_duplicates(df2)
    print("\n=== Doublons supprimés ===")
    print(df3.head())

    # 4. Pipeline complet
    df4 = cleaning.prepare_dataset(df, missing_strategy="mean")
    print("\n=== Pipeline complet ===")
    print(df4.head())

if __name__ == "__main__":
    run_tests()
