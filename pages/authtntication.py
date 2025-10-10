
import streamlit as st
from core.auth import register_user, authenticate_user
from utils.db import load_users, save_users

st.set_page_config(
    page_title="Authentification", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======== STYLE CSS MOBILE-FRIENDLY ========
st.markdown("""
<style>
    /* Background principal */
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style pour le contenu principal - MOBILE FIRST */
    .block-container {
        background-color: white;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Style du titre */
    .css-10trblm {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 28px !important;
    }
    
    /* Style des radio buttons - MOBILE */
    .stRadio > div {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    /* Style des inputs - GRANDS SUR MOBILE */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 15px !important;
        font-size: 16px !important;
    }
    
    /* Style des boutons - PLEINE LARGEUR MOBILE */
    .stButton > button {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 15px 25px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        font-size: 18px !important;
    }
    
    .stButton > button:hover {
        background-color: #764ba2 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* ======== STYLES MOBILE SPECIFIQUES ======== */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem !important;
            margin-top: 0.5rem !important;
        }
        
        .css-10trblm {
            font-size: 24px !important;
            margin-bottom: 1rem !important;
        }
        
        .stTextInput > div > div > input {
            padding: 18px !important;
            font-size: 18px !important;
        }
        
        .stButton > button {
            padding: 18px !important;
            font-size: 20px !important;
        }
        
        .stRadio > div {
            padding: 15px !important;
        }
        
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        .main {
            width: 100% !important;
            padding: 0 !important;
        }
    }
    
    @media (max-width: 480px) {
        .block-container {
            padding: 1rem !important;
            border-radius: 10px !important;
        }
        
        .css-10trblm {
            font-size: 22px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Portail d'accès")

st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <p style='color: #666; font-size: 14px;'>
    📱 <strong>Version mobile</strong> - Tous les champs sont adaptés aux écrans tactiles
    </p>
</div>
""", unsafe_allow_html=True)

menu = st.radio("Choisir une action", ["Connexion", "Inscription", "Approbation (admin)"])
# Connexion - OPTIMISÉ MOBILE
if menu == "Connexion":
    st.subheader("Se connecter")
    
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        submitted = st.form_submit_button("Se connecter")
        
        if submitted:
            if not username or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                result = authenticate_user(username, password)
                if result == "OK":
                    st.session_state['user'] = username
                    st.success(f"✅ Connexion réussie ! Bienvenue {username}")
                    
                    st.markdown("---")
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                        <h3>🚀 Connexion réussie !</h3>
                        <p><strong>Pour accéder à l'application :</strong></p>
                        <p>👉 <strong>Retournez à la page principale</strong></p>
                        <p>👉 <strong>Ou cliquez sur le menu en haut à gauche</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.warning(f"⚠️ {result}")

# Inscription - OPTIMISÉ MOBILE
elif menu == "Inscription":
    st.subheader("Créer un compte")
    
    with st.form("register_form"):
        new_user = st.text_input("Nom d'utilisateur", placeholder="Choisissez un nom d'utilisateur")
        new_pass = st.text_input("Mot de passe", type="password", placeholder="Choisissez un mot de passe")
        submitted = st.form_submit_button("S'inscrire")
        
        if submitted:
            if not new_user or not new_pass:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                msg = register_user(new_user, new_pass)
                st.info(f"ℹ️ {msg}")

# Approbation manuelle - OPTIMISÉ MOBILE
elif menu == "Approbation (admin)":
    st.subheader("Gestion des approbations")
    
    if st.session_state.get('user') == 'admin':
        users = load_users()
        pending = users[users['is_approved'] == False]
        
        if pending.empty:
            st.success("✅ Aucun utilisateur en attente d'approbation")
        else:
            st.write(f"**Utilisateurs en attente : {len(pending)}**")
            
            for i, row in pending.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        st.write(f"👤 **{row['username']}**")
                    with col2:
                        if st.button(f"✅ Approuver", key=row['username']):
                            users.at[i, 'is_approved'] = True
                            save_users(users)
                            st.success(f"✅ {row['username']} approuvé !")
                            st.rerun()
    else:
        st.warning("⛔ Accès réservé à l'administrateur")

# Création du compte admin - OPTIMISÉ MOBILE
users = load_users()
if "admin" not in users["username"].str.lower().values:
    st.markdown("---")
    st.subheader("🛠️ Configuration initiale")
    st.info("Première utilisation : créez le compte administrateur")
    
    with st.form("create_admin"):
        admin_user = st.text_input("Nom d'utilisateur admin", value="admin")
        admin_pass = st.text_input("Mot de passe admin", type="password", placeholder="Choisissez un mot de passe sécurisé")
        submitted = st.form_submit_button("Créer le compte admin")
        
        if submitted:
            if not admin_pass:
                st.error("❌ Veuillez définir un mot de passe")
            else:
                users = load_users()
                if admin_user.lower() in users['username'].str.lower().values:
                    st.warning("⚠️ Le compte admin existe déjà.")
                else:
                    register_user(admin_user, admin_pass)
                    users = load_users()
                    users.loc[users['username'].str.lower() == admin_user.lower(), 'is_approved'] = True
                    save_users(users)
                    st.success("✅ Compte admin créé et approuvé !")
                    st.info("🔐 Vous pouvez maintenant vous connecter en tant qu'admin")
