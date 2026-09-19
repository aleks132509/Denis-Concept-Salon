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
    .overlap-alert { background-color: rgba(120, 50, 20, 0.85); color: #fef08a; padding: 14px; border-radius: 10px; border: 1px solid #d97706; font-weight: 600; margin-bottom: 15px;}
    .success-alert { background-color: rgba(6, 78, 59, 0.95); color: #6ee7b7; padding: 14px; border-radius: 10px; border: 1px solid #10b981; font-weight: 600; margin-bottom: 12px;}
    .info-alert { background-color: rgba(30, 58, 138, 0.85); color: #93c5fd; padding: 14px; border-radius: 10px; border: 1px solid #3b82f6; font-weight: 600; margin-bottom: 12px;}
    
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid #e5c158 !important;
        color: #e5c158 !important;
        border-radius: 8px !important;
    }
    span[data-baseweb="tag"] span {
        color: #e5c158 !important;
    }
    span[data-baseweb="tag"] svg {
        fill: #e5c158 !important;
    }

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
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        opacity: 0.95 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(212, 175, 55, 0.6) !important;
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
# GESTIUNE SIGURĂ FIȘIERE PERSISTENTE
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

def remove_diacritics(text):
    if not text:
        return ""
    nfd_form = unicodedata.normalize('NFD', text)
    without_diacritics = "".join([c for c in nfd_form if unicodedata.category(c) != 'Mn'])
    replacements = {'ă': 'a', 'Ă': 'A', 'â': 'a', 'Â': 'A', 'î': 'i', 'Î': 'I', 'ș': 's', 'Ș': 'S', 'ț': 't', 'Ț': 'T'}
    for k, v in replacements.items():
        without_diacritics = without_diacritics.replace(k, v)
    return without_diacritics

def send_free_automatic_whatsapp(phone, message, apikey=None):
    target_apikey = str(apikey).strip() if apikey and pd.notna(apikey) and str(apikey).strip() != "" and str(apikey).strip() != "nan" else MASTER_WHATSAPP_APIKEY
    target_phone = str(phone).strip() if phone and pd.notna(phone) and str(phone).strip() != "" else MASTER_WHATSAPP_PHONE
    
    clean_phone = "".join(filter(str.isdigit, str(target_phone)))
    if clean_phone.startswith("0"):
        clean_phone = "4" + clean_phone
    elif not clean_phone.startswith("40") and len(clean_phone) == 9:
        clean_phone = "40" + clean_phone
        
    clean_msg = remove_diacritics(message)
    encoded_text = urllib.parse.quote_plus(clean_msg)
    url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={target_apikey}"
    
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    return True
        except Exception as e:
            print(f"Încercare {attempt} eșuată trimitere WhatsApp:", e)
        time.sleep(1)
    return False

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

RO_DAYS = {0: "Luni", 1: "Marți", 2: "Miercuri", 3: "Joi", 4: "Vineri", 5: "Sâmbătă", 6: "Duminică"}
RO_MONTHS = {1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie", 5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August", 9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"}

def format_ro_date(d_input):
    if pd.isna(d_input) or not d_input:
        return ""
    try:
        if isinstance(d_input, str):
            dt = datetime.strptime(d_input.strip()[:10], "%Y-%m-%d")
        elif isinstance(d_input, (date, datetime)):
            dt = pd.to_datetime(d_input)
        else:
            return str(d_input)
        return f"{RO_DAYS[dt.weekday()]}, {dt.day} {RO_MONTHS[dt.month]} {dt.year}"
    except:
        return str(d_input)

def render_lux_table(df):
    if df.empty:
        return "<div style='text-align: center; padding: 25px; color: #9ca3af; background: #131722; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.2);'>Nu există înregistrări de afișat momentan.</div>"
    
    df_render = df.copy()
    cols_to_keep = ["Dată", "Ora Start", "Ora Sfârșit", "Client", "Telefon", "Serviciu", "Stilist", "Preț", "Durată", "Status", "Observații"]
    existing_cols = [c for c in cols_to_keep if c in df_render.columns]
    df_render = df_render[existing_cols]
            
    if "Dată" in df_render.columns:
        df_render["Dată"] = df_render["Dată"].apply(format_ro_date)

    html = "<div style='overflow-x: auto; margin-bottom: 20px;'><table style='width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #131722 0%, #1a202c 100%); border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.6); border: 1px solid rgba(212, 175, 55, 0.3); font-family: sans-serif; font-size: 13px;'>"
    html += "<thead><tr style='background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); color: #e5c158; text-transform: uppercase; font-size: 11px; letter-spacing: 1.5px; border-bottom: 2px solid rgba(212, 175, 55, 0.4);'>"
    for col in df_render.columns:
        html += f"<th style='padding: 16px 14px; text-align: center; font-weight: 700;'>{col}</th>"
    html += "</tr></thead><tbody>"
    
    for idx, row in df_render.iterrows():
        row_bg = "#131722" if idx % 2 == 0 else "#181d29"
        html += f"<tr style='background-color: {row_bg}; border-bottom: 1px solid rgba(255, 255, 255, 0.06);'>"
        for col in df_render.columns:
            val = str(row[col])
            if val in ["nan", "NaN", "None"]:
                val = ""
            cell_style = "padding: 14px 12px; text-align: center; color: #f3f4f6;"
            if col == "Status":
                if val in ["Confirmat"]:
                    val = f"<span style='background: rgba(30, 58, 138, 0.6); color: #93c5fd; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(59, 130, 246, 0.4); display: inline-block; text-transform: uppercase;'>{val}</span>"
                elif val in ["În Așteptare"]:
                    val = f"<span style='background: rgba(120, 80, 20, 0.5); color: #fef08a; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(212, 175, 55, 0.4); display: inline-block; text-transform: uppercase;'>{val}</span>"
                elif val in ["Efectuat", "Aprobat"]:
                    val = f"<span style='background: rgba(6, 78, 59, 0.6); color: #6ee7b7; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(16, 185, 129, 0.4); display: inline-block; text-transform: uppercase;'>{val}</span>"
                elif val in ["Anulat", "Respins"]:
                    val = f"<span style='background: rgba(127, 29, 29, 0.6); color: #fca5a5; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(239, 68, 68, 0.4); display: inline-block; text-transform: uppercase;'>{val}</span>"
            html += f"<td style='{cell_style}'>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

def render_marquee_banner():
    rev_aprobate = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
    if not rev_aprobate.empty:
        items = "".join([f"<span>⭐ <b>{r['Client']}</b> despre {r['Stilist']}: \"{r['Comentariu']}\"</span>" for _, r in rev_aprobate.iterrows()])
        st.markdown(f'<div class="marquee-container"><div class="marquee-content">{items} &nbsp;|&nbsp; {items}</div></div>', unsafe_allow_html=True)

# ==========================================
# SESIUNE & AUTENTIFICARE
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
        st.markdown("<h1 style='text-align: center; color: #e5c158; font-family: serif; letter-spacing: 2px;'>✂️ Denis Concept Salon</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cbd5e1; text-transform: uppercase; font-size: 12px; letter-spacing: 3px; font-weight: 700;'>Luxury Hair & Barber Experience</p><br>", unsafe_allow_html=True)
        
        with st.form("login_form_streamlit"):
            u_input = st.text_input("👤 Utilizator / Nume", placeholder="ex: Alex, Ionuț, Adrian")
            p_input = st.text_input("🔑 Parolă", type="password")
            submit_login = st.form_submit_button("✨ Intră în Cont", use_container_width=True)
            if submit_login:
                users = st.session_state.users_df
                match = users[(users["Utilizator"] == u_input) & (users["Parolă"] == p_input)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = u_input
                    st.session_state.role = match.iloc[0]["Rol"]
                    st.session_state.selected_nav = "🏠 Acasă / Dashboard"
                    st.toast("Autentificare reușită! Bine ai venit.", icon="✨")
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
# VERIFICARE NOTIFICĂRI APROBARE CLIENT
# ==========================================
if not is_admin_or_stylist:
    df_p_all = st.session_state.prog_df.copy()
    client_progs_check = df_p_all[df_p_all["Client"].str.contains(current_user, case=False, na=False)] if not df_p_all.empty else pd.DataFrame()
    approved_modifs_client = client_progs_check[client_progs_check["Status Modificare"] == "Aprobat"]
    if not approved_modifs_client.empty:
        st.toast("Solicitarea ta de modificare a fost aprobată de către stilist!", icon="🟢")
        for idx_app in approved_modifs_client.index:
            st.session_state.prog_df.loc[idx_app, "Status Modificare"] = ""
        save_all()

# ==========================================
# POP-UP MODAL PENTRU APROBARE / RESPINGERE
# ==========================================
@st.dialog("Gestionează Cererea de Modificare")
def approval_popup(req_r):
    st.markdown(f"**Client:** {req_r['Client']} | **Stilist Asignat:** {req_r['Stilist']}")
    st.markdown(f"📅 Data actuală: `{format_ro_date(req_r['Dată'])} {req_r['Ora Start']}`")
    st.markdown(f"➡️ **Solicitat nou:** `{format_ro_date(req_r['Noua Dată'])} {req_r['Noua Ora']}` | Serviciu nou: *{req_r['Noul Serviciu']}*")
    
    req_dur = int(float(req_r["Durată"])) if pd.notna(req_r["Durată"]) else 30
    has_ov_req, _ = check_overlap(req_r["Stilist"], req_r["Noua Dată"], req_r["Noua Ora"], req_dur, exclude_nr=req_r["Nr. Programare"])
    if has_ov_req:
        st.markdown('<div class="overlap-alert">⚠️ <b>ATENȚIE SUPRAPUNERE:</b> Noul interval orar se suprapune cu o altă programare!</div>', unsafe_allow_html=True)

    motiv_refuz = st.text_input("Motiv respingere (opțional)", key=f"popup_motiv_{req_r['Nr. Programare']}")
    col_pop1, col_pop2 = st.columns(2)
    with col_pop1:
        if st.button("✅ Aprobă Modificarea", use_container_width=True):
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Dată"] = req_r["Noua Dată"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Ora Start"] = req_r["Noua Ora"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Serviciu"] = req_r["Noul Serviciu"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Aprobat"
            save_all()
            
            # Notificare WhatsApp client
            u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == req_r['Client']]
            if not u_row.empty and pd.notna(u_row.iloc[0]["Telefon"]):
                msg = f"Salut {req_r['Client']}, programarea ta la Denis Concept Salon a fost modificata si aprobata pentru data {req_r['Noua Dată']} ora {req_r['Noua Ora']}."
                send_free_automatic_whatsapp(u_row.iloc[0]["Telefon"], msg)
                
            st.toast("Modificarea a fost aprobată cu succes!", icon="✅")
            st.rerun()
    with col_pop2:
        if st.button("❌ Respinge Solicitarea", use_container_width=True):
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Respins"
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Motiv Refuz"] = motiv_refuz if motiv_refuz else "Fără motiv specificat"
            save_all()
            st.toast("Modificarea a fost respinsă.", icon="⚠️")
            st.rerun()

# ==========================================
# MENIU PRINCIPAL & NAVIGARE
# ==========================================
if is_admin:
    nav_options = [
        "🏠 Acasă / Dashboard", 
        "➕ Adaugă Programare", 
        "📅 Programările mele", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii", 
        "📊 Raport Financiar", 
        "⚙️ Setări & Utilizatori"
    ]
elif is_stylist:
    nav_options = [
        "🏠 Acasă / Dashboard", 
        "➕ Adaugă Programare", 
        "📅 Programările mele", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii & Istoric",
        "📊 Raport Financiarul Meu"
    ]
else:
    nav_options = [
        "🏠 Acasă / Dashboard", 
        "📅 Programează-te", 
        "📜 Programări curente & modificări", 
        "⭐ Recenzii Salon & Istoricul Meu"
    ]

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
if not is_admin_or_stylist:
    user_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
    current_tel = format_phone_input(user_row.iloc[0]["Telefon"]) if not user_row.empty else "+40 "
    with st.sidebar.form("edit_client_phone_form"):
        st.text_input("Nume (Fix)", value=current_user, disabled=True)
        new_phone_input = st.text_input("Număr Telefon", value=current_tel)
        if st.form_submit_button("Salvează Telefonul"):
            formatted_p = format_phone_input(new_phone_input)
            st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == current_user, "Telefon"] = formatted_p
            save_all()
            st.toast("Telefonul a fost actualizat!", icon="✅")
            trigger_rerun()
    st.sidebar.markdown("---")

if st.sidebar.button("🚪 Deconectare", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    trigger_rerun()

# SELECTOR SUS PE ECRAN (NUMIT EXACT "Meniu")
st.markdown("""
<div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(212, 175, 55, 0.4); margin-bottom: 15px;">
    <span style="color: #e5c158; font-weight: 700; font-size: 13px;">📱 Meniu</span>
</div>
""", unsafe_allow_html=True)

current_index = nav_options.index(st.session_state.selected_nav) if st.session_state.selected_nav in nav_options else 0
selected_page = st.selectbox("Meniu", nav_options, index=current_index, key="main_screen_select", label_visibility="collapsed")

if selected_page != st.session_state.selected_nav:
    st.session_state.selected_nav = selected_page
    trigger_rerun()

stilisti_disponibili = ["Adrian", "Andreea", "Alex", "Denis"]

# Determinare default stilist pentru client bazat pe ultima programare
default_client_stilist_idx = 0
if not is_admin_or_stylist:
    client_progs_all = st.session_state.prog_df[st.session_state.prog_df["Client"].str.contains(current_user, case=False, na=False)] if not st.session_state.prog_df.empty else pd.DataFrame()
    if not client_progs_all.empty:
        client_progs_all["temp_dt"] = pd.to_datetime(client_progs_all["Dată"] + " " + client_progs_all["Ora Start"], errors="coerce")
        client_progs_all = client_progs_all.sort_values("temp_dt", ascending=False)
        last_used_stylist = client_progs_all.iloc[0]["Stilist"]
        if last_used_stylist in stilisti_disponibili:
            default_client_stilist_idx = stilisti_disponibili.index(last_used_stylist)
else:
    default_client_stilist_idx = stilisti_disponibili.index(current_user) if current_user in stilisti_disponibili else 0

# ==========================================
# RUTARE PAGINI
# ==========================================
if selected_page == "🏠 Acasă / Dashboard":
    st.markdown(f"### ✨ Bun venit la Denis Concept Salon, **{current_user}**!")
    st.markdown("<p style='color: #9ca3af;'>Folosește meniul de mai sus pentru a accesa secțiunile dorite instantaneu.</p>", unsafe_allow_html=True)
    
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
    st.markdown(f"### ➕ Adaugă Programare Nouă ({current_user})")
    
    with st.form("admin_new_appointment_form"):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            if is_admin_or_stylist:
                existing_clients = sorted(st.session_state.prog_df["Client"].dropna().unique().tolist()) if not st.session_state.prog_df.empty else []
                existing_users = sorted(st.session_state.users_df[st.session_state.users_df["Rol"] == "Client"]["Utilizator"].dropna().unique().tolist())
                all_known_clients = sorted(list(set(existing_clients + existing_users)))
                
                client_input_mode = st.radio("Mod selectare client", ["Din agendă / clienți existenți", "Client nou (manual)"], horizontal=True)
                if client_input_mode == "Din agendă / clienți existenți" and all_known_clients:
                    client_nume = st.selectbox("👤 Selectează Client din Agendă", all_known_clients)
                    u_match = st.session_state.users_df[st.session_state.users_df["Utilizator"] == client_nume]
                    default_tel_agenda = "+40 "
                    if not u_match.empty and pd.notna(u_match.iloc[0]["Telefon"]):
                        default_tel_agenda = format_phone_input(u_match.iloc[0]["Telefon"])
                    client_tel = st.text_input("📞 Telefon Client", value=default_tel_agenda)
                else:
                    client_nume = st.text_input("👤 Nume Client Nou", value="")
                    client_tel = st.text_input("📞 Telefon Client", value="+40 ")
            else:
                client_nume = st.text_input("👤 Nume Client", value=current_user, disabled=True)
                default_tel = "+40 "
                user_u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
                if not user_u_row.empty and pd.notna(user_u_row.iloc[0]["Telefon"]):
                    default_tel = format_phone_input(user_u_row.iloc[0]["Telefon"])
                client_tel = st.text_input("📞 Telefon Client", value=default_tel)

            p_data = st.date_input("📅 Dată Programare", value=date.today(), min_value=date.today())

        with col_in2:
            p_stilist = st.selectbox("💈 Stilist / Barber", stilisti_disponibili, index=default_client_stilist_idx)
            df_serv_all = st.session_state.serv_df
            serv_filtered = df_serv_all[df_serv_all["Stilist"] == p_stilist]
            if serv_filtered.empty:
                serv_filtered = df_serv_all
                
            st.markdown("##### ✂️ Alege Serviciile Dorite")
            selected_services = []
            total_pret = 0
            total_durata = 0
            for idx, s_row in serv_filtered.iterrows():
                s_name = s_row["Serviciu"]
                s_pret = int(float(s_row["Preț"]) if pd.notna(s_row["Preț"]) else 50)
                s_dur = int(float(s_row["Durată (min)"]) if pd.notna(s_row["Durată (min)"]) else 30)
                if st.checkbox(f"{s_name} - {s_pret} RON ({s_dur} min)", key=f"srv_bifat_{p_stilist}_{idx}"):
                    selected_services.append(s_name)
                    total_pret += s_pret
                    total_durata += s_dur

            st.markdown(f'<div style="background: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 8px; margin-top: 5px; font-size: 13px;">⏱️ Durată: <b>{total_durata} min</b> | 💰 <b>Total: {total_pret} RON</b></div>', unsafe_allow_html=True)

            all_possible_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30"]
            data_str = p_data.strftime("%Y-%m-%d")
            dur_check = total_durata if total_durata > 0 else 30
            
            available_slots = []
            slot_options_admin = []
            slot_map = {}
            
            for slot in all_possible_slots:
                has_ov, _ = check_overlap(p_stilist, data_str, slot, dur_check)
                try:
                    t_s = datetime.strptime(slot, "%H:%M")
                    t_e = t_s + timedelta(minutes=dur_check)
                    if t_e.time() <= datetime.strptime("20:00", "%H:%M").time():
                        if not has_ov:
                            available_slots.append(slot)
                        label_slot = f"🔴 {slot} - Ocupat" if has_ov else f"🟢 {slot} - Disponibil"
                        slot_options_admin.append(label_slot)
                        slot_map[label_slot] = slot
                except:
                    pass

            if not is_admin_or_stylist:
                if not available_slots:
                    st.warning("Nu există sloturi disponibile pentru data selectată la acest stilist.")
                    p_ora = None
                else:
                    p_ora = st.selectbox("⏰ Alege Slot Orar Disponibil", available_slots)
            else:
                sel_slot_label = st.selectbox("⏰ Alege Ora Start", slot_options_admin)
                p_ora = slot_map.get(sel_slot_label, None)

            p_obs = st.text_area("📝 Observații", height=68)

        submit_btn = st.form_submit_button("🚀 SALVEAZĂ PROGRAMAREA", use_container_width=True)
        if submit_btn:
            target_client_name = client_nume if (is_admin_or_stylist or not client_nume) else current_user
            if not target_client_name:
                st.toast("Te rog introdu numele clientului!", icon="❌")
            elif not selected_services:
                st.toast("Te rog să bifezi cel puțin un serviciu!", icon="❌")
            elif not p_ora:
                st.toast("Te rog să selectezi un slot orar valid!", icon="❌")
            else:
                try:
                    ora_sfarsit = (datetime.strptime(p_ora, "%H:%M") + timedelta(minutes=total_durata if total_durata > 0 else 30)).strftime("%H:%M")
                except:
                    ora_sfarsit = "10:30"
                new_nr = int(st.session_state.prog_df["Nr. Programare"].max() + 1) if not st.session_state.prog_df.empty and pd.notna(st.session_state.prog_df["Nr. Programare"].max()) else 1
                new_row = pd.DataFrame([{
                    "Nr. Programare": new_nr, "Dată": data_str, "Ora Start": p_ora, "Ora Sfârșit": ora_sfarsit,
                    "Client": target_client_name, "Telefon": format_phone_input(client_tel), "Serviciu": ", ".join(selected_services),
                    "Stilist": p_stilist, "Preț": total_pret, "Durată": total_durata if total_durata > 0 else 30,
                    "Status": "Confirmat", "Observații": p_obs, "Status Modificare": "", "Noua Dată": "", "Noua Ora": "", "Noul Serviciu": "", "Motiv Refuz": ""
                }])
                st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
                save_all()
                
                # Trimitere WhatsApp confirmare
                u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == target_client_name]
                user_api = u_row.iloc[0]["APIKey"] if not u_row.empty else None
                msg_whats = f"Salut {target_client_name}, programarea ta la Denis Concept Salon cu {p_stilist} pentru data de {format_ro_date(data_str)} la ora {p_ora} a fost confirmata!"
                send_free_automatic_whatsapp(format_phone_input(client_tel), msg_whats, user_api)
                
                st.toast("Programare salvată și trimisă pe WhatsApp cu succes!", icon="✅")
                trigger_rerun()

elif is_admin_or_stylist and selected_page == "📅 Programările mele":
    st.markdown(f"### 📅 Programările mele — {current_user}")
    df_p = st.session_state.prog_df.copy()
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        view_mode = st.selectbox("Perioadă", ["Toate", "Azi", "Mâine", "Săptămâna aceasta", "Programări Viitoare"])
    with col_f2:
        fil_stilist = st.selectbox("Stilist", options=["Toți"] + stilisti_disponibili, index=1 if current_user in stilisti_disponibili else 0)

    today = date.today()
    if not df_p.empty:
        df_p = df_p[df_p["Status"] == "Confirmat"]
        df_p["Dată_dt"] = pd.to_datetime(df_p["Dată"], errors="coerce")
        if view_mode == "Azi": df_p = df_p[df_p["Dată"] == str(today)]
        elif view_mode == "Mâine": df_p = df_p[df_p["Dată"] == str(today + timedelta(days=1))]
        elif view_mode == "Programări Viitoare": df_p = df_p[df_p["Dată_dt"].dt.date >= today]
        if fil_stilist != "Toți": df_p = df_p[df_p["Stilist"] == fil_stilist]
        if "Dată_dt" in df_p.columns: df_p = df_p.drop(columns=["Dată_dt"])

    if not df_p.empty:
        st.markdown(render_lux_table(df_p), unsafe_allow_html=True)
    else:
        st.info("Nu există programări active conform filtrelor.")

elif not is_admin_or_stylist and selected_page == "📜 Programări curente & modificări":
    st.markdown(f"### ⚙️ Programări curente & modificări — {current_user}")
    client_progs = st.session_state.prog_df[st.session_state.prog_df["Client"].str.contains(current_user, case=False, na=False)] if not st.session_state.prog_df.empty else pd.DataFrame()
    
    st.markdown("##### 📅 Programările Tale Active")
    active_progs = client_progs[client_progs["Status"] == "Confirmat"]
    if not active_progs.empty:
        st.markdown(render_lux_table(active_progs), unsafe_allow_html=True)
    else:
        st.info("Nu ai programări active.")

    st.markdown("---")
    st.markdown("##### ✏️ Anulare sau Modificare Programare")
    viitoare = client_progs[(client_progs["Dată"] >= str(date.today())) & (client_progs["Status"] == "Confirmat")]
    if not viitoare.empty:
        prog_options = {f"Data: {format_ro_date(r['Dată'])} | Ora: {r['Ora Start']} | {r['Serviciu']}": int(r['Nr. Programare']) for _, r in viitoare.iterrows()}
        sel_lbl = st.selectbox("Alege programarea", list(prog_options.keys()))
        nr_sel = prog_options[sel_lbl]
        selected_row = client_progs[client_progs["Nr. Programare"] == nr_sel].iloc[0]

        tab_m1, tab_m2 = st.tabs(["❌ Anulare", "✏️ Solicită Modificare"])
        with tab_m1:
            if st.button("❌ Confirmă Anularea", use_container_width=True):
                st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_sel, "Status"] = "Anulat"
                save_all()
                
                # Notificare WhatsApp anulare
                u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
                user_api = u_row.iloc[0]["APIKey"] if not u_row.empty else None
                user_tel = u_row.iloc[0]["Telefon"] if not u_row.empty else MASTER_WHATSAPP_PHONE
                msg_cancel = f"Salut {current_user}, programarea ta din data de {format_ro_date(selected_row['Dată'])} a fost anulata cu succes."
                send_free_automatic_whatsapp(user_tel, msg_cancel, user_api)
                
                st.toast("Programare anulată și notificare trimisă pe WhatsApp!", icon="⚠️")
                trigger_rerun()
        with tab_m2:
            with st.form(f"mod_form_{nr_sel}"):
                new_date = st.date_input("Noua Dată", value=datetime.strptime(selected_row["Dată"], "%Y-%m-%d").date(), min_value=date.today())
                stilist_alocat = selected_row["Stilist"]
                durata_act = int(float(selected_row["Durată"])) if pd.notna(selected_row["Durată"]) else 30
                
                all_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30"]
                date_str_n = new_date.strftime("%Y-%m-%d")
                avail_mod = []
                for slot in all_slots:
                    has_ov, _ = check_overlap(stilist_alocat, date_str_n, slot, durata_act, exclude_nr=nr_sel)
                    try:
                        if (datetime.strptime(slot, "%H:%M") + timedelta(minutes=durata_act)).time() <= datetime.strptime("20:00", "%H:%M").time() and not has_ov:
                            avail_mod.append(slot)
                    except:
                        pass
                new_ora = st.selectbox("Slot Disponibil", avail_mod) if avail_mod else None
                new_serv = st.text_input("Serviciu", value=selected_row["Serviciu"])
                
                if st.form_submit_button("Trimite Solicitarea de Modificare", use_container_width=True):
                    if not new_ora:
                        st.toast("Selectează un orar valid!", icon="❌")
                    else:
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_sel, "Status Modificare"] = "În Așteptare"
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_sel, "Noua Dată"] = date_str_n
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_sel, "Noua Ora"] = new_ora
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_sel, "Noul Serviciu"] = new_serv
                        save_all()
                        st.toast("Solicitarea de modificare a fost trimisă stilistului!", icon="✅")
                        trigger_rerun()
    else:
        st.info("Nu ai programări viitoare de modificat.")

elif is_admin_or_stylist and selected_page == "⚙️ Gestiune & Aprobări":
    st.markdown("### ⚙️ Gestiune & Aprobări")
    pending = st.session_state.prog_df[st.session_state.prog_df["Status Modificare"] == "În Așteptare"]
    if not pending.empty:
        for _, req_r in pending.iterrows():
            with st.container(border=True):
                st.markdown(f"**Client:** {req_r['Client']} | ➡️ Nou: {format_ro_date(req_r['Noua Dată'])} {req_r['Noua Ora']}")
                if st.button(f"🔍 Gestionează cererea ({req_r['Client']})", key=f"pop_{req_r['Nr. Programare']}"):
                    approval_popup(req_r)
    else:
        st.info("Nu există cereri în așteptare.")

    st.markdown("---")
    st.markdown("##### 📋 Toate Programările Active")
    st.markdown(render_lux_table(st.session_state.prog_df[st.session_state.prog_df["Status"] != "Anulat"]), unsafe_allow_html=True)

elif is_admin_or_stylist and selected_page == "💇‍♂️ Servicii & Prețuri":
    st.markdown("### 💇‍♂️ Catalog Servicii")
    st.markdown(render_lux_table(st.session_state.serv_df), unsafe_allow_html=True)

elif is_admin_or_stylist and ("Recenzii" in selected_page):
    st.markdown("### ⭐ Moderare Recenzii")
    st.markdown(render_lux_table(st.session_state.rev_df), unsafe_allow_html=True)

elif is_stylist and selected_page == "📊 Raport Financiarul Meu":
    st.markdown(f"### 📊 Raport Financiar — {current_user}")
    df_f = st.session_state.prog_df[st.session_state.prog_df["Stilist"] == current_user] if not st.session_state.prog_df.empty else pd.DataFrame()
    total_inc = df_f[df_f["Status"] == "Confirmat"]["Preț"].sum() if not df_f.empty else 0
    st.markdown(f'<div class="salon-card"><div class="metric-lbl">Încasări Active</div><div class="metric-val">{total_inc} RON</div></div>', unsafe_allow_html=True)

elif is_admin and selected_page == "📊 Raport Financiar":
    st.markdown("### 📊 Raport Financiar General")
    df_f = st.session_state.prog_df
    total_inc = df_f[df_f["Status"] == "Confirmat"]["Preț"].sum() if not df_f.empty else 0
    st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Încasări Salon</div><div class="metric-val">{total_inc} RON</div></div>', unsafe_allow_html=True)

elif is_admin and selected_page == "⚙️ Setări & Utilizatori":
    st.markdown("### ⚙️ Setări & Utilizatori / API WhatsApp")
    st.markdown(render_lux_table(st.session_state.users_df[["Utilizator", "Rol", "Telefon", "APIKey"]]), unsafe_allow_html=True)

elif not is_admin_or_stylist and selected_page == "⭐ Recenzii Salon & Istoricul Meu":
    st.markdown("### ⭐ Recenzii Salon")
    aprobate = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
    for _, row in aprobate.iterrows():
        st.markdown(f"**👤 {row['Client']}** ({row['Stilist']}): ⭐ {row['Rating']}<br>> *{row['Comentariu']}*", unsafe_allow_html=True)
