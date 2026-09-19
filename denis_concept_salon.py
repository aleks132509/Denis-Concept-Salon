import streamlit as st
import pandas as pd
import unicodedata
import urllib.parse
import requests
from datetime import datetime

# Configurarea paginii
st.set_page_config(page_title="Denis Concept Salon", page_icon="💇‍♀️", layout="wide")

# ==========================================
# 1. CONFIGURARE & FUNCȚIE WHATSAPP (CallMeBot)
# ==========================================
WHATSAPP_PHONE = "35796005530"
WHATSAPP_APIKEY = "9926434"

def remove_diacritics(text):
    """Elimină diacriticele românești pentru a preveni erorile API CallMeBot."""
    if not text:
        return ""
    nfd_form = unicodedata.normalize('NFD', text)
    without_diacritics = "".join([c for c in nfd_form if unicodedata.category(c) != 'Mn'])
    
    replacements = {
        'ă': 'a', 'Ă': 'A',
        'â': 'a', 'Â': 'A',
        'î': 'i', 'Î': 'I',
        'ș': 's', 'Ș': 'S',
        'ț': 't', 'Ț': 'T'
    }
    for k, v in replacements.items():
        without_diacritics = without_diacritics.replace(k, v)
        
    return without_diacritics

def send_whatsapp_notification(phone, raw_text, api_key):
    """Trimite mesajul prin CallMeBot fără diacritice și cu URL Encoding corect."""
    clean_text = remove_diacritics(raw_text)
    encoded_text = urllib.parse.quote(clean_text)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_text}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"Eroare de rețea WhatsApp: {e}")
        return False

# ==========================================
# 2. DATE SIMULATE (Bază de date locală/sesiune)
# ==========================================
if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {"id": 1, "nr": "nr 1", "data": "2026-06-01", "ora": "10:00", "serviciu": "Tuns", "stilist": "Denis", "status": "Confirmat"},
        {"id": 2, "nr": "nr 2", "data": "2026-06-01", "ora": "11:30", "serviciu": "Vopsit", "stilist": "Maria", "status": "În așteptare"},
        {"id": 3, "nr": "nr 3", "data": "2026-06-02", "ora": "09:00", "serviciu": "Coafat", "stilist": "Denis", "status": "Finalizat"},
    ]

if "catalog" not in st.session_state:
    st.session_state.catalog = [
        {"id": 1, "nume": "Tuns Stil", "stilist": "Denis", "pret": 100},
        {"id": 2, "nume": "Vopsit Profesional", "stilist": "Maria", "pret": 250},
    ]

if "recenzii" not in st.session_state:
    st.session_state.recenzii = [
        {"id": 1, "stilist": "Denis", "client": "Ana", "comentariu": "Foarte mulțumită!", "rating": 5},
        {"id": 2, "stilist": "Maria", "client": "Ioana", "comentariu": "Super servicii!", "rating": 5},
    ]

# ==========================================
# 3. INTERFAȚA UTILIZATORULUI (UI)
# ==========================================
st.sidebar.title("Meniu Navigare")
user_role = st.sidebar.selectbox("Selectează Rolul", ["Client", "Stilist / Admin (Denis)", "Stilist (Maria)"])

st.title("Denis Concept Salon - Panou de Control")

# ------------------------------------------
# A. SECȚIUNEA CLIENT (Fără ID, fără Nul, fără Număr programare)
# ------------------------------------------
if user_role == "Client":
    st.header("Programările Mele Curente")
    st.info("Aici puteți vizualiza detaliile programării dumneavoastră.")
    
    client_view_data = []
    for app in st.session_state.appointments:
        client_view_data.append({
            "Data": app["data"],
            "Ora": app["ora"],
            "Serviciu": app["serviciu"],
            "Stilist": app["stilist"]
        })
    
    st.table(pd.DataFrame(client_view_data))

# ------------------------------------------
# B. SECȚIUNEA STILIST / ADMIN
# ------------------------------------------
else:
    current_admin_stylist = "Denis" if "Denis" in user_role else "Maria"
    st.subheader(f"Bun venit, {current_admin_stylist}!")

    tab1, tab2, tab3, tab4 = st.tabs(["Programări & Filtre", "Gestiune & Catalog", "Recenzii", "Test WhatsApp"])

    # --- TAB 1: Programări cu Filtre Multi-Select Redenumite ---
    with tab1:
        st.markdown("### Filtre Programări")
        
        all_stylists = list(set([a["stilist"] for a in st.session_state.appointments]))
        all_statuses = list(set([a["status"] for a in st.session_state.appointments]))
        
        selected_stylists = st.multiselect("Alege Stilist", options=all_stylists, default=[current_admin_stylist])
        selected_statuses = st.multiselect("Alege Status Programare", options=all_statuses, default=all_statuses)
        
        filtered_apps = [
            app for app in st.session_state.appointments 
            if app["stilist"] in selected_stylists and app["status"] in selected_statuses
        ]
        
        st.dataframe(pd.DataFrame(filtered_apps))
        
        if st.button("Salvează Modificări Programări"):
            st.success("Modificarea sau salvarea s-a efectuat cu succes!")
            send_whatsapp_notification(WHATSAPP_PHONE, "Modificarea programarii a fost salvata cu succes!", WHATSAPP_APIKEY)

    # --- TAB 2: Gestiune & Catalog (Default utilizator curent + Opțiune alții) ---
    with tab2:
        st.markdown("### Catalog Servicii")
        
        available_catalog_stylists = list(set([c["stilist"] for c in st.session_state.catalog]))
        view_catalog_stylists = st.multiselect(
            "Alege Stilist / Admin pentru Catalog", 
            options=available_catalog_stylists, 
            default=[current_admin_stylist]
        )
        
        filtered_catalog = [c for c in st.session_state.catalog if c["stilist"] in view_catalog_stylists]
        st.dataframe(pd.DataFrame(filtered_catalog))
        
        with st.form("add_catalog_form"):
            st.write("Adaugă element nou în catalog")
            new_nume = st.text_input("Nume Serviciu")
            new_pret = st.number_input("Preț", min_value=0.0)
            submitted = st.form_submit_button("Adaugă Serviciu")
            if submitted:
                st.session_state.catalog.append({"id": len(st.session_state.catalog)+1, "nume": new_nume, "stilist": current_admin_stylist, "pret": new_pret})
                st.success("Modificarea sau salvarea s-a efectuat cu succes!")

    # --- TAB 3: Recenzii ---
    with tab3:
        st.markdown("### Recenzii Primite")
        
        view_reviews_stylists = st.multiselect(
            "Alege Stilist pentru Recenzii", 
            options=all_stylists, 
            default=[current_admin_stylist]
        )
        
        filtered_reviews = [r for r in st.session_state.recenzii if r["stilist"] in view_reviews_stylists]
        st.dataframe(pd.DataFrame(filtered_reviews))

    # --- TAB 4: Test Trimis Mesaj WhatsApp ---
    with tab4:
        st.markdown("### Verificare Conexiune WhatsApp API")
        st.write("Folosit pentru testarea trimiterii automate către telefonul +35796005530.")
        
        test_message = st.text_input("Mesaj de trimis", "Salvarea s-a efectuat cu succes!")
        if st.button("Trimite Mesaj WhatsApp acum"):
            success = send_whatsapp_notification(WHATSAPP_PHONE, test_message, WHATSAPP_APIKEY)
            if success:
                st.success("Mesajul WhatsApp a fost trimis cu succes (fără diacritice)!")
            else:
                st.error("Eroare la trimiterea mesajului WhatsApp. Verifică conexiunea sau cheia API.")
