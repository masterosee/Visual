
import streamlit as st
from core.auth import register_user, authenticate_user
from utils.db import load_users, save_users

st.set_page_config(page_title="Authentification", layout="centered")

# ======== STYLE CSS POUR L'AUTHENTIFICATION ========
st.markdown("""
<style>
    /* Background principal de l'authentification */
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style pour le contenu principal */
    .block-container {
        background-color: white;
        border-radius: 15px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Style du titre */
    .css-10trblm {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Style des radio buttons */
    .stRadio > div {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    /* Style des inputs */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Style des boutons */
    .stButton > button {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #764ba2 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Style des messages */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 15px;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
    }
    
    .stInfo {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Style du formulaire admin */
    .stForm {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

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
            st.success(f"✅ Connexion réussie ! Bienvenue {username}")
            
            # ✅ MESSAGE DE NAVIGATION SIMPLE
            st.markdown("---")
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                <h3>🚀 Connexion réussie !</h3>
                <p><strong>Pour accéder à l'application :</strong></p>
                <p>👉 <strong>Cliquez sur "menu app" dans le menu de gauche</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
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
