import unicodedata
import urllib.parse
import requests

# ==========================================
# 1. Funcție curățare diacritice și trimitere WhatsApp
# ==========================================
def remove_diacritics(text):
    """Elimină diacriticele românești pentru a preveni erorile API."""
    if not text:
        return ""
    # Normalizează caracterele Unicode și elimină semnele diacritice (categoria 'Mn')
    nfd_form = unicodedata.normalize('NFD', text)
    without_diacritics = "".join([c for c in nfd_form if unicodedata.category(c) != 'Mn'])
    
    # Înlocuiri suplimentare de siguranță pentru litere românești specifice
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
        if response.status_code == 200:
            print("Mesaj WhatsApp trimis cu succes!")
        else:
            print(f"Eroare API CallMeBot: {response.status_code}")
    except Exception as e:
        print(f"Eroare de rețea: {e}")

# Exemplu de apel:
# send_whatsapp_notification("35796005530", "Programarea a fost salvată cu succes!", "9926434")


# ==========================================
# 2. Exemplu pentru Interfață (Streamlit UI)
# ==========================================
def render_ui_example(st, current_user, all_stylists, all_statuses):
    """Exemplu de componente pentru filtre și interfață în Python/Streamlit"""
    
    # A. Filtre Multi-select redenumite
    selected_stylists = st.multiselect("Alege Stilist", options=all_stylists, default=[current_user])
    selected_statuses = st.multiselect("Alege Status Programare", options=all_statuses)
    
    # B. Notificare de succes vizibilă pe ecran (în Streamlit apare automat sus/în fluxul paginii)
    # st.success("Modificarea sau salvarea s-a efectuat cu succes!")
