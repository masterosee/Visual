import matplotlib.pyplot as plt
import pandas as pd

def plot_time_series(df, x_col, y_col, title="Série temporelle", xlabel=None, ylabel=None):
    """
    Trace une série temporelle simple.
    - df : DataFrame Pandas
    - x_col : colonne pour l’axe des X (dates ou périodes)
    - y_col : colonne pour l’axe des Y (valeurs numériques)
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
    - x_col : colonne pour l’axe des X (dates ou périodes)
    - y_cols : liste de colonnes pour l’axe des Y
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
