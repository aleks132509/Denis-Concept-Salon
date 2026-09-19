import os
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import urllib.parse
import urllib.request

# ==========================================
# CONFIGURARE PAGINĂ & DESIGN SALON DE LUX
# ==========================================
st.set_page_config(
    page_title="Denis Concept Salon | Luxury Experience",
    layout="wide",
    page_icon="✂️",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #090a0f !important;
        color: #f3f4f6 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .salon-card {
        background: linear-gradient(135deg, #131722 0%, #1a202c 100%);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(212, 175, 55, 0.25);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-val { font-size: 28px; font-weight: 800; color: #e5c158; letter-spacing: 0.5px; }
    .metric-lbl { font-size: 11px; color: #9ca3af; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
    .role-tag { background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%); color: #090a0f; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
    .overlap-alert { background-color: rgba(127, 29, 29, 0.85); color: #fca5a5; padding: 14px; border-radius: 10px; border: 1px solid #ef4444; font-weight: 600; margin-bottom: 12px;}
    .success-alert { background-color: rgba(6, 78, 59, 0.95); color: #6ee7b7; padding: 14px; border-radius: 10px; border: 1px solid #10b981; font-weight: 600; margin-bottom: 12px;}
    .info-alert { background-color: rgba(30, 58, 138, 0.85); color: #93c5fd; padding: 14px; border-radius: 10px; border: 1px solid #3b82f6; font-weight: 600; margin-bottom: 12px;}
    
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
        margin: 6px 0;
        transition: all 0.3s ease;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    .whatsapp-btn:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.6);
        color: white !important;
    }
    
    .marquee-container {
        overflow: hidden;
        white-space: nowrap;
        background: linear-gradient(90deg, #131722, #1a202c, #131722);
        padding: 14px 0;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.35);
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .marquee-content {
        display: inline-block;
        animation: marquee 25s linear infinite;
        -webkit-animation: marquee 25s linear infinite;
        animation-play-state: running !important;
        -webkit-animation-play-state: running !important;
        color: #f3f4f6;
        font-size: 14px;
        font-weight: 500;
        will-change: transform;
        transform: translateZ(0);
    }
    .marquee-content span {
        margin-right: 60px;
        color: #e5c158;
    }
    @keyframes marquee {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-50%); }
    }
    @-webkit-keyframes marquee {
        0% { -webkit-transform: translateX(0%); }
        100% { -webkit-transform: translateX(-50%); }
    }

    .stButton>button {
        background: linear-gradient(135deg, #e5c158 0%, #c5a059 100%) !important;
        color: #090a0f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(212, 175, 55, 0.5) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

def trigger_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ==========================================
# GESTIUNE FIȘIERE PERSISTENTE & DATE
# ==========================================
PROG_FILE = "programari_denis_concept.csv"
SERV_FILE = "servicii_denis_concept.csv"
USER_FILE = "utilizatori_denis_concept.csv"
REV_FILE = "recenzii_denis_concept.csv"
SALON_WHATSAPP = "+35796005530"

def init_csvs():
    today_str = date.today().strftime("%Y-%m-%d")
    future_str = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    if not os.path.exists(PROG_FILE):
        df_p = pd.DataFrame([
            {"Nr. Programare": 1, "Dată": today_str, "Ora Start": "10:00", "Ora Sfârșit": "10:45", "Client": "Alex", "Telefon": "+40722000000", "Serviciu": "Tuns + Barbă Fade", "Stilist": "Adrian", "Preț": 90, "Durată": 45, "Status": "Confirmat", "Observații": "Test programare Alex", "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""},
            {"Nr. Programare": 2, "Dată": future_str, "Ora Start": "11:30", "Ora Sfârșit": "12:30", "Client": "Ionuț", "Telefon": "+40733111222", "Serviciu": "Tuns Lung & Coafat", "Stilist": "Andreea", "Preț": 120, "Durată": 60, "Status": "Confirmat", "Observații": "Test programare Ionuț", "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""}
        ])
        df_p.to_csv(PROG_FILE, index=False)
    else:
        df_p = pd.read_csv(PROG_FILE)
        if "ID" in df_p.columns and "Nr. Programare" not in df_p.columns:
            df_p.rename(columns={"ID": "Nr. Programare"}, inplace=True)
        cols_needed = {"Nr. Programare": 1, "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""}
        for col, default_val in cols_needed.items():
            if col not in df_p.columns:
                df_p[col] = default_val
        df_p["Status Modificare"] = df_p["Status Modificare"].replace(["Niciuna", "nan", "NaN"], "")
        df_p.to_csv(PROG_FILE, index=False)
    
    if not os.path.exists(SERV_FILE):
        df_s = pd.DataFrame([
            {"Serviciu": "Tuns Clasic Barber", "Preț": 50, "Durată (min)": 30, "Stilist": "Adrian"},
            {"Serviciu": "Tuns + Barbă Fade", "Preț": 90, "Durată (min)": 45, "Stilist": "Adrian"},
            {"Serviciu": "Aranjat Barbă & Contur", "Preț": 40, "Durată (min)": 20, "Stilist": "Adrian"},
            {"Serviciu": "Vopsit Barbă", "Preț": 60, "Durată (min)": 30, "Stilist": "Adrian"},
            {"Serviciu": "Tuns Scurt Dama", "Preț": 70, "Durată (min)": 45, "Stilist": "Andreea"},
            {"Serviciu": "Tuns Lung & Coafat", "Preț": 120, "Durată (min)": 60, "Stilist": "Andreea"},
            {"Serviciu": "Balayage / Decolorare", "Preț": 250, "Durată (min)": 120, "Stilist": "Andreea"},
            {"Serviciu": "Vopsit Rădăcină", "Preț": 100, "Durată (min)": 50, "Stilist": "Andreea"},
        ])
        df_s.to_csv(SERV_FILE, index=False)

    if not os.path.exists(USER_FILE):
        df_u = pd.DataFrame([
            {"Utilizator": "Alex", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "+40722000000", "APIKey": ""},
            {"Utilizator": "Denis", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "+40733000000", "APIKey": ""},
            {"Utilizator": "Adrian", "Parolă": "admin123", "Rol": "Stilist", "Telefon": "+40744111222", "APIKey": ""},
            {"Utilizator": "Andreea", "Parolă": "admin123", "Rol": "Stilist", "Telefon": "+40755222333", "APIKey": ""},
            {"Utilizator": "Ionuț", "Parolă": "client123", "Rol": "Client", "Telefon": "+40733111222", "APIKey": ""},
        ])
        df_u.to_csv(USER_FILE, index=False)
    else:
        df_u = pd.read_csv(USER_FILE, dtype=str)
        if "APIKey" not in df_u.columns:
            df_u["APIKey"] = ""
            df_u.to_csv(USER_FILE, index=False)

    if not os.path.exists(REV_FILE):
        df_r = pd.DataFrame([
            {"ID": 1, "Client": "Alex", "Stilist": "Adrian", "Rating": 5, "Comentariu": "Serviciu impecabil și profesionalism!", "Status": "Aprobat"},
            {"ID": 2, "Client": "Ionuț", "Stilist": "Andreea", "Rating": 5, "Comentariu": "Atmosferă excelentă și atenție la detalii.", "Status": "Aprobat"}
        ])
        df_r.to_csv(REV_FILE, index=False)

init_csvs()

def load_data():
    st.session_state.prog_df = pd.read_csv(PROG_FILE, dtype=str)
    if "ID" in st.session_state.prog_df.columns and "Nr. Programare" not in st.session_state.prog_df.columns:
        st.session_state.prog_df.rename(columns={"ID": "Nr. Programare"}, inplace=True)
    
    for col in ["Nr. Programare", "Preț", "Durată"]:
        if col in st.session_state.prog_df.columns:
            st.session_state.prog_df[col] = pd.to_numeric(st.session_state.prog_df[col], errors="coerce")
    if "Status Modificare" in st.session_state.prog_df.columns:
        st.session_state.prog_df["Status Modificare"] = st.session_state.prog_df["Status Modificare"].replace(["Niciuna", "nan", "NaN"], "")
            
    st.session_state.serv_df = pd.read_csv(SERV_FILE)
    for col in ["Preț", "Durată (min)"]:
        if col in st.session_state.serv_df.columns:
            st.session_state.serv_df[col] = pd.to_numeric(st.session_state.serv_df[col], errors="coerce")
            
    st.session_state.users_df = pd.read_csv(USER_FILE, dtype=str)
    if "APIKey" not in st.session_state.users_df.columns:
        st.session_state.users_df["APIKey"] = ""
        
    st.session_state.rev_df = pd.read_csv(REV_FILE, dtype=str)
    if "Rating" in st.session_state.rev_df.columns:
        st.session_state.rev_df["Rating"] = pd.to_numeric(st.session_state.rev_df["Rating"], errors="coerce")
    if "ID" in st.session_state.rev_df.columns:
        st.session_state.rev_df["ID"] = pd.to_numeric(st.session_state.rev_df["ID"], errors="coerce")

if "prog_df" not in st.session_state:
    load_data()

def save_all():
    st.session_state.prog_df.to_csv(PROG_FILE, index=False)
    st.session_state.serv_df.to_csv(SERV_FILE, index=False)
    st.session_state.users_df.to_csv(USER_FILE, index=False)
    st.session_state.rev_df.to_csv(REV_FILE, index=False)

def format_phone_input(val):
    if not val or pd.isna(val) or str(val).strip() == "" or str(val).strip() == "nan":
        return "+40 "
    clean = "".join(filter(str.isdigit, str(val)))
    if clean.startswith("40"):
        clean = clean[2:]
    elif clean.startswith("0"):
        clean = clean[1:]
    return f"+40 {clean}".strip()

def get_whatsapp_link(phone, text):
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith("0"):
        clean_phone = "4" + clean_phone
    elif not clean_phone.startswith("40") and len(clean_phone) == 9:
        clean_phone = "40" + clean_phone
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/{clean_phone}?text={encoded_text}"

# Funcție CallMeBot optimizată pentru WhatsApp automat
def send_free_automatic_whatsapp(phone, message, apikey):
    try:
        if not apikey or pd.isna(apikey) or str(apikey).strip() == "" or str(apikey).strip() == "nan":
            return False
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if clean_phone.startswith("0"):
            clean_phone = "4" + clean_phone
        elif not clean_phone.startswith("40") and len(clean_phone) == 9:
            clean_phone = "40" + clean_phone
            
        encoded_text = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={apikey.strip()}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as response:
            return response.status == 200
    except Exception as e:
        print("Erore trimitere WhatsApp automat CallMeBot:", e)
        return False

def highlight_status_cells(row):
    styles = []
    for val in row:
        v_str = str(val)
        if v_str in ["Anulat", "Respins"]:
            styles.append('background-color: rgba(127, 29, 29, 0.4); color: #fca5a5; font-weight: bold; text-align: center;')
        elif v_str in ["Efectuat", "Aprobat"]:
            styles.append('background-color: rgba(6, 78, 59, 0.4); color: #6ee7b7; font-weight: bold; text-align: center;')
        elif v_str in ["Confirmat", "În Așteptare"]:
            styles.append('background-color: rgba(120, 80, 20, 0.4); color: #fef08a; font-weight: bold; text-align: center;')
        else:
            styles.append('text-align: center;')
    return styles

def render_marquee_banner():
    rev_aprobate_banner = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
    if not rev_aprobate_banner.empty:
        marquee_items = ""
        for _, r_row in rev_aprobate_banner.iterrows():
            stars = "⭐" * int(float(r_row['Rating']) if pd.notna(r_row['Rating']) else 5)
            marquee_items += f"<span>{stars} <b>{r_row['Client']}</b> despre stilistul <b>{r_row['Stilist']}</b>: \"{r_row['Comentariu']}\"</span>"
        
        st.markdown(f"""
        <div class="marquee-container">
            <div class="marquee-content">
                {marquee_items} &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; {marquee_items}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# SESIUNE & AUTENTIFICARE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

if not st.session_state.logged_in:
    render_marquee_banner()
    
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_auth, _ = st.columns([1, 1.4, 1])
    with col_auth:
        st.markdown("<h1 style='text-align: center; color: #e5c158; font-family: serif; letter-spacing: 2px;'>✂️ Denis Concept Salon</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; text-transform: uppercase; font-size: 12px; letter-spacing: 3px;'>Luxury Hair & Barber Experience</p><br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            u_input = st.text_input("👤 Utilizator / Nume", placeholder="ex: Alex, Ionuț, Adrian")
            p_input = st.text_input("🔑 Parolă", type="password")
            
            if st.button("✨ Intră în Cont", use_container_width=True):
                users = st.session_state.users_df
                match = users[(users["Utilizator"] == u_input) & (users["Parolă"] == p_input)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = u_input
                    st.session_state.role = match.iloc[0]["Rol"]
                    trigger_rerun()
                else:
                    st.error("Utilizator sau parolă incorectă!")
        st.stop()

is_admin = st.session_state.role == "Administrator"
is_stylist = st.session_state.role == "Stilist"
is_admin_or_stylist = is_admin or is_stylist
current_user = st.session_state.user

# ==========================================
# BANNER RULANT (MARQUEE) CU RECENZII
# ==========================================
render_marquee_banner()

# ==========================================
# SIDEBAR / MENIU LATERAL
# ==========================================
st.sidebar.markdown(f"### ✂️ **{current_user}**")
st.sidebar.markdown(f"Rol: <span class='role-tag'>{st.session_state.role}</span>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if not is_admin_or_stylist:
    st.sidebar.markdown("##### 👤 Profilul Meu & Telefon")
    user_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
    current_tel = format_phone_input(user_row.iloc[0]["Telefon"]) if not user_row.empty else "+40 "
    
    with st.sidebar.form("edit_client_phone_form"):
        st.text_input("Nume (Fix)", value=current_user, disabled=True)
        new_phone_input = st.text_input("Număr Telefon", value=current_tel, placeholder="+40 7xxxxxxxx")
        if st.form_submit_button("Salvează Telefonul"):
            formatted_p = format_phone_input(new_phone_input)
            st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == current_user, "Telefon"] = formatted_p
            save_all()
            st.sidebar.success("Telefon actualizat!")
            trigger_rerun()
    st.sidebar.markdown("---")
    
    wa_support_link = get_whatsapp_link(SALON_WHATSAPP, f"Salut, sunt {current_user} și doresc informații despre Denis Concept Salon.")
    st.sidebar.markdown(f"""
    <div style="text-align: center; margin-bottom: 15px;">
        <a href="{wa_support_link}" target="_blank" class="whatsapp-btn" style="width: 100%; justify-content: center;">
            💬 Contact Salon WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("🚪 Deconectare", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    trigger_rerun()

st.sidebar.markdown("---")

if is_admin_or_stylist:
    df_prog_all = st.session_state.prog_df
    pending_modifs = df_prog_all[df_prog_all["Status Modificare"] == "În Așteptare"]
    if not pending_modifs.empty:
        st.markdown(f"""
        <div class="overlap-alert">
            🔔 <b>ATENȚIE!</b> Există <b>{len(pending_modifs)}</b> cereri de modificare programare în așteptarea aprobării! Verifică tabul <b>⚙️ Gestiune & Aprobări</b>.
        </div>
        """, unsafe_allow_html=True)

def check_overlap(stilist, data_str, ora_start_str, durata_min, exclude_nr=None):
    try:
        t_start = datetime.strptime(ora_start_str, "%H:%M").time()
        start_dt = datetime.combine(datetime.strptime(data_str, "%Y-%m-%d"), t_start)
        end_dt = start_dt + timedelta(minutes=int(durata_min))
    except:
        return False, []

    df = st.session_state.prog_df
    conflicts = []
    
    for idx, row in df.iterrows():
        if exclude_nr is not None and str(row.get("Nr. Programare")) == str(exclude_nr):
            continue
        if row["Stilist"] == stilist and row["Dată"] == data_str and row["Status"] != "Anulat":
            try:
                ex_start = datetime.strptime(row["Ora Start"], "%H:%M").time()
                ex_end = datetime.strptime(row["Ora Sfârșit"], "%H:%M").time()
                ex_s_dt = datetime.combine(datetime.strptime(row["Dată"], "%Y-%m-%d"), ex_start)
                ex_e_dt = datetime.combine(datetime.strptime(row["Dată"], "%Y-%m-%d"), ex_end)
                
                if start_dt < ex_e_dt and end_dt > ex_s_dt:
                    conflicts.append(row)
            except:
                pass
    return len(conflicts) > 0, conflicts

# ==========================================
# CONFIGURARE TAB-URI ÎN FUNCȚIE DE ROL
# ==========================================
if is_admin:
    tabs = st.tabs([
        "📅 Programări & Calendar", 
        "➕ Adaugă Programare", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii", 
        "📊 Raport Financiar", 
        "⚙️ Setări & Utilizatori"
    ])
elif is_stylist:
    tabs = st.tabs([
        "📅 Programări & Calendar", 
        "➕ Adaugă Programare", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii"
    ])
else:
    tabs = st.tabs([
        "📅 Programează-te", 
        "📜 Istoric Programări", 
        "⭐ Recenzii Salon & Istoricul Meu"
    ])

# ==========================================
# TAB 1: PROGRAMĂRI & CALENDAR (Admin/Stilist) / PROGRAMARE NOUĂ (Client)
# ==========================================
with tabs[0]:
    if is_admin_or_stylist:
        st.markdown("### 📅 Vizualizator Programări & Calendar")
        df_p = st.session_state.prog_df.copy()
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            view_mode = st.selectbox("Vizualizare Perioadă", ["Toate", "Azi", "Mâine", "Săptămâna aceasta", "Săptămâna viitoare", "Luna aceasta", "Programări Viitoare", "Programări Trecute"])
        with col_f2:
            stilisti_opt = ["Toți"] + ["Adrian", "Andreea", "Alex", "Denis"]
            fil_stilist = st.selectbox("Filtru Stilist / Barber", stilisti_opt)
        with col_f3:
            fil_status = st.selectbox("Filtru Status", ["Toate", "Confirmat", "Efectuat", "Anulat"])

        today = date.today()
        if not df_p.empty:
            df_p["Dată_dt"] = pd.to_datetime(df_p["Dată"], errors="coerce")
            
            if view_mode == "Azi":
                df_p = df_p[df_p["Dată"] == str(today)]
            elif view_mode == "Mâine":
                tmr = today + timedelta(days=1)
                df_p = df_p[df_p["Dată"] == str(tmr)]
            elif view_mode == "Săptămâna aceasta":
                start_w = today - timedelta(days=today.weekday())
                end_w = start_w + timedelta(days=6)
                df_p = df_p[(df_p["Dată_dt"].dt.date >= start_w) & (df_p["Dată_dt"].dt.date <= end_w)]
            elif view_mode == "Săptămâna viitoare":
                start_w = today + timedelta(days=(7 - today.weekday()))
                end_w = start_w + timedelta(days=6)
                df_p = df_p[(df_p["Dată_dt"].dt.date >= start_w) & (df_p["Dată_dt"].dt.date <= end_w)]
            elif view_mode == "Luna aceasta":
                df_p = df_p[(df_p["Dată_dt"].dt.year == today.year) & (df_p["Dată_dt"].dt.month == today.month)]
            elif view_mode == "Programări Viitoare":
                df_p = df_p[df_p["Dată_dt"].dt.date >= today]
            elif view_mode == "Programări Trecute":
                df_p = df_p[df_p["Dată_dt"].dt.date < today]

            if fil_stilist != "Toți":
                df_p = df_p[df_p["Stilist"] == fil_stilist]
            if fil_status != "Toate":
                df_p = df_p[df_p["Status"] == fil_status]
            
            if "Dată_dt" in df_p.columns:
                df_p = df_p.drop(columns=["Dată_dt"])

        if not df_p.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Afișate</div><div class="metric-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
            with c2:
                total_incasari_efectuate = df_p[df_p["Status"] == "Efectuat"]["Preț"].sum() if "Preț" in df_p.columns else 0
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Încasări (Efectuate)</div><div class="metric-val">{total_incasari_efectuate} RON</div></div>', unsafe_allow_html=True)
            with c3:
                azi_count = len(df_p[df_p["Dată"] == str(today)])
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Programări Astăzi</div><div class="metric-val">{azi_count}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not df_p.empty:
            df_display_admin = df_p.copy()
            status_cols_admin = [c for c in ["Status", "Status Modificare"] if c in df_display_admin.columns]
            
            if status_cols_admin:
                styled_admin_df = df_display_admin.style.apply(highlight_status_cells, subset=status_cols_admin, axis=1)
                st.dataframe(styled_admin_df, use_container_width=True)
            else:
                st.dataframe(df_display_admin, use_container_width=True)
            
            st.markdown("##### 📱 Acțiuni Rapide WhatsApp pe Dată Selectată")
            col_wa_d1, col_wa_d2 = st.columns(2)
            with col_wa_d1:
                sel_date_wa = st.date_input("Selectează data programării", value=date.today(), key="calendar_wa_picker")
            
            date_str_wa_sel = sel_date_wa.strftime("%Y-%m-%d")
            progs_on_date = df_p[df_p["Dată"] == date_str_wa_sel]
            
            with col_wa_d2:
                if not progs_on_date.empty:
                    selected_prog_wa_nr = st.selectbox(
                        "Alege programarea din această dată", 
                        progs_on_date["Nr. Programare"].tolist(), 
                        format_func=lambda x: f"Nr. {x} - {progs_on_date[progs_on_date['Nr. Programare']==x].iloc[0]['Client']} ({progs_on_date[progs_on_date['Nr. Programare']==x].iloc[0]['Ora Start']})"
                    )
                else:
                    selected_prog_wa_nr = None
                    st.info("Nu există programări în data selectată.")

            if selected_prog_wa_nr:
                row_sel_wa = df_p[df_p["Nr. Programare"] == selected_prog_wa_nr].iloc[0]
                cli_phone_wa = row_sel_wa["Telefon"]
                wa_msg_admin = f"Salut {row_sel_wa['Client']}, te contactăm de la Denis Concept Salon în legătură cu programarea ta din data de {row_sel_wa['Dată']} la ora {row_sel_wa['Ora Start']}."
                wa_link_admin = get_whatsapp_link(cli_phone_wa, wa_msg_admin)
                st.markdown(f'<a href="{wa_link_admin}" target="_blank" class="whatsapp-btn">💬 Trimite WhatsApp către {row_sel_wa["Client"]}</a>', unsafe_allow_html=True)
        else:
            st.info("Nu există programări care să corespundă filtrelor selectate.")

    else:
        # Client Tab 1: Programează-te
        st.markdown("### ➕ Programare Nouă")
        
        if "msg_status" in st.session_state:
            if st.session_state["msg_status"]["type"] == "error":
                st.markdown(f'<div class="overlap-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
            del st.session_state["msg_status"]

        default_tel = "+40 "
        default_stilist_idx = 0
        stilisti_disponibili = ["Adrian", "Andreea", "Alex", "Denis"]

        user_u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
        if not user_u_row.empty and pd.notna(user_u_row.iloc[0]["Telefon"]):
            default_tel = format_phone_input(user_u_row.iloc[0]["Telefon"])

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            client_nume = st.text_input("👤 Nume Client", value=current_user, disabled=True, key="input_client_nuum_c")
            client_tel = st.text_input("📞 Telefon Client (Prefix +40 inclus)", value=default_tel, key="input_client_tel_c", placeholder="+40 7xxxxxxxx")

            p_data = st.date_input("📅 Dată Programare", value=date.today(), key="client_p_date")
            p_stilist = st.selectbox("💈 Stilist / Barber", stilisti_disponibili, index=default_stilist_idx, key="client_prog_stilist")

        with col_in2:
            df_serv_all = st.session_state.serv_df
            serv_filtered = df_serv_all[df_serv_all["Stilist"] == p_stilist]
            if serv_filtered.empty:
                serv_filtered = df_serv_all
                
            st.markdown("##### ✂️ Alege Serviciile Dorite (Poți bifa mai multe)")
            selected_services = []
            total_pret = 0
            total_durata = 0
            
            for idx, s_row in serv_filtered.iterrows():
                s_name = s_row["Serviciu"]
                s_pret = int(float(s_row["Preț"]) if pd.notna(s_row["Preț"]) else 50)
                s_dur = int(float(s_row["Durată (min)"]) if pd.notna(s_row["Durată (min)"]) else 30)
                if st.checkbox(f"{s_name} - {s_pret} RON ({s_dur} min)", key=f"client_srv_bifat_{p_stilist}_{idx}"):
                    selected_services.append(s_name)
                    total_pret += s_pret
                    total_durata += s_dur
            
            st.markdown(f"""
            <div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.3); margin-top: 10px;">
                ⏱️ Durată totală estimată: <b>{total_durata} minute</b><br>
                💰 <b>Total de Plată: {total_pret} RON</b>
            </div>
            """, unsafe_allow_html=True)

            all_possible_slots = [
                "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
                "18:00", "18:30", "19:00", "19:30"
            ]
            
            data_str = p_data.strftime("%Y-%m-%d")
            available_slots = []
            if total_durata > 0:
                for slot in all_possible_slots:
                    has_ov, _ = check_overlap(p_stilist, data_str, slot, total_durata)
                    try:
                        t_s = datetime.strptime(slot, "%H:%M")
                        t_e = t_s + timedelta(minutes=total_durata)
                        if t_e.time() <= datetime.strptime("20:00", "%H:%M").time() and not has_ov:
                            available_slots.append(slot)
                    except:
                        pass

            if not selected_services:
                st.info("ℹ️ Te rugăm să bifezi cel puțin un serviciu pentru a vedea sloturile orare disponibile.")
                p_ora = None
            elif not available_slots:
                st.warning("⚠️ Nu mai există sloturi disponibile pentru data și serviciile selectate la acest stilist.")
                p_ora = None
            else:
                p_ora = st.selectbox("⏰ Alege Slot Orar Disponibil", available_slots, key="client_slot_sel")

            p_obs = st.text_area("📝 Observații / Preferințe", key="client_p_obs")

        try:
            t_start_obj = datetime.strptime(p_ora, "%H:%M") if p_ora else datetime.strptime("10:00", "%H:%M")
            t_end_obj = t_start_obj + timedelta(minutes=total_durata if total_durata > 0 else 30)
            ora_sfarsit = t_end_obj.strftime("%H:%M")
        except:
            ora_sfarsit = "10:30"

        st.markdown("<br>", unsafe_allow_html=True)

        def action_save_client():
            if not client_nume:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog introdu numele clientului!"}
                return
            if not selected_services:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog să bifezi cel puțin un serviciu!"}
                return
            if not p_ora:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog să selectezi un slot orar valid!"}
                return
            
            servicii_str = ", ".join(selected_services)
            new_nr = int(st.session_state.prog_df["Nr. Programare"].max() + 1) if not st.session_state.prog_df.empty and "Nr. Programare" in st.session_state.prog_df.columns and pd.notna(st.session_state.prog_df["Nr. Programare"].max()) else 1
            
            formatted_final_tel = format_phone_input(client_tel)
            new_row = pd.DataFrame([{
                "Nr. Programare": new_nr,
                "Dată": data_str,
                "Ora Start": p_ora,
                "Ora Sfârșit": ora_sfarsit,
                "Client": client_nume,
                "Telefon": formatted_final_tel,
                "Serviciu": servicii_str,
                "Stilist": p_stilist,
                "Preț": total_pret,
                "Durată": total_durata if total_durata > 0 else 30,
                "Status": "Confirmat",
                "Observații": p_obs,
                "Status Modificare": "",
                "Noua Dată": "",
                "Noua Ora": "",
                "Noul Serviciu": "",
                "Motiv Refuz": ""
            }])

            st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
            save_all()
            
            msg = f"✅ Programarea a fost salvată cu succes! Total de plată: **{total_pret} RON**."
            st.session_state["msg_status"] = {"type": "success", "text": msg}
            trigger_rerun()

        st.button("💾 Salvează Programarea", type="primary", use_container_width=True, on_click=action_save_client)

# ==========================================
# TAB 2: ADAUGĂ PROGRAMARE (Admin/Stilist) / ISTORIC PROGRAMĂRI (Client)
# ==========================================
with tabs[1]:
    if is_admin_or_stylist:
        st.markdown("### ➕ Adaugă Programare Nouă (Admin / Stilist - Permite suprapuneri)")
        
        if "msg_status" in st.session_state:
            if st.session_state["msg_status"]["type"] == "error":
                st.markdown(f'<div class="overlap-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
            del st.session_state["msg_status"]

        stilisti_disponibili = ["Adrian", "Andreea", "Alex", "Denis"]

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            client_nume = st.text_input("👤 Nume Client", value="", key="input_client_nuum_admin")
            client_tel = st.text_input("📞 Telefon Client (Prefix +40 inclus)", value="+40 ", key="input_client_tel_admin", placeholder="+40 7xxxxxxxx")

            p_data = st.date_input("📅 Dată Programare", value=date.today(), key="admin_p_date")
            p_stilist = st.selectbox("💈 Stilist / Barber", stilisti_disponibili, key="admin_prog_stilist")

        with col_in2:
            df_serv_all = st.session_state.serv_df
            serv_filtered = df_serv_all[df_serv_all["Stilist"] == p_stilist]
            if serv_filtered.empty:
                serv_filtered = df_serv_all
                
            st.markdown("##### ✂️ Alege Serviciile Dorite (Poți bifa mai multe)")
            selected_services = []
            total_pret = 0
            total_durata = 0
            
            for idx, s_row in serv_filtered.iterrows():
                s_name = s_row["Serviciu"]
                s_pret = int(float(s_row["Preț"]) if pd.notna(s_row["Preț"]) else 50)
                s_dur = int(float(s_row["Durată (min)"]) if pd.notna(s_row["Durată (min)"]) else 30)
                if st.checkbox(f"{s_name} - {s_pret} RON ({s_dur} min)", key=f"admin_srv_bifat_{p_stilist}_{idx}"):
                    selected_services.append(s_name)
                    total_pret += s_pret
                    total_durata += s_dur
            
            st.markdown(f"""
            <div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.3); margin-top: 10px;">
                ⏱️ Durată totală estimată: <b>{total_durata} minute</b><br>
                💰 <b>Total de Plată: {total_pret} RON</b>
            </div>
            """, unsafe_allow_html=True)

            all_possible_slots = [
                "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
                "18:00", "18:30", "19:00", "19:30"
            ]
            
            data_str = p_data.strftime("%Y-%m-%d")
            slot_options_admin = []
            slot_map_admin = {}
            dur_check = total_durata if total_durata > 0 else 30
            for slot in all_possible_slots:
                has_ov, _ = check_overlap(p_stilist, data_str, slot, dur_check)
                if has_ov:
                    label_slot = f"🔴 {slot} - OCUPAT / Suprapunere"
                else:
                    label_slot = f"🟢 {slot} - Disponibil (Liber)"
                slot_options_admin.append(label_slot)
                slot_map_admin[label_slot] = slot

            sel_slot_adm_label = st.selectbox("⏰ Alege Ora Start (🟢 Liber / 🔴 Ocupat - Permite suprapuneri)", slot_options_admin, key="admin_slot_sel")
            p_ora = slot_map_admin[sel_slot_adm_label]

            p_obs = st.text_area("📝 Observații / Preferințe", key="admin_p_obs")

        try:
            t_start_obj = datetime.strptime(p_ora, "%H:%M") if p_ora else datetime.strptime("10:00", "%H:%M")
            t_end_obj = t_start_obj + timedelta(minutes=total_durata if total_durata > 0 else 30)
            ora_sfarsit = t_end_obj.strftime("%H:%M")
        except:
            ora_sfarsit = "10:30"

        st.markdown("<br>", unsafe_allow_html=True)

        def action_save_admin():
            if not client_nume:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog introdu numele clientului!"}
                return
            if not selected_services:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog să bifezi cel puțin un serviciu!"}
                return
            if not p_ora:
                st.session_state["msg_status"] = {"type": "error", "text": "Te rog să selectezi un slot orar valid!"}
                return
            
            servicii_str = ", ".join(selected_services)
            new_nr = int(st.session_state.prog_df["Nr. Programare"].max() + 1) if not st.session_state.prog_df.empty and "Nr. Programare" in st.session_state.prog_df.columns and pd.notna(st.session_state.prog_df["Nr. Programare"].max()) else 1
            
            formatted_final_tel = format_phone_input(client_tel)
            new_row = pd.DataFrame([{
                "Nr. Programare": new_nr,
                "Dată": data_str,
                "Ora Start": p_ora,
                "Ora Sfârșit": ora_sfarsit,
                "Client": client_nume,
                "Telefon": formatted_final_tel,
                "Serviciu": servicii_str,
                "Stilist": p_stilist,
                "Preț": total_pret,
                "Durată": total_durata if total_durata > 0 else 30,
                "Status": "Confirmat",
                "Observații": p_obs,
                "Status Modificare": "",
                "Noua Dată": "",
                "Noua Ora": "",
                "Noul Serviciu": "",
                "Motiv Refuz": ""
            }])

            st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
            save_all()
            
            msg = f"✅ Programarea a fost salvată cu succes! Total de plată: **{total_pret} RON**."
            st.session_state["msg_status"] = {"type": "success", "text": msg}
            trigger_rerun()

        st.button("💾 Salvează Programarea", type="primary", use_container_width=True, on_click=action_save_admin)

    else:
        # Client Tab 2: Istoric Programări
        st.markdown(f"### 📜 Istoricul Programărilor Tale, {current_user}")
        client_name = current_user
        df_p_all = st.session_state.prog_df.copy()
        client_progs = df_p_all[df_p_all["Client"].str.contains(client_name, case=False, na=False)] if not df_p_all.empty else pd.DataFrame()
        
        approved_modifs_client = client_progs[client_progs["Status Modificare"] == "Aprobat"]
        if not approved_modifs_client.empty:
            st.markdown("""
            <div class="success-alert">
                🟢 <b>MODIFICARE APROBATĂ!</b> Solicitarea ta de modificare a fost aprobată cu succes de către stilist!
            </div>
            """, unsafe_allow_html=True)

        if "cancel_success_alert" in st.session_state:
            st.markdown(f"""
            <div class="success-alert">
                {st.session_state["cancel_success_alert"]}
            </div>
            """, unsafe_allow_html=True)
            del st.session_state["cancel_success_alert"]

        if not client_progs.empty:
            df_client_display = client_progs[["Nr. Programare", "Dată", "Ora Start", "Ora Sfârșit", "Serviciu", "Stilist", "Preț", "Durată", "Status", "Status Modificare"]].copy()
            df_client_display["Status Modificare"] = df_client_display["Status Modificare"].apply(lambda x: "" if str(x) in ["Niciuna", "nan", "NaN", ""] else x)
            
            status_cols_client = [c for c in ["Status", "Status Modificare"] if c in df_client_display.columns]
            
            if status_cols_client:
                styled_client_df = df_client_display.style.apply(highlight_status_cells, subset=status_cols_client, axis=1)
                st.dataframe(styled_client_df, use_container_width=True)
            else:
                st.dataframe(df_client_display, use_container_width=True)
            
            st.markdown("---")
            st.markdown("##### ❌ Anulare / ✏️ Modificare Programare Viitoare")
            viitoare = client_progs[(client_progs["Dată"] >= str(date.today())) & (client_progs["Status"] == "Confirmat")]
            
            if not viitoare.empty:
                prog_options = {}
                for _, r in viitoare.iterrows():
                    label = f"Nr. {int(r['Nr. Programare'])} | Data: {r['Dată']} | Ora: {r['Ora Start']} | Serviciu: {r['Serviciu']} | Stilist: {r['Stilist']}"
                    prog_options[label] = int(r['Nr. Programare'])
                
                selected_label = st.selectbox("Alege programarea", list(prog_options.keys()), key="client_hist_sel_prog")
                nr_selected = prog_options[selected_label]
                selected_row = client_progs[client_progs["Nr. Programare"] == nr_selected].iloc[0]

                tab_m1, tab_m2 = st.tabs(["❌ Anulare Programare", "✏️ Modificare Programare"])
                
                with tab_m1:
                    if st.button("Confirmă Anularea Programării", key="client_cancel_btn"):
                        p_dt = datetime.strptime(f"{selected_row['Dată']} {selected_row['Ora Start']}", "%Y-%m-%d %H:%M")
                        ore_ramase = (p_dt - datetime.now()).total_seconds() / 3600
                        
                        if ore_ramase < 24:
                            st.error(f"❌ Anularea nu este permisă! Mai sunt doar {ore_ramase:.1f} ore până la programare (limita minimă este de 24 de ore).")
                        else:
                            stilist_alocat = selected_row["Stilist"]
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Status"] = "Anulat"
                            save_all()
                            
                            stylist_user_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == stilist_alocat]
                            if not stylist_user_row.empty:
                                st_phone = stylist_user_row.iloc[0]["Telefon"]
                                st_apikey = stylist_user_row.iloc[0]["APIKey"]
                                
                                wa_cancel_msg = (
                                    f"🚨 ANULARE PROGRAMARE 🚨\n"
                                    f"Stilist: {stilist_alocat}\n"
                                    f"Client: {current_user}\n"
                                    f"Data: {selected_row['Dată']}\n"
                                    f"Slot: {selected_row['Ora Start']} - {selected_row['Ora Sfârșit']}\n"
                                    f"Serviciu: {selected_row['Serviciu']}"
                                )
                                success_wa = send_free_automatic_whatsapp(st_phone, wa_cancel_msg, st_apikey)
                                if success_wa:
                                    st.session_state["cancel_success_alert"] = "✅ Programarea a fost anulată cu succes, iar înștiințarea a fost trimisă stilistului pe WhatsApp!"
                                else:
                                    st.session_state["cancel_success_alert"] = "✅ Programarea a fost anulată cu succes în sistem!"
                            else:
                                st.session_state["cancel_success_alert"] = "✅ Programarea a fost anulată cu succes în sistem!"

                            trigger_rerun()

                with tab_m2:
                    st.markdown("""
                    <div class="info-alert">
                        ⚠️ <b>ATENȚIE:</b> Alege data dorită, iar sistemul îți va afișa în dropdown <b>doar sloturile orare disponibile</b>. Modificarea necesită aprobare!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.form(f"mod_form_client_{nr_selected}"):
                        new_date = st.date_input("Noua Dată Dorită", value=datetime.strptime(selected_row["Dată"], "%Y-%m-%d").date(), key=f"client_nd_{nr_selected}")
                        stilist_alocat = selected_row["Stilist"]
                        durata_act = int(float(selected_row["Durată"])) if pd.notna(selected_row["Durată"]) else 30
                        
                        all_possible_slots = [
                            "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                            "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
                            "18:00", "18:30", "19:00", "19:30"
                        ]
                        
                        date_str_n = new_date.strftime("%Y-%m-%d")
                        available_slots_mod = []
                        for slot in all_possible_slots:
                            has_ov, _ = check_overlap(stilist_alocat, date_str_n, slot, durata_act, exclude_nr=nr_selected)
                            try:
                                t_s = datetime.strptime(slot, "%H:%M")
                                t_e = t_s + timedelta(minutes=durata_act)
                                if t_e.time() <= datetime.strptime("20:00", "%H:%M").time() and not has_ov:
                                    available_slots_mod.append(slot)
                            except:
                                pass

                        if not available_slots_mod:
                            st.warning("Nu există sloturi disponibile pentru data selectată la acest stilist.")
                            new_ora = ""
                        else:
                            new_ora = st.selectbox("Alege Slotul Orar Disponibil", available_slots_mod, key=f"client_no_{nr_selected}")

                        new_serv = st.text_input("Serviciu / Mențiuni", value=selected_row["Serviciu"], key=f"client_ns_{nr_selected}")
                        
                        if st.form_submit_button("Trimite Solicitarea de Modificare"):
                            if not new_ora:
                                st.error("Te rog selectează un slot orar valid!")
                            else:
                                st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Status Modificare"] = "În Așteptare"
                                st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noua Dată"] = date_str_n
                                st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noua Ora"] = new_ora
                                st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noul Serviciu"] = new_serv
                                save_all()
                                st.session_state["client_mod_sent_success"] = True
                                trigger_rerun()

                if st.session_state.get("client_mod_sent_success", False):
                    st.markdown("""
                    <div class="overlap-alert">
                        🔴 <b>SOLICITARE TRIMISĂ SPRE APROBARE!</b> Cererea ta de modificare a fost înregistrată și trimisă stilistului spre validare.
                    </div>
                    """, unsafe_allow_html=True)
                    del st.session_state["client_mod_sent_success"]
            else:
                st.info("Nu ai programări viitoare active pe care să le poți modifica sau anula.")
        else:
            st.info("Nu ai nicio programare înregistrată momentan în istoric.")

# ==========================================
# TAB 3: GESTIUNE & APROBĂRI (Admin & Stilist)
# ==========================================
if is_admin_or_stylist:
    with tabs[2]:
        st.markdown("### ⚙️ Gestiune, Aprobare Modificări & Programări")
        
        df_all_mgmt = st.session_state.prog_df.copy()
        pending_requests = df_all_mgmt[df_all_mgmt["Status Modificare"] == "În Așteptare"]
        
        if not pending_requests.empty:
            st.markdown("#### 🔔 Cereri de Modificare de la Clienți în Așteptare")
            for _, req_r in pending_requests.iterrows():
                with st.container(border=True):
                    st.markdown(f"**Client:** {req_r['Client']} | **Stilist Asignat:** {req_r['Stilist']} | **Nr. Programare:** {req_r['Nr. Programare']}")
                    st.markdown(f"📅 Data actuală: `{req_r['Dată']} {req_r['Ora Start']}` ➡️ **Solicitat nou:** `{req_r['Noua Dată']} {req_r['Noua Ora']}` | Serviciu nou: *{req_r['Noul Serviciu']}*")
                    
                    col_ap1, col_ap2 = st.columns(2)
                    with col_ap1:
                        if st.button(f"✅ Aprobă Modificarea (Nr. {req_r['Nr. Programare']})", key=f"app_mod_{req_r['Nr. Programare']}"):
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Dată"] = req_r["Noua Dată"]
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Ora Start"] = req_r["Noua Ora"]
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Serviciu"] = req_r["Noul Serviciu"]
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Aprobat"
                            save_all()
                            st.success("Modificarea a fost aprobată cu succes!")
                            trigger_rerun()
                            
                    with col_ap2:
                        motiv_refuz = st.text_input(f"Motiv respingere (opțional) pentru Nr. {req_r['Nr. Programare']}", key=f"motiv_ref_{req_r['Nr. Programare']}")
                        if st.button(f"❌ Respinge Modificarea (Nr. {req_r['Nr. Programare']})", key=f"rej_mod_{req_r['Nr. Programare']}"):
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Respins"
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Motiv Refuz"] = motiv_refuz if motiv_refuz else "Fără motiv specificat"
                            save_all()
                            st.warning("Modificarea a fost respinsă.")
                            trigger_rerun()
            st.markdown("---")

        if not df_all_mgmt.empty:
            col_mg1, col_mg2 = st.columns(2)
            with col_mg1:
                filter_mg_date = st.date_input("📅 Selectează Data pentru Gestionare", value=date.today(), key="mgmt_date_picker")
            
            date_str_mg = filter_mg_date.strftime("%Y-%m-%d")
            filtered_mgmt_progs = df_all_mgmt[df_all_mgmt["Dată"] == date_str_mg]
            
            with col_mg2:
                stilist_filter_mg = st.selectbox("💈 Filtrează după Stilist", ["Toți"] + stilisti_disponibili, key="mgmt_stilist_filter")
            
            if stilist_filter_mg != "Toți":
                filtered_mgmt_progs = filtered_mgmt_progs[filtered_mgmt_progs["Stilist"] == stilist_filter_mg]

            if not filtered_mgmt_progs.empty:
                prog_mgmt_options = {}
                for _, r in filtered_mgmt_progs.iterrows():
                    label = f"⏰ {r['Ora Start']} - {r['Ora Sfârșit']} | Client: {r['Client']} | Serviciu: {r['Serviciu']} | Stilist: {r['Stilist']} | Status: {r['Status']}"
                    prog_mgmt_options[label] = int(r['Nr. Programare'])
                
                sel_mg_label = st.selectbox("Alege Programarea din Intervalul Orar", list(prog_mgmt_options.keys()))
                sel_mg_nr = prog_mgmt_options[sel_mg_label]
                curr_mgmt_row = st.session_state.prog_df[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr].iloc[0]

                with st.container(border=True):
                    st.markdown("##### 📝 Editează Detaliile Programării Selectate")
                    with st.form(f"quick_mod_prog_form_{sel_mg_nr}"):
                        q_client = st.text_input("Nume Client", value=curr_mgmt_row["Client"])
                        q_tel = st.text_input("Telefon", value=format_phone_input(curr_mgmt_row["Telefon"]))
                        q_data = st.date_input("Dată", value=datetime.strptime(curr_mgmt_row["Dată"], "%Y-%m-%d").date())
                        q_ora = st.text_input("Ora Start (HH:MM)", value=curr_mgmt_row["Ora Start"])
                        q_stilist = st.selectbox("Stilist", stilisti_disponibili, index=stilisti_disponibili.index(curr_mgmt_row["Stilist"]) if curr_mgmt_row["Stilist"] in stilisti_disponibili else 0)
                        q_serviciu = st.text_input("Serviciu", value=curr_mgmt_row["Serviciu"])
                        q_pret = st.number_input("Preț (RON)", value=int(float(curr_mgmt_row["Preț"]) if pd.notna(curr_mgmt_row["Preț"]) else 50))
                        q_durata = st.number_input("Durată (min)", value=int(float(curr_mgmt_row["Durată"]) if pd.notna(curr_mgmt_row["Durată"]) else 30))
                        q_status = st.selectbox("Status", ["Confirmat", "Efectuat", "Anulat"], index=["Confirmat", "Efectuat", "Anulat"].index(curr_mgmt_row["Status"]) if curr_mgmt_row["Status"] in ["Confirmat", "Efectuat", "Anulat"] else 0)
                        q_obs = st.text_area("Observații", value=str(curr_mgmt_row["Observații"]) if pd.notna(curr_mgmt_row["Observații"]) else "")
                        
                        if st.form_submit_button("💾 Salvează Modificările"):
                            has_ov, _ = check_overlap(q_stilist, q_data.strftime("%Y-%m-%d"), q_ora, q_durata, exclude_nr=sel_mg_nr)
                            if has_ov:
                                st.warning("⚠️ Atenție: Programarea modificată se suprapune cu alta existentă pentru acest stilist!")
                            
                            try:
                                t_s = datetime.strptime(q_ora, "%H:%M")
                                t_e = t_s + timedelta(minutes=int(q_durata))
                                q_ora_sf = t_e.strftime("%H:%M")
                            except:
                                q_ora_sf = curr_mgmt_row["Ora Sfârșit"]

                            formatted_q_tel = format_phone_input(q_tel)
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Dată"] = q_data.strftime("%Y-%m-%d")
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Ora Start"] = q_ora
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Ora Sfârșit"] = q_ora_sf
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Client"] = q_client
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Telefon"] = formatted_q_tel
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Serviciu"] = q_serviciu
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Stilist"] = q_stilist
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Preț"] = q_pret
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Durată"] = q_durata
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Status"] = q_status
                            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Observații"] = q_obs
                            save_all()
                            st.success("Programarea a fost actualizată cu succes!")
                            trigger_rerun()

                col_btn_m1, col_btn_m2, col_btn_m3 = st.columns(3)
                with col_btn_m1:
                    if st.button("Marchează ca Efectuat"):
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Status"] = "Efectuat"
                        save_all()
                        st.success("Programare marcată ca efectuat!")
                        trigger_rerun()
                with col_btn_m2:
                    if st.button("Marchează ca Anulat"):
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Status"] = "Anulat"
                        save_all()
                        st.warning("Programare anulată.")
                        trigger_rerun()
                with col_btn_m3:
                    if st.button("Șterge Definitiv", type="primary"):
                        st.session_state.prog_df = st.session_state.prog_df[st.session_state.prog_df["Nr. Programare"] != sel_mg_nr]
                        save_all()
                        st.error("Programare ștersă.")
                        trigger_rerun()
            else:
                st.info(f"Nu există programări înregistrate pentru data de {date_str_mg} cu filtrele selectate.")
        else:
            st.info("Nu există programări în sistem.")

# ==========================================
# TAB 4 & 5: SERVICII & RECENZII (Admin & Stilist)
# ==========================================
if is_admin_or_stylist:
    with tabs[3]:
        st.markdown("### 💇‍♂️ Gestiune & Catalog Servicii în funcție de Stilist")
        df_serv = st.session_state.serv_df.copy()
        st.dataframe(df_serv, use_container_width=True)

        st.markdown("---")
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.markdown("#### ➕ Adaugă Serviciu Nou")
            with st.form("add_serv"):
                ns_nume = st.text_input("Nume Serviciu")
                ns_stilist = st.selectbox("Asignat Stilist", ["Adrian", "Andreea", "Alex", "Denis"])
                ns_pret = st.number_input("Preț (RON)", min_value=0, value=50)
                ns_durata = st.number_input("Durată (minute)", min_value=5, value=30)
                if st.form_submit_button("Adaugă"):
                    if ns_nume:
                        new_s = pd.DataFrame([{"Serviciu": ns_nume, "Preț": ns_pret, "Durată (min)": ns_durata, "Stilist": ns_stilist}])
                        st.session_state.serv_df = pd.concat([st.session_state.serv_df, new_s], ignore_index=True)
                        save_all()
                        st.success("Serviciu adăugat!")
                        trigger_rerun()
                        
        with col_s2:
            st.markdown("#### ✏️ Editează Serviciu")
            edit_target = st.selectbox("Alege serviciul de modificat", df_serv["Serviciu"].tolist() if not df_serv.empty else [])
            if edit_target:
                s_curr = df_serv[df_serv["Serviciu"] == edit_target].iloc[0]
                with st.form("edit_serv_form"):
                    e_nume = st.text_input("Nume nou", value=s_curr["Serviciu"])
                    e_stilist = st.selectbox("Stilist", ["Adrian", "Andreea", "Alex", "Denis"], index=["Adrian", "Andreea", "Alex", "Denis"].index(s_curr["Stilist"]) if s_curr["Stilist"] in ["Adrian", "Andreea", "Alex", "Denis"] else 0)
                    e_pret = st.number_input("Preț nou (RON)", min_value=0, value=int(float(s_curr["Preț"]) if pd.notna(s_curr["Preț"]) else 50))
                    e_durata = st.number_input("Durată nouă (min)", min_value=5, value=int(float(s_curr["Durată (min)"]) if pd.notna(s_curr["Durată (min)"]) else 30))
                    if st.form_submit_button("Salvează Modificări"):
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Serviciu"] = e_nume
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Stilist"] = e_stilist
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Preț"] = e_pret
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Durată (min)"] = e_durata
                        save_all()
                        st.success("Serviciu actualizat!")
                        trigger_rerun()
                        
        with col_s3:
            st.markdown("#### 🗑️ Șterge Serviciu")
            with st.form("del_serv_form"):
                del_serv = st.selectbox("Alege serviciul de șters", df_serv["Serviciu"].tolist() if not df_serv.empty else [])
                if st.form_submit_button("Șterge Serviciul"):
                    st.session_state.serv_df = st.session_state.serv_df[st.session_state.serv_df["Serviciu"] != del_serv]
                    save_all()
                    st.success("Serviciul a fost șters.")
                    trigger_rerun()

    with tabs[4]:
        st.markdown("### ⭐ Moderare Recenzii (În Așteptare)")
        rev_df = st.session_state.rev_df.copy()
        pending_revs = rev_df[rev_df["Status"] == "În așteptare"] if not rev_df.empty else pd.DataFrame()
        
        if not pending_revs.empty:
            rev_options = {}
            for _, r in pending_revs.iterrows():
                label = f"Client: {r['Client']} | Stilist: {r['Stilist']} | Rating: {r['Rating']}⭐ | Comentariu: {str(r['Comentariu'])[:35]}..."
                rev_options[label] = int(r['ID']) if pd.notna(r['ID']) else 0

            sel_rev_label = st.selectbox("Selectează Recenzia din Așteptare pentru Aprobare", list(rev_options.keys()))
            sel_rev_id = rev_options[sel_rev_label]
            
            rev_display = rev_df[rev_df["ID"] == sel_rev_id].drop(columns=["ID"], errors="ignore")
            status_cols_rev = [c for c in ["Status"] if c in rev_display.columns]
            
            if status_cols_rev:
                st.dataframe(rev_display.style.apply(highlight_status_cells, subset=status_cols_rev, axis=1), use_container_width=True)
            else:
                st.dataframe(rev_display, use_container_width=True)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.button("✅ Aprobă Publicarea Recenziei"):
                    st.session_state.rev_df.loc[st.session_state.rev_df["ID"] == sel_rev_id, "Status"] = "Aprobat"
                    save_all()
                    st.success("Recenzia a fost aprobată și adăugată în bannerul public!")
                    trigger_rerun()
            with col_m2:
                if st.button("🗑️ Șterge Recenzia", type="primary"):
                    st.session_state.rev_df = st.session_state.rev_df[st.session_state.rev_df["ID"] != sel_rev_id]
                    save_all()
                    st.error("Recenzia a fost ștersă.")
                    trigger_rerun()
        else:
            st.info("Nu există nicio recenzie în așteptarea moderării.")

# ==========================================
# RAPORT FINANCIAR & SETĂRI (Doar pentru Administrator)
# ==========================================
if is_admin:
    with tabs[5]:
        st.markdown("### 📊 Raport Financiar & Total Plată în Funcție de Servicii Efectuate")
        df_f = st.session_state.prog_df.copy()

        if not df_f.empty and "Preț" in df_f.columns:
            df_f["Dată_dt"] = pd.to_datetime(df_f["Dată"], errors="coerce")
            df_f["Lună"] = df_f["Dată_dt"].dt.strftime("%Y-%m")

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                luni_disponibile = ["Toate"] + sorted(df_f["Lună"].dropna().unique().tolist())
                sel_luna = st.selectbox("Filtrează Lunar", luni_disponibile)
            with col_r2:
                stilisti_raport = ["Toți"] + df_f["Stilist"].dropna().unique().tolist()
                sel_stilist_r = st.selectbox("Filtrează după Stilist", stilisti_raport)

            if sel_luna != "Toate":
                df_f = df_f[df_f["Lună"] == sel_luna]
            if sel_stilist_r != "Toți":
                df_f = df_f[df_f["Stilist"] == sel_stilist_r]

            total_incasari_efectuate = df_f[df_f["Status"] == "Efectuat"]["Preț"].sum()
            total_programari = len(df_f)

            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Încasări Reale (Servicii Efectuate)</div><div class="metric-val">{total_incasari_efectuate} RON</div></div>', unsafe_allow_html=True)
            with c_f2:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Programări în Filtru</div><div class="metric-val">{total_programari}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if not df_f.empty:
                fig = px.bar(
                    df_f, x="Dată", y="Preț", color="Stilist", barmode="group",
                    title="Încasări Detaliate pe Stilist și Dată",
                    template="plotly_dark",
                    color_discrete_sequence=["#e5c158", "#38bdf8", "#34d399", "#f43f5e"]
                )
                max_p = df_f["Preț"].max() if not df_f.empty else 100
                fig.update_layout(yaxis=dict(range=[0, max_p * 1.25]))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există suficiente date financiare pentru generarea rapoartelor.")

    with tabs[6]:
        st.markdown("### ⚙️ Panou Setări & Gestiune Utilizatori / Chei API WhatsApp")
        st.dataframe(st.session_state.users_df[["Utilizator", "Rol", "Telefon", "APIKey"]], use_container_width=True)

        users_list = st.session_state.users_df["Utilizator"].tolist()
        sel_user_mgmt = st.selectbox("Selectează Utilizator pentru Setarea cheii API WhatsApp sau Adaugă", ["-- Adaugă Utilizator Nou --"] + users_list)

        if sel_user_mgmt == "-- Adaugă Utilizator Nou --":
            with st.form("add_new_user_form"):
                n_user = st.text_input("Nume Utilizator Nou")
                n_pass = st.text_input("Parolă", type="password")
                n_rol = st.selectbox("Rol", ["Administrator", "Stilist", "Client"])
                n_tel = st.text_input("Telefon contact", value="+40 ", placeholder="+40 7xxxxxxxx")
                n_apikey = st.text_input("API Key WhatsApp (CallMeBot)", placeholder="opțional pentru stilisti")
                
                if st.form_submit_button("Adaugă Utilizator"):
                    if n_user and n_pass:
                        if n_user in st.session_state.users_df["Utilizator"].values:
                            st.error("Utilizatorul există deja!")
                        else:
                            formatted_new_tel = format_phone_input(n_tel)
                            new_u = pd.DataFrame([{"Utilizator": n_user, "Parolă": n_pass, "Rol": n_rol, "Telefon": formatted_new_tel, "APIKey": n_apikey}])
                            st.session_state.users_df = pd.concat([st.session_state.users_df, new_u], ignore_index=True)
                            save_all()
                            st.success(f"Utilizatorul {n_user} a fost adăugat!")
                            trigger_rerun()
        else:
            u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == sel_user_mgmt].iloc[0]
            with st.form("edit_existing_user_form"):
                e_pass = st.text_input("Parolă", value=u_row["Parolă"], type="password")
                e_rol = st.selectbox("Rol", ["Administrator", "Stilist", "Client"], index=["Administrator", "Stilist", "Client"].index(u_row["Rol"]) if u_row["Rol"] in ["Administrator", "Stilist", "Client"] else 2)
                e_tel = st.text_input("Telefon contact", value=format_phone_input(u_row["Telefon"]))
                e_apikey = st.text_input("API Key WhatsApp (CallMeBot)", value=str(u_row["APIKey"]) if pd.notna(u_row["APIKey"]) else "")
                
                col_u_btn1, col_u_btn2 = st.columns(2)
                with col_u_btn1:
                    save_mod = st.form_submit_button("Salvează Modificările")
                with col_u_btn2:
                    del_mod = st.form_submit_button("Șterge Utilizatorul")
                
                if save_mod:
                    formatted_edited_tel = format_phone_input(e_tel)
                    st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == sel_user_mgmt, "Parolă"] = e_pass
                    st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == sel_user_mgmt, "Rol"] = e_rol
                    st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == sel_user_mgmt, "Telefon"] = formatted_edited_tel
                    st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == sel_user_mgmt, "APIKey"] = e_apikey
                    save_all()
                    st.success(f"Utilizatorul {sel_user_mgmt} a fost actualizat!")
                    trigger_rerun()
                if del_mod:
                    if sel_user_mgmt in ["Alex", "Denis", "Adrian", "Andreea"]:
                        st.error("Nu poți șterge membrii principali ai echipei!")
                    else:
                        st.session_state.users_df = st.session_state.users_df[st.session_state.users_df["Utilizator"] != sel_user_mgmt]
                        save_all()
                        st.success(f"Utilizatorul {sel_user_mgmt} a fost șters cu succes!")
                        trigger_rerun()

# ==========================================
# VIZIUNE CLIENT: TAB 3 (Recenzii)
# ==========================================
if not is_admin_or_stylist:
    with tabs[2]:
        st.markdown("### ⭐ Recenzii Salon & Istoricul Meu")
        
        st.markdown("#### 💬 Ce spun clienții noștri")
        aprobate = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
        
        if not aprobate.empty:
            for idx, row in aprobate.iterrows():
                with st.container(border=True):
                    st.markdown(f"**👤 {row['Client']}** | Stilist: *{row['Stilist']}* | Rating: {'⭐' * int(float(row['Rating']) if pd.notna(row['Rating']) else 5)}")
                    st.markdown(f"> *{row['Comentariu']}*")
        else:
            st.info("Nu există recenzii aprobate momentan.")

        st.markdown("---")
        st.markdown("#### 📜 Recenziile Tale Trimise")
        my_reviews = st.session_state.rev_df[st.session_state.rev_df["Client"] == current_user] if not st.session_state.rev_df.empty else pd.DataFrame()
        
        if not my_reviews.empty:
            for _, rev_row in my_reviews.iterrows():
                with st.container(border=True):
                    st.markdown(f"**Stilist:** {rev_row['Stilist']} | **Rating:** {'⭐' * int(float(rev_row['Rating']) if pd.notna(rev_row['Rating']) else 5)}")
                    st.markdown(f"Comentariu: *{rev_row['Comentariu']}*")
        else:
            st.info("Nu ai adăugat nicio recenzie până acum.")

        st.markdown("---")
        st.markdown("#### ✍️ Adaugă o Recenzie Nouă")
        with st.form("apply_review_form"):
            r_stilist = st.selectbox("Stilistul vizitat", ["Adrian", "Andreea", "Alex", "Denis"])
            r_rating = st.slider("Rating (Stele)", 1, 5, 5)
            r_comentariu = st.text_area("Scrie experiența ta...")
            if st.form_submit_button("Trimite Recenzia"):
                if r_comentariu:
                    new_rev_id = int(st.session_state.rev_df["ID"].max() + 1) if not st.session_state.rev_df.empty and "ID" in st.session_state.rev_df.columns and pd.notna(st.session_state.rev_df["ID"].max()) else 1
                    new_r = pd.DataFrame([{
                        "ID": new_rev_id,
                        "Client": current_user,
                        "Stilist": r_stilist,
                        "Rating": r_rating,
                        "Comentariu": r_comentariu,
                        "Status": "În așteptare"
                    }])
                    st.session_state.rev_df = pd.concat([st.session_state.rev_df, new_r], ignore_index=True)
                    save_all()
                    st.markdown('<div class="success-alert">✅ Recenzia a fost trimisă cu succes! Îți mulțumim pentru feedback.</div>', unsafe_allow_html=True)
                    trigger_rerun()
