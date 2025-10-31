import streamlit as st
from core.auth import register_user, authenticate_user
from utils.db import load_users, save_users

st.set_page_config(page_title="Authentification", layout="centered")

st.title("🔐 Portail d'accès")

# ✅ Vérification si l'utilisateur est déjà connecté et approuvé
if 'user' in st.session_state:
    users = load_users()
    user_row = users[users['username'].str.lower() == st.session_state['user'].lower()]
    
    if not user_row.empty and user_row.iloc[0]['is_approved']:
        # Redirection automatique si déjà connecté et approuvé
        st.success(f"✅ Déjà connecté en tant que {st.session_state['user']}")
        st.info("Redirection automatique vers l'application...")
        
        # Bouton de redirection manuelle
        if st.button("🚀 Accéder maintenant à l'application", type="primary"):
            st.switch_page("../menu_app.py")
        
        # Redirection automatique
        import time
        time.sleep(3)
        st.switch_page("../menu_app.py")
        st.stop()

menu = st.radio("Choisir une action", ["Connexion", "Inscription", "Approbation (admin)"])

# Connexion
if menu == "Connexion":
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        result = authenticate_user(username, password)
        if result == "OK":
            st.session_state['user'] = username
            st.success(f"✅ Connexion réussie ! Bienvenue {username}")
            
            # ✅ REDIRECTION AUTOMATIQUE APRÈS LOGIN
            st.info("Redirection vers l'application...")
            
            import time
            time.sleep(2)
            
            # Redirection vers la page principale
            st.switch_page("../menu_app.py")
            
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
                    st.rerun()
    else:
        st.warning("Accès réservé à l'administrateur.")

# Création du compte admin (si nécessaire)
users = load_users()
if "admin" not in users["username"].str.lower().values:
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