
import pandas as pd
import os

USER_DB = "users.csv"


def init_user_db():
    """Crée le fichier users.csv s'il n'existe pas."""
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=["username", "password_hash", "is_approved"])
        df.to_csv(USER_DB, index=False)


def load_users() -> pd.DataFrame:
    """Charge les utilisateurs depuis users.csv."""
    init_user_db()
    return pd.read_csv(USER_DB)


def save_users(df: pd.DataFrame):
    """Sauvegarde les utilisateurs dans users.csv."""
    df.to_csv(USER_DB, index=False)
