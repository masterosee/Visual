
# utils/pdf_generator.py
import streamlit as st
import os
import base64

def create_pdf_download_section():
    """
    Crée une section complète avec bouton de téléchargement PDF
    À ajouter à la fin de menu_app.py
    """
    
    st.markdown("---")
    
    # Section stylisée pour le PDF
    st.markdown("""
    <style>
    .pdf-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .pdf-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .pdf-subtitle {
        font-size: 16px;
        margin-bottom: 20px;
        opacity: 0.9;
    }
    .download-btn {
        background: #FFD700;
        color: black;
        padding: 15px 30px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #FFD700;
        font-size: 16px;
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    .download-btn:hover {
        background: #FFE066;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête PDF
    st.markdown("""
    <div class="pdf-container">
        <div class="pdf-title">📕 MANUEL COMPLET</div>
        <div class="pdf-subtitle">Téléchargez le guide d'utilisation détaillé au format PDF</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chemins possibles pour le PDF
    pdf_paths = [
        "assets/manuel_visualisation_universelle.pdf",
        "manuel_visualisation_universelle.pdf", 
        "./assets/manuel_visualisation_universelle.pdf",
        "../assets/manuel_visualisation_universelle.pdf"
    ]
    
    pdf_found = None
    pdf_bytes = None
    
    # Chercher le PDF dans différents emplacements
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                pdf_found = pdf_path
                break
            except Exception as e:
                continue
    
    if pdf_found and pdf_bytes:
        # PDF trouvé - créer le bouton de téléchargement
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        
        st.markdown(
            f"""
            <div style='text-align: center; margin: 20px 0;'>
                <a href="data:application/pdf;base64,{b64_pdf}" 
                   download="manuel_visualisation_universelle.pdf"
                   class="download-btn">
                   ⬇️ TÉLÉCHARGER LE MANUEL PDF
                </a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.success("✅ Manuel disponible ! Cliquez sur le bouton jaune ci-dessus pour télécharger.")
        st.info(f"📁 Fichier trouvé : {pdf_found}")
        
    else:
        # PDF non trouvé - instructions
        st.warning("📄 Le fichier PDF n'a pas été trouvé.")
        
        with st.expander("📋 Instructions pour ajouter le PDF"):
            st.markdown("""
            ### Comment ajouter le manuel PDF :
            
            1. **Créez le dossier `assets`** dans votre projet :
            ```
            visualisation_universelle/
            ├── assets/                    ← Créez ce dossier
            │   └── manuel_visualisation_universelle.pdf
            ├── menu_app.py
            └── ...
            ```
            
            2. **Placez votre PDF** dans le dossier `assets/`
            
            3. **Redémarrez** l'application Streamlit
            
            4. **Le bouton apparaîtra automatiquement** ✅
            
            ### Méthodes pour créer le PDF :
            - **Word/Google Docs** : Créez un document et exportez en PDF
            - **HTML vers PDF** : Créez un fichier HTML et imprimez en PDF via le navigateur
            - **Outils en ligne** : Utilisez un convertisseur HTML vers PDF
            """)
        
        # Bouton de test avec PDF minimal
        st.info("🔄 En attendant, vous pouvez tester avec un PDF minimal :")
        
        if st.button("🧪 Tester avec PDF de démonstration", key="test_pdf"):
            try:
                from fpdf import FPDF
                # Créer un PDF minimal de test
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Manuel Visualisation Universelle", ln=1, align='C')
                pdf.cell(200, 10, txt="Version de test - PDF fonctionnel", ln=1, align='C')
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                b64_test = base64.b64encode(pdf_output).decode()
                st.markdown(
                    f"""
                    <div style='text-align: center; margin: 20px 0;'>
                        <a href="data:application/pdf;base64,{b64_test}" 
                        download="manuel_test.pdf"
                        class="download-btn">
                        ⬇️ TÉLÉCHARGER PDF DE TEST
                        </a>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.success("✅ PDF de test généré !")
                
            except ImportError:
                st.error("❌ Module FPDF non installé. Exécutez : `pip install fpdf`")

def get_pdf_download_code():
    """
    Retourne le code à ajouter à menu_app.py
    """
    return """
    # === SECTION TÉLÉCHARGEMENT PDF ===
    from utils.pdf_generator import create_pdf_download_section
    create_pdf_download_section()
    """

# Test du module
if __name__ == "__main__":
    create_pdf_download_section()