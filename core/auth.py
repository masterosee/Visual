
import bcrypt
import pandas as pd
from utils.db import load_users, save_users, init_user_db

# Initialise le fichier users.csv s'il n'existe pas
init_user_db()


def hash_password(password):
    """Hash sécurisé du mot de passe."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed):
    """Vérifie si le mot de passe correspond au hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(username: str, password: str) -> str:
    """Inscrit un nouvel utilisateur en attente d'approbation."""
    username = username.strip().lower()
    users = load_users()

    # Vérifie si le nom existe déjà (insensible à la casse)
    if username in users['username'].str.lower().values:
        return "Nom d'utilisateur déjà pris."

    new_user = {
        'username': username,
        'password_hash': hash_password(password),
        'is_approved': False
    }

    users = pd.concat([users, pd.DataFrame([new_user])], ignore_index=True)
    save_users(users)
    return "Inscription enregistrée. En attente d’approbation."


def authenticate_user(username: str, password: str) -> str:
    """Authentifie un utilisateur si approuvé."""
    username = username.strip().lower()
    users = load_users()

    user = users[users['username'].str.lower() == username]
    if user.empty:
        return "Utilisateur inconnu."

    if not user.iloc[0]['is_approved']:
        return "Compte en attente d’approbation."

    if check_password(password, user.iloc[0]['password_hash']):
        return "OK"

    return "Mot de passe incorrect."
