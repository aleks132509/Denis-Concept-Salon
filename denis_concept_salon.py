import os
import time
import unicodedata
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
    initial_sidebar_state="collapsed",
)

def apply_background_style(is_logged_in):
    if not is_logged_in:
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, rgba(15, 17, 23, 0.94) 0%, rgba(26, 31, 44, 0.96) 50%, rgba(10, 12, 16, 0.98) 100%),
                            radial-gradient(circle at 50% 30%, rgba(212, 175, 55, 0.18) 0%, transparent 60%),
                            url('https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1920&q=80') !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
                color: #f3f4f6 !important;
                font-family: 'Helvetica Neue', sans-serif;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, rgba(13, 17, 23, 0.95) 0%, rgba(22, 27, 39, 0.97) 100%),
                            url('https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=1920&q=80') !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
                color: #f3f4f6 !important;
                font-family: 'Helvetica Neue', sans-serif;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <style>
    .salon-card {
        background: linear-gradient(135deg, #131722 0%, #1a202c 100%);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(212, 175, 55, 0.25);
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-val { font-size: 26px; font-weight: 800; color: #e5c158; letter-spacing: 0.5px; }
    .metric-lbl { font-size: 11px; color: #9ca3af; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
    .role-tag { background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%); color: #090a0f; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
    .overlap-alert { background-color: rgba(120, 50, 20, 0.85); color: #fef08a; padding: 14px; border-radius: 10px; border: 1px solid #d97706; font-weight: 600; margin-bottom: 15px;}
    .success-alert { background-color: rgba(6, 78, 59, 0.95); color: #6ee7b7; padding: 14px; border-radius: 10px; border: 1px solid #10b981; font-weight: 600; margin-bottom: 12px;}
    .info-alert { background-color: rgba(30, 58, 138, 0.85); color: #93c5fd; padding: 14px; border-radius: 10px; border: 1px solid #3b82f6; font-weight: 600; margin-bottom: 12px;}
    
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        font-weight: 700;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
        margin: 6px 0;
        transition: all 0.3s ease;
        font-size: 15px;
        letter-spacing: 0.5px;
        width: 100%;
        justify-content: center;
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
        padding: 12px 0;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.35);
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .marquee-content {
        display: inline-block;
        animation: marquee 25s linear infinite;
        -webkit-animation: marquee 25s linear infinite;
        color: #f3f4f6;
        font-size: 14px;
        font-weight: 500;
    }
    .marquee-content span {
        margin-right: 60px;
        color: #e5c158;
    }
    @keyframes marquee {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-50%); }
    }

    .stButton>button {
        background: linear-gradient(135deg, #e5c158 0%, #c5a059 100%) !important;
        color: #090a0f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 15px !important;
        box-shadow: 0 4px 14px rgba(212, 175, 55, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        opacity: 0.95 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6) !important;
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
# GESTIUNE SIGURĂ FIȘIERE CSV (ELIMINĂ EMPTYDATAERROR)
# ==========================================
PROG_FILE = "programari_denis_concept.csv"
SERV_FILE = "servicii_denis_concept.csv"
USER_FILE = "utilizatori_denis_concept.csv"
REV_FILE = "recenzii_denis_concept.csv"
MASTER_WHATSAPP_PHONE = "35796005530"
MASTER_WHATSAPP_APIKEY = "9926434"

def get_default_dfs():
    today_str = date.today().strftime("%Y-%m-%d")
    future_str = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    df_p = pd.DataFrame([
        {"Nr. Programare": 1, "Dată": today_str, "Ora Start": "10:00", "Ora Sfârșit": "10:45", "Client": "Alex", "Telefon": "+40722000000", "Serviciu": "Tuns + Barbă Fade", "Stilist": "Adrian", "Preț": 90, "Durată": 45, "Status": "Confirmat", "Observații": "Test programare Alex", "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""},
        {"Nr. Programare": 2, "Dată": future_str, "Ora Start": "11:30", "Ora Sfârșit": "12:30", "Client": "Ionuț", "Telefon": "+40733111222", "Serviciu": "Tuns Lung & Coafat", "Stilist": "Andreea", "Preț": 120, "Durată": 60, "Status": "Confirmat", "Observații": "Test programare Ionuț", "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""}
    ])
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
    df_u = pd.DataFrame([
        {"Utilizator": "Alex", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "+40722000000", "APIKey": ""},
        {"Utilizator": "Denis", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "+40733000000", "APIKey": ""},
        {"Utilizator": "Adrian", "Parolă": "admin123", "Rol": "Stilist", "Telefon": "+40744111222", "APIKey": ""},
        {"Utilizator": "Andreea", "Parolă": "admin123", "Rol": "Stilist", "Telefon": "+40755222333", "APIKey": ""},
        {"Utilizator": "Ionuț", "Parolă": "client123", "Rol": "Client", "Telefon": "+40733111222", "APIKey": ""},
    ])
    df_r = pd.DataFrame([
        {"ID": 1, "Client": "Alex", "Stilist": "Adrian", "Rating": 5, "Comentariu": "Serviciu impecabil și profesionalism!", "Status": "Aprobat"},
        {"ID": 2, "Client": "Ionuț", "Stilist": "Andreea", "Rating": 5, "Comentariu": "Atmosferă excelentă și atenție la detalii.", "Status": "Aprobat"}
    ])
    return df_p, df_s, df_u, df_r

def safe_load_csv(file_path, default_df):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        default_df.to_csv(file_path, index=False)
        return default_df.astype(str)
    try:
        df = pd.read_csv(file_path, dtype=str)
        if df.empty or len(df.columns) == 0:
            default_df.to_csv(file_path, index=False)
            return default_df.astype(str)
        return df
    except Exception:
        default_df.to_csv(file_path, index=False)
        return default_df.astype(str)

def load_data():
    df_p_def, df_s_def, df_u_def, df_r_def = get_default_dfs()
    
    st.session_state.prog_df = safe_load_csv(PROG_FILE, df_p_def)
    if "ID" in st.session_state.prog_df.columns and "Nr. Programare" not in st.session_state.prog_df.columns:
        st.session_state.prog_df.rename(columns={"ID": "Nr. Programare"}, inplace=True)
    for col in ["Nr. Programare", "Preț", "Durată"]:
        if col in st.session_state.prog_df.columns:
            st.session_state.prog_df[col] = pd.to_numeric(st.session_state.prog_df[col], errors="coerce")
    if "Status Modificare" in st.session_state.prog_df.columns:
        st.session_state.prog_df["Status Modificare"] = st.session_state.prog_df["Status Modificare"].replace(["Niciuna", "nan", "NaN"], "")

    st.session_state.serv_df = safe_load_csv(SERV_FILE, df_s_def)
    for col in ["Preț", "Durată (min)"]:
        if col in st.session_state.serv_df.columns:
            st.session_state.serv_df[col] = pd.to_numeric(st.session_state.serv_df[col], errors="coerce")

    st.session_state.users_df = safe_load_csv(USER_FILE, df_u_def)
    if "APIKey" not in st.session_state.users_df.columns:
        st.session_state.users_df["APIKey"] = ""

    st.session_state.rev_df = safe_load_csv(REV_FILE, df_r_def)
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
    if not val or pd.isna(val) or str(val).strip() in ["", "nan"]:
        return "+40 "
    val_str = str(val).strip()
    if val_str.startswith("+"):
        return val_str
    clean = "".join(filter(str.isdigit, val_str))
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
    return f"https://wa.me/{clean_phone}?text={urllib.parse.quote(text)}"

def check_overlap(stilist, data_str, ora_start_str, durata_min, exclude_nr=None):
    try:
        t_start = datetime.strptime(ora_start_str, "%H:%M").time()
        start_dt = datetime.combine(datetime.strptime(data_str, "%Y-%m-%d"), t_start)
        end_dt = start_dt + timedelta(minutes=int(durata_min))
    except:
        return False, []

    df = st.session_state.prog_df
    conflicts = []
    for _, row in df.iterrows():
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

RO_DAYS = {0: "Luni", 1: "Marți", 2: "Miercuri", 3: "Joi", 4: "Vineri", 5: "Sâmbătă", 6: "Duminică"}
RO_MONTHS = {1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie", 5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August", 9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"}

def format_ro_date(d_input):
    if pd.isna(d_input) or not d_input:
        return ""
    try:
        dt = datetime.strptime(str(d_input).strip()[:10], "%Y-%m-%d")
        return f"{RO_DAYS[dt.weekday()]}, {dt.day} {RO_MONTHS[dt.month]} {dt.year}"
    except:
        return str(d_input)

def render_lux_table(df):
    if df.empty:
        return "<div style='text-align: center; padding: 25px; color: #9ca3af; background: #131722; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.2);'>Nu există înregistrări.</div>"
    
    df_render = df.copy()
    for drop_col in ["Nr. Programare", "ID"]:
        if drop_col in df_render.columns:
            df_render = df_render.drop(columns=[drop_col])
    if "Dată" in df_render.columns:
        df_render["Dată"] = df_render["Dată"].apply(format_ro_date)

    html = "<div style='overflow-x: auto; margin-bottom: 20px;'><table style='width: 100%; border-collapse: collapse; background: #131722; border-radius: 14px; overflow: hidden; border: 1px solid rgba(212, 175, 55, 0.3); font-size: 13px;'>"
    html += "<thead><tr style='background: #1a202c; color: #e5c158; text-transform: uppercase; font-size: 11px;'>"
    for col in df_render.columns:
        if col != "Status Modificare":
            html += f"<th style='padding: 14px; text-align: center;'>{col}</th>"
    html += "</tr></thead><tbody>"
    
    for idx, row in df_render.iterrows():
        row_bg = "#131722" if idx % 2 == 0 else "#181d29"
        html += f"<tr style='background-color: {row_bg}; border-bottom: 1px solid rgba(255, 255, 255, 0.05);'>"
        for col in df_render.columns:
            if col == "Status Modificare":
                continue
            val = str(row[col])
            if val in ["nan", "NaN", "None"]: val = ""
            html += f"<td style='padding: 12px; text-align: center; color: #f3f4f6;'>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

def render_marquee_banner():
    rev_aprobate = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
    if not rev_aprobate.empty:
        items = "".join([f"<span>⭐ <b>{r['Client']}</b> despre {r['Stilist']}: \"{r['Comentariu']}\"</span>" for _, r in rev_aprobate.iterrows()])
        st.markdown(f'<div class="marquee-container"><div class="marquee-content">{items} &nbsp;|&nbsp; {items}</div></div>', unsafe_allow_html=True)

# ==========================================
# AUTENTIFICARE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

apply_background_style(st.session_state.logged_in)

if not st.session_state.logged_in:
    render_marquee_banner()
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_auth, _ = st.columns([1, 1.4, 1])
    with col_auth:
        st.markdown("<h1 style='text-align: center; color: #e5c158; font-family: serif;'>✂️ Denis Concept Salon</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            u_input = st.text_input("👤 Utilizator", placeholder="ex: Alex, Ionuț, Adrian")
            p_input = st.text_input("🔑 Parolă", type="password")
            if st.form_submit_button("✨ Intră în Cont", use_container_width=True):
                users = st.session_state.users_df
                match = users[(users["Utilizator"] == u_input) & (users["Parolă"] == p_input)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = u_input
                    st.session_state.role = match.iloc[0]["Rol"]
                    st.session_state.selected_nav = "🏠 Acasă / Dashboard"  # HOME LA LOGARE
                    st.toast("Autentificare reușită!", icon="✨")
                    trigger_rerun()
                else:
                    st.toast("Utilizator sau parolă incorectă!", icon="❌")
        st.stop()

is_admin = st.session_state.role == "Administrator"
is_stylist = st.session_state.role == "Stilist"
is_admin_or_stylist = is_admin or is_stylist
current_user = st.session_state.user

render_marquee_banner()

# ==========================================
# MENIU PRINCIPAL PE ECRAN (MOBILE FIRST)
# ==========================================
if is_admin:
    nav_options = ["🏠 Acasă / Dashboard", "➕ Adaugă Programare", "📅 Programările mele", "⚙️ Gestiune & Aprobări", "💇‍♂️ Servicii & Prețuri", "⭐ Recenzii", "📊 Raport Financiar", "⚙️ Setări & Utilizatori"]
elif is_stylist:
    nav_options = ["🏠 Acasă / Dashboard", "➕ Adaugă Programare", "📅 Programările mele", "⚙️ Gestiune & Aprobări", "💇‍♂️ Servicii & Prețuri", "⭐ Recenzii & Istoric", "📊 Raport Financiarul Meu"]
else:
    nav_options = ["🏠 Acasă / Dashboard", "📅 Programează-te", "📜 Programări curente & modificări", "⭐ Recenzii Salon & Istoricul Meu"]

if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "🏠 Acasă / Dashboard"

# Buton Home în Sidebar care duce STRICT la Acasă / Dashboard
st.sidebar.markdown(f"### ✂️ **{current_user}**")
st.sidebar.markdown(f"Rol: <span class='role-tag'>{st.session_state.role}</span>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🏠 ACASĂ / HOME", use_container_width=True):
    st.session_state.selected_nav = "🏠 Acasă / Dashboard"
    trigger_rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Deconectare", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    trigger_rerun()

# SELECTOR SUS PE ECRAN (Fără să fie nevoie de meniul lateral pe telefon)
st.markdown("""
<div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(212, 175, 55, 0.4); margin-bottom: 15px;">
    <span style="color: #e5c158; font-weight: 700; font-size: 13px;">📱 Meniu Rapid Salon</span>
</div>
""", unsafe_allow_html=True)

current_index = nav_options.index(st.session_state.selected_nav) if st.session_state.selected_nav in nav_options else 0
selected_page = st.selectbox("Navigare Secțiune", nav_options, index=current_index, key="main_screen_select")

if selected_page != st.session_state.selected_nav:
    st.session_state.selected_nav = selected_page
    trigger_rerun()

stilisti_disponibili = ["Adrian", "Andreea", "Alex", "Denis"]
default_stylist_idx = stilisti_disponibili.index(current_user) if current_user in stilisti_disponibili else 0

# ==========================================
# AFIȘARE PAGINI
# ==========================================
if selected_page == "🏠 Acasă / Dashboard":
    st.markdown(f"### ✨ Bun venit la Denis Concept Salon, **{current_user}**!")
    st.markdown("<p style='color: #9ca3af;'>Folosește meniul rapid de sus pentru a accesa secțiunile dorite instantaneu.</p>", unsafe_allow_html=True)
    
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.markdown(f'<div class="salon-card"><div class="metric-lbl">Status Cont</div><div class="metric-val" style="font-size: 18px;">Activ ⭐</div></div>', unsafe_allow_html=True)
    with col_h2:
        active_cnt = len(st.session_state.prog_df[st.session_state.prog_df["Status"] == "Confirmat"])
        st.markdown(f'<div class="salon-card"><div class="metric-lbl">Programări Active</div><div class="metric-val">{active_cnt}</div></div>', unsafe_allow_html=True)
    with col_h3:
        rev_cnt = len(st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"])
        st.markdown(f'<div class="salon-card"><div class="metric-lbl">Recenzii Aprobate</div><div class="metric-val">{rev_cnt}</div></div>', unsafe_allow_html=True)

elif selected_page in ["➕ Adaugă Programare", "📅 Programează-te"]:
    st.markdown(f"### 🚀 Programare Nouă ({current_user})")
    with st.form("new_app_form"):
        col1, col2 = st.columns(2)
        with col1:
            if is_admin_or_stylist:
                client_nume = st.text_input("👤 Nume Client")
            else:
                client_nume = st.text_input("👤 Client", value=current_user, disabled=True)
            client_tel = st.text_input("📞 Telefon", value="+40 ")
            p_data = st.date_input("📅 Dată", value=date.today(), min_value=date.today())
        with col2:
            p_stilist = st.selectbox("💈 Stilist", stilisti_disponibili, index=default_stylist_idx)
            df_serv = st.session_state.serv_df
            serv_f = df_serv[df_serv["Stilist"] == p_stilist]
            if serv_f.empty: serv_f = df_serv
            
            selected_services = []
            total_pret = 0
            total_durata = 0
            for idx, s_row in serv_f.iterrows():
                if st.checkbox(f"{s_row['Serviciu']} - {s_row['Preț']} RON", key=f"srv_{idx}"):
                    selected_services.append(s_row['Serviciu'])
                    total_pret += int(float(s_row['Preț']))
                    total_durata += int(float(s_row['Durată (min)']))
            
            st.markdown(f"**Durată:** {total_durata} min | **Total:** {total_pret} RON")
            
            slots = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
            p_ora = st.selectbox("⏰ Ora Start", slots)
            p_obs = st.text_area("📝 Observații")

        if st.form_submit_button("✨ Salvează Programarea", use_container_width=True):
            if not client_nume or not selected_services:
                st.toast("Completează numele și selectează cel puțin un serviciu!", icon="❌")
            else:
                new_nr = int(st.session_state.prog_df["Nr. Programare"].max() + 1) if not st.session_state.prog_df.empty and pd.notna(st.session_state.prog_df["Nr. Programare"].max()) else 1
                new_row = pd.DataFrame([{
                    "Nr. Programare": new_nr, "Dată": p_data.strftime("%Y-%m-%d"), "Ora Start": p_ora, 
                    "Ora Sfârșit": "10:00", "Client": client_nume, "Telefon": format_phone_input(client_tel),
                    "Serviciu": ", ".join(selected_services), "Stilist": p_stilist, "Preț": total_pret, 
                    "Durată": total_durata, "Status": "Confirmat", "Observații": p_obs, 
                    "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""
                }])
                st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
                save_all()
                st.toast("Programare salvată cu succes!", icon="✅")
                trigger_rerun()

elif selected_page in ["📅 Programările mele", "📜 Programări curente & modificări"]:
    st.markdown("### 📅 Programări Active")
    df_p = st.session_state.prog_df.copy()
    if not is_admin_or_stylist:
        df_p = df_p[df_p["Client"].str.contains(current_user, case=False, na=False)]
    st.markdown(render_lux_table(df_p), unsafe_allow_html=True)

elif selected_page == "⚙️ Gestiune & Aprobări":
    st.markdown("### ⚙️ Gestiune & Aprobări")
    st.markdown(render_lux_table(st.session_state.prog_df), unsafe_allow_html=True)

elif selected_page == "💇‍♂️ Servicii & Prețuri":
    st.markdown("### 💇‍♂️ Catalog Servicii")
    st.markdown(render_lux_table(st.session_state.serv_df), unsafe_allow_html=True)

elif "Recenzii" in selected_page:
    st.markdown("### ⭐ Recenzii Salon")
    st.markdown(render_lux_table(st.session_state.rev_df), unsafe_allow_html=True)

elif "Raport" in selected_page:
    st.markdown("### 📊 Raport Financiar")
    total_inc = st.session_state.prog_df[st.session_state.prog_df["Status"] == "Confirmat"]["Preț"].sum() if not st.session_state.prog_df.empty else 0
    st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Încasări</div><div class="metric-val">{total_inc} RON</div></div>', unsafe_allow_html=True)

elif selected_page == "⚙️ Setări & Utilizatori":
    st.markdown("### ⚙️ Setări & Utilizatori")
    st.markdown(render_lux_table(st.session_state.users_df[["Utilizator", "Rol", "Telefon", "APIKey"]]), unsafe_allow_html=True)
