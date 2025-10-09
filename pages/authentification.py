import streamlit as st
from core.auth import register_user, authenticate_user
from utils.db import load_users, save_users

st.set_page_config(page_title="Authentification", layout="centered")

st.title("🔐 Portail d'accès")

menu = st.radio("Choisir une action", ["Connexion", "Inscription", "Approbation (admin)"])

# Connexion
if menu == "Connexion":
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        result = authenticate_user(username, password)
        if result == "OK":
            st.session_state['user'] = username
            st.success(f"Bienvenue {username}")
        else:
            st.warning(result)

# Inscription
elif menu == "Inscription":
    new_user = st.text_input("Nom d'utilisateur")
    new_pass = st.text_input("Mot de passe", type="password")
    if st.button("S'inscrire"):
        msg = register_user(new_user, new_pass)
        st.info(msg)

# Approbation manuelle
elif menu == "Approbation (admin)":
    if st.session_state.get('user') == 'admin':
        users = load_users()
        pending = users[users['is_approved'] == False]
        st.subheader("Utilisateurs en attente")
        for i, row in pending.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"👤 {row['username']}")
            with col2:
                if st.button(f"Approuver {row['username']}", key=row['username']):
                    users.at[i, 'is_approved'] = True
                    save_users(users)
                    st.success(f"{row['username']} approuvé.")
    else:
        st.warning("Accès réservé à l'administrateur.")


users = load_users()
if "admin" in users["username"].str.lower().values:
    st.stop()

st.subheader("🛠️ Créer le compte admin")

with st.form("create_admin"):
    admin_user = st.text_input("Nom d'utilisateur admin", value="admin")
    admin_pass = st.text_input("Mot de passe admin", type="password")
    submitted = st.form_submit_button("Créer admin")

    if submitted:
        users = load_users()
        if admin_user.lower() in users['username'].str.lower().values:
            st.warning("⚠️ Le compte admin existe déjà.")
        else:
            register_user(admin_user, admin_pass)
            users = load_users()
            users.loc[users['username'].str.lower() == admin_user.lower(), 'is_approved'] = True
            save_users(users)
            st.success("✅ Compte admin créé et approuvé.")
