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
# CONFIGURARE FIȘIER CONFIG.TOML STREAMLIT (ELIMINARE DEFINITIVĂ ROȘU MULTISELECT)
# ==========================================
os.makedirs(".streamlit", exist_ok=True)
config_toml_content = """
[theme]
primaryColor = "#e5c158"
backgroundColor = "#0f1117"
secondaryBackgroundColor = "#1a202c"
textColor = "#f3f4f6"
font = "sans serif"
"""
with open(".streamlit/config.toml", "w") as f:
    f.write(config_toml_content.strip())

# ==========================================
# CONFIGURARE PAGINĂ & DESIGN SALON DE LUX
# ==========================================
st.set_page_config(
    page_title="Denis Concept Salon | Luxury Experience",
    layout="wide",
    page_icon="✂️",
    initial_sidebar_state="expanded",
)

def apply_background_style(is_logged_in):
    salon_bg_url = "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=1920&q=80"
    
    # Valoare de blur mai mare și accentuată după logare
    blur_val = "16px" if is_logged_in else "4px"
    
    css_template = """
    <style>
    /* Fundal cu efect real de blur folosind un strat pseudo-element dedicat */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('REPLACE_URL') center/cover fixed !important;
        filter: blur(BLUR_VAL);
        -webkit-filter: blur(BLUR_VAL);
        transform: scale(1.1);
        z-index: -999999;
    }
    .stApp {
        background: linear-gradient(135deg, rgba(15, 17, 23, 0.85) 0%, rgba(22, 26, 34, 0.92) 100%) !important;
        color: #f3f4f6 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* STILIZARE RIGUROASĂ AURIU-LUX PENTRU TOATE TAG-URILE DIN ST.MULTISELECT */
    div[data-baseweb="tag"], 
    span[data-baseweb="tag"], 
    .stMultiSelect div[data-baseweb="tag"], 
    .stMultiSelect span[data-baseweb="tag"],
    [data-testid="stMultiSelect"] div[data-baseweb="tag"],
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #e5c158 0%, #c5a059 100%) !important;
        background-color: #e5c158 !important;
        color: #090a0f !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        border: 1px solid #d4af37 !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3) !important;
    }
    div[data-baseweb="tag"] span, 
    span[data-baseweb="tag"] span, 
    .stMultiSelect [data-baseweb="tag"] span,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] span {
        color: #090a0f !important;
    }
    div[data-baseweb="tag"] svg, 
    span[data-baseweb="tag"] svg, 
    .stMultiSelect [data-baseweb="tag"] svg,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
        fill: #090a0f !important;
    }
    div[data-baseweb="tag"] svg:hover, 
    span[data-baseweb="tag"] svg:hover {
        opacity: 0.7;
    }
    </style>
    """
    final_css = css_template.replace("REPLACE_URL", salon_bg_url).replace("BLUR_VAL", blur_val)
    st.markdown(final_css, unsafe_allow_html=True)

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
    .highlight-box { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px; border-radius: 14px; border: 2px solid #e5c158; margin-bottom: 18px; box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4); }

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
MASTER_WHATSAPP_PHONE = "35796005530"
MASTER_WHATSAPP_APIKEY = "9926434"

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
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/{clean_phone}?text={encoded_text}"

def remove_diacritics(text):
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

def send_free_automatic_whatsapp(phone, message, apikey=None):
    target_apikey = str(apikey).strip() if apikey and pd.notna(apikey) and str(apikey).strip() != "" and str(apikey).strip() != "nan" else MASTER_WHATSAPP_APIKEY
    target_phone = str(phone).strip() if phone and pd.notna(phone) and str(phone).strip() != "" else MASTER_WHATSAPP_PHONE
    
    clean_phone = "".join(filter(str.isdigit, str(target_phone)))
    if clean_phone.startswith("0"):
        clean_phone = "4" + clean_phone
    elif not clean_phone.startswith("40") and len(clean_phone) == 9:
        clean_phone = "40" + clean_phone
        
    clean_msg = remove_diacritics(message)
    encoded_text = urllib.parse.quote(clean_msg)
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
        day_name = RO_DAYS[dt.weekday()]
        month_name = RO_MONTHS[dt.month]
        return f"{day_name}, {dt.day} {month_name} {dt.year}"
    except:
        return str(d_input)

def render_lux_table(df):
    if df.empty:
        return "<div style='text-align: center; padding: 25px; color: #9ca3af; background: #131722; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.2);'>Nu există înregistrări de afișat momentan.</div>"
    
    df_render = df.copy()
    
    if all(col in df_render.columns for col in ["Dată", "Ora Start", "Ora Sfârșit"]):
        combined_col = []
        for _, row in df_render.iterrows():
            d_formatted = format_ro_date(row["Dată"])
            start = row["Ora Start"]
            end = row["Ora Sfârșit"]
            if start and end and str(start) not in ["nan", "NaN", "None", ""]:
                combined_col.append(f"{d_formatted} | {start} - {end}")
            else:
                combined_col.append(d_formatted)
        df_render["Dată & Oră"] = combined_col
        df_render = df_render.drop(columns=["Dată", "Ora Start", "Ora Sfârșit"])
        cols = list(df_render.columns)
        if "Dată & Oră" in cols:
            cols.insert(0, cols.pop(cols.index("Dată & Oră")))
            df_render = df_render[cols]

    for drop_col in ["Nr. Programare", "ID"]:
        if drop_col in df_render.columns:
            df_render = df_render.drop(columns=[drop_col])
            
    if "Status Modificare" in df_render.columns:
        for i, row in df_render.iterrows():
            if str(row.get("Status Modificare")) == "În Așteptare":
                df_render.at[i, "Status"] = "În Așteptare"

    html = "<div style='overflow-x: auto; margin-bottom: 20px;'><table style='width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #131722 0%, #1a202c 100%); border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.6); border: 1px solid rgba(212, 175, 55, 0.3); font-family: sans-serif; font-size: 13px;'>"
    html += "<thead><tr style='background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); color: #e5c158; text-transform: uppercase; font-size: 11px; letter-spacing: 1.5px; border-bottom: 2px solid rgba(212, 175, 55, 0.4);'>"
    for col in df_render.columns:
        if col != "Status Modificare":
            html += f"<th style='padding: 16px 14px; text-align: center; font-weight: 700;'>{col}</th>"
    html += "</tr></thead><tbody>"
    
    for idx, row in df_render.iterrows():
        row_bg = "#131722" if idx % 2 == 0 else "#181d29"
        html += f"<tr style='background-color: {row_bg}; border-bottom: 1px solid rgba(255, 255, 255, 0.06); transition: background 0.2s;' onmouseover=\"this.style.backgroundColor='#222736'\" onmouseout=\"this.style.backgroundColor='{row_bg}'\">"
        
        for col in df_render.columns:
            if col == "Status Modificare":
                continue
            val = str(row[col])
            if val == "nan" or val == "NaN" or val == "None":
                val = ""
            
            cell_style = "padding: 14px 12px; text-align: center; color: #f3f4f6;"
            if col == "Status":
                if val in ["Confirmat"]:
                    val = f"<span style='background: rgba(30, 58, 138, 0.6); color: #93c5fd; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(59, 130, 246, 0.4); display: inline-block; text-transform: uppercase; letter-spacing: 0.5px;'>{val}</span>"
                elif val in ["În Așteptare"]:
                    val = f"<span style='background: rgba(120, 80, 20, 0.5); color: #fef08a; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(212, 175, 55, 0.4); display: inline-block; text-transform: uppercase; letter-spacing: 0.5px;'>{val}</span>"
                elif val in ["Efectuat", "Aprobat"]:
                    val = f"<span style='background: rgba(6, 78, 59, 0.6); color: #6ee7b7; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(16, 185, 129, 0.4); display: inline-block; text-transform: uppercase; letter-spacing: 0.5px;'>{val}</span>"
                elif val in ["Anulat", "Respins"]:
                    val = f"<span style='background: rgba(127, 29, 29, 0.6); color: #fca5a5; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 11px; border: 1px solid rgba(239, 68, 68, 0.4); display: inline-block; text-transform: uppercase; letter-spacing: 0.5px;'>{val}</span>"
            
            html += f"<td style='{cell_style}'>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

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
# SESIUNE, PERSISTENȚĂ & AUTENTIFICARE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

if not st.session_state.logged_in:
    saved_user = st.query_params.get("logged_user")
    saved_role = st.query_params.get("role")
    if saved_user and saved_role:
        st.session_state.logged_in = True
        st.session_state.user = saved_user
        st.session_state.role = saved_role

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
            remember_me = st.checkbox("Ține-mă minte (Rămâi conectat)")
            
            submit_login = st.form_submit_button("✨ Intră în Cont", use_container_width=True)
            if submit_login:
                users = st.session_state.users_df
                match = users[(users["Utilizator"] == u_input) & (users["Parolă"] == p_input)]
                if not match.empty:
                    role_val = match.iloc[0]["Rol"]
                    st.session_state.logged_in = True
                    st.session_state.user = u_input
                    st.session_state.role = role_val
                    
                    if remember_me or role_val in ["Administrator", "Stilist"]:
                        st.query_params["logged_user"] = u_input
                        st.query_params["role"] = role_val
                        
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

@st.dialog("Gestionează Cererea de Modificare")
def approval_popup(req_r):
    st.markdown(f"**Client:** {req_r['Client']} | **Stilist Asignat:** {req_r['Stilist']}")
    st.markdown(f"📅 Data actuală: `{format_ro_date(req_r['Dată'])} {req_r['Ora Start']}`")
    st.markdown(f"➡️ **Solicitat nou:** `{format_ro_date(req_r['Noua Dată'])} {req_r['Noua Ora']}` | Serviciu nou: *{req_r['Noul Serviciu']}*")
    
    req_dur = int(float(req_r["Durată"])) if pd.notna(req_r["Durată"]) else 30
    has_ov_req, _ = check_overlap(req_r["Stilist"], req_r["Noua Dată"], req_r["Noua Ora"], req_dur, exclude_nr=req_r["Nr. Programare"])
    if has_ov_req:
        st.markdown("""
        <div class="overlap-alert">
            ⚠️ <b>ATENȚIE SUPRAPUNERE:</b> Noul interval orar solicitat se suprapune cu o altă programare existentă pentru acest stilist!
        </div>
        """, unsafe_allow_html=True)

    motiv_refuz = st.text_input("Motiv respingere (opțional)", key=f"popup_motiv_{req_r['Nr. Programare']}")
    
    col_pop1, col_pop2 = st.columns(2)
    with col_pop1:
        if st.button("✅ Aprobă Modificarea", use_container_width=True):
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Dată"] = req_r["Noua Dată"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Ora Start"] = req_r["Noua Ora"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Serviciu"] = req_r["Noul Serviciu"]
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Aprobat"
            save_all()
            st.toast("Modificarea a fost aprobată cu succes!", icon="✅")
            st.rerun()
    with col_pop2:
        if st.button("❌ Respinge Solicitarea", use_container_width=True):
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Status Modificare"] = "Respins"
            st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == int(req_r['Nr. Programare']), "Motiv Refuz"] = motiv_refuz if motiv_refuz else "Fără motiv specificat"
            save_all()
            st.toast("Modificarea a fost respinsă.", icon="⚠️")
            st.rerun()

if is_admin_or_stylist:
    df_prog_all = st.session_state.prog_df
    pending_modifs = df_prog_all[df_prog_all["Status Modificare"] == "În Așteptare"]
    if not pending_modifs.empty:
        st.markdown(f"""
        <div class="overlap-alert">
            🔔 <b>ATENȚIE!</b> Există <b>{len(pending_modifs)}</b> cereri de modificare programare în așteptarea aprobării!
        </div>
        """, unsafe_allow_html=True)
        for _, req_item in pending_modifs.iterrows():
            if st.button(f"👉 Gestionează cererea pentru clientul {req_item['Client']} ({format_ro_date(req_item['Noua Dată'])} - {req_item['Noua Ora']})", key=f"top_btn_popup_{req_item['Nr. Programare']}"):
                approval_popup(req_item)

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
        new_phone_input = st.text_input("Număr Telefon", value=current_tel, placeholder="+40 7xxxxxxxx sau +357...")
        if st.form_submit_button("Salvează Telefonul"):
            formatted_p = format_phone_input(new_phone_input)
            st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == current_user, "Telefon"] = formatted_p
            save_all()
            st.toast("Telefonul a fost actualizat cu succes!", icon="✅")
            trigger_rerun()
    st.sidebar.markdown("---")
    
    wa_support_link = get_whatsapp_link(MASTER_WHATSAPP_PHONE, f"Salut, sunt {current_user} și doresc informații despre Denis Concept Salon.")
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
    st.query_params.clear()
    trigger_rerun()

st.sidebar.markdown("---")

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
# DEFINIRE TAB-URI
# ==========================================
stilisti_disponibili = ["Adrian", "Andreea", "Alex", "Denis"]
default_stylist_idx = 0
if is_admin_or_stylist and current_user in stilisti_disponibili:
    default_stylist_idx = stilisti_disponibili.index(current_user)

if is_admin:
    tab_titles = [
        "➕ Adaugă Programare", 
        "📅 Programările mele", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii", 
        "📊 Raport Financiar", 
        "⚙️ Setări & Utilizatori"
    ]
elif is_stylist:
    tab_titles = [
        "➕ Adaugă Programare", 
        "📅 Programările mele", 
        "⚙️ Gestiune & Aprobări", 
        "💇‍♂️ Servicii & Prețuri", 
        "⭐ Recenzii & Istoric",
        "📊 Raport Financiarul Meu"
    ]
else:
    tab_titles = [
        "📅 Programează-te", 
        "📜 Programări curente & modificări programări", 
        "⭐ Recenzii Salon & Istoricul Meu"
    ]

tabs = st.tabs(tab_titles)

# ==========================================
# TAB 1: ADAUGĂ PROGRAMARE
# ==========================================
with tabs[0]:
    if is_admin_or_stylist:
        st.markdown(f"### ➕ Adaugă Programare Nouă (Admin / Stilist — {current_user})")
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            existing_clients = sorted(st.session_state.prog_df["Client"].dropna().unique().tolist()) if not st.session_state.prog_df.empty else []
            existing_users = sorted(st.session_state.users_df[st.session_state.users_df["Rol"] == "Client"]["Utilizator"].dropna().unique().tolist())
            all_known_clients = sorted(list(set(existing_clients + existing_users)))
            
            client_input_mode = st.radio("Mod selectare client", ["Din agendă / clienți existenți", "Client nou (manual)"], horizontal=True, key="admin_client_mode_radio")
            
            if client_input_mode == "Din agendă / clienți existenți" and all_known_clients:
                client_nume = st.selectbox("👤 Selectează Client din Agendă", all_known_clients, key="admin_agenda_client_sel")
                
                u_match = st.session_state.users_df[st.session_state.users_df["Utilizator"] == client_nume]
                default_tel_agenda = "+40 "
                if not u_match.empty and pd.notna(u_match.iloc[0]["Telefon"]):
                    default_tel_agenda = format_phone_input(u_match.iloc[0]["Telefon"])
                else:
                    p_match = st.session_state.prog_df[st.session_state.prog_df["Client"] == client_nume]
                    if not p_match.empty and pd.notna(p_match.iloc[0]["Telefon"]):
                        default_tel_agenda = format_phone_input(p_match.iloc[0]["Telefon"])
                client_tel = st.text_input("📞 Telefon Client", value=default_tel_agenda, key="admin_agenda_tel_inp")
            else:
                client_nume = st.text_input("👤 Nume Client Nou", value="", key="admin_new_client_name_inp")
                client_tel = st.text_input("📞 Telefon Client", value="+40 ", placeholder="+40 7xxxxxxxx sau +357...", key="admin_new_client_tel_inp")

            p_data = st.date_input("📅 Dată Programare", value=date.today(), min_value=date.today(), key="admin_prog_date_picker")

        with col_in2:
            p_stilist = st.selectbox("💈 Stilist / Barber", stilisti_disponibili, index=default_stylist_idx, key="admin_stylist_picker")

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
                if st.checkbox(f"{s_name} - {s_pret} RON ({s_dur} min)", key=f"admin_srv_bifat_{p_stilist}_{idx}"):
                    selected_services.append(s_name)
                    total_pret += s_pret
                    total_durata += s_dur
            
            st.markdown(f"""
            <div style="background: rgba(212, 175, 55, 0.15); padding: 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.4); margin: 10px 0; font-size: 14px;">
                ⏱️ Durată Totală: <b>{total_durata} min</b> | 💰 Total de Plată: <b>{total_pret} RON</b>
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
                    label_slot = f"🔴 {slot} - Ocupat (Suprapunere)"
                else:
                    label_slot = f"🟢 {slot} - Disponibil (Liber)"
                slot_options_admin.append(label_slot)
                slot_map_admin[label_slot] = slot

            sel_slot_adm_label = st.selectbox("⏰ Alege Ora Start", slot_options_admin, key="admin_time_slot_sel")
            p_ora = slot_map_admin[sel_slot_adm_label]

            p_obs = st.text_area("📝 Observații", height=68, key="admin_obs_inp")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvează Programarea (Admin)", use_container_width=True, key="admin_submit_btn"):
            if not client_nume:
                st.toast("Te rog introdu numele clientului!", icon="❌")
            elif not selected_services:
                st.toast("Te rog să bifezi cel puțin un serviciu!", icon="❌")
            elif not p_ora:
                st.toast("Te rog să selectezi un slot orar valid!", icon="❌")
            else:
                dup_check = st.session_state.prog_df[
                    (st.session_state.prog_df["Client"].str.lower() == client_nume.lower()) &
                    (st.session_state.prog_df["Dată"] == data_str) &
                    (st.session_state.prog_df["Ora Start"] == p_ora) &
                    (st.session_state.prog_df["Status"] != "Anulat")
                ]
                if not dup_check.empty:
                    st.toast(f"Ai deja o programare înregistrată pentru ziua de {format_ro_date(data_str)} la ora {p_ora}!", icon="⚠️")
                else:
                    try:
                        t_start_obj = datetime.strptime(p_ora, "%H:%M")
                        t_end_obj = t_start_obj + timedelta(minutes=total_durata if total_durata > 0 else 30)
                        ora_sfarsit = t_end_obj.strftime("%H:%M")
                    except:
                        ora_sfarsit = "10:30"

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
                    st.toast(f"Programare salvată cu succes pentru {client_nume}! Total: {total_pret} RON.", icon="✅")
                    trigger_rerun()

    else:
        st.markdown("### ➕ Programare Nouă")
        
        default_tel = "+40 "
        user_u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == current_user]
        if not user_u_row.empty and pd.notna(user_u_row.iloc[0]["Telefon"]):
            default_tel = format_phone_input(user_u_row.iloc[0]["Telefon"])

        client_progs_all = st.session_state.prog_df[st.session_state.prog_df["Client"].str.contains(current_user, case=False, na=False)] if not st.session_state.prog_df.empty else pd.DataFrame()
        default_client_stilist_idx = 0
        if not client_progs_all.empty:
            client_progs_all["temp_dt"] = pd.to_datetime(client_progs_all["Dată"] + " " + client_progs_all["Ora Start"], errors="coerce")
            client_progs_all = client_progs_all.sort_values("temp_dt", ascending=False)
            last_used_stylist = client_progs_all.iloc[0]["Stilist"]
            if last_used_stylist in stilisti_disponibili:
                default_client_stilist_idx = stilisti_disponibili.index(last_used_stylist)

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            client_nume = st.text_input("👤 Nume Client", value=current_user, disabled=True, key="client_name_inp")
            client_tel = st.text_input("📞 Telefon Client (Prefix +40 sau altul ex. +357)", value=default_tel, placeholder="+40 7xxxxxxxx sau +357...", key="client_tel_inp")
            p_data = st.date_input("📅 Dată Programare", value=date.today(), min_value=date.today(), key="client_date_inp")

        with col_in2:
            p_stilist = st.selectbox("💈 Stilist / Barber", stilisti_disponibili, index=default_client_stilist_idx, key="client_stylist_inp")

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
                if st.checkbox(f"{s_name} - {s_pret} RON ({s_dur} min)", key=f"client_srv_bifat_{p_stilist}_{idx}"):
                    selected_services.append(s_name)
                    total_pret += s_pret
                    total_durata += s_dur
            
            st.markdown(f"""
            <div style="background: rgba(212, 175, 55, 0.15); padding: 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.4); margin: 10px 0; font-size: 14px;">
                ⏱️ Durată Totală: <b>{total_durata} min</b> | 💰 Total de Plată: <b>{total_pret} RON</b>
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
                st.info("👈 Bifează cel puțin un serviciu pentru a vedea orarele libere.")
                p_ora = None
            elif not available_slots:
                st.warning("⚠️ Nu există sloturi disponibile pentru data selectată și durata serviciului aleasă. Încearcă altă dată sau alt stilist.")
                p_ora = None
            else:
                p_ora = st.selectbox("⏰ Alege Slot Orar Disponibil", available_slots, key="client_slot_sel")

            p_obs = st.text_area("📝 Observații / Preferințe", height=68, key="client_obs_inp")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvează Programarea", use_container_width=True, key="client_submit_btn"):
            if not client_nume:
                st.toast("Te rog introdu numele clientului!", icon="❌")
            elif not selected_services:
                st.toast("Te rog să bifezi cel puțin un serviciu!", icon="❌")
            elif not p_ora:
                st.toast("Te rog să selectezi un slot orar valid!", icon="❌")
            else:
                dup_check = st.session_state.prog_df[
                    (st.session_state.prog_df["Client"].str.lower() == client_nume.lower()) &
                    (st.session_state.prog_df["Dată"] == data_str) &
                    (st.session_state.prog_df["Ora Start"] == p_ora) &
                    (st.session_state.prog_df["Status"] != "Anulat")
                ]
                if not dup_check.empty:
                    st.toast(f"Ai deja o programare înregistrată pentru ziua de {format_ro_date(data_str)} la ora {p_ora}!", icon="⚠️")
                else:
                    try:
                        t_start_obj = datetime.strptime(p_ora, "%H:%M")
                        t_end_obj = t_start_obj + timedelta(minutes=total_durata if total_durata > 0 else 30)
                        ora_sfarsit = t_end_obj.strftime("%H:%M")
                    except:
                        ora_sfarsit = "10:30"

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
                    st.toast(f"Programare salvată cu succes! Total de plată: {total_pret} RON.", icon="✅")
                    trigger_rerun()

# ==========================================
# TAB 2: PROGRAMĂRILE MELE / PROGRAMĂRI CURENTE
# ==========================================
with tabs[1]:
    if is_admin_or_stylist:
        st.markdown(f"### 📅 Programările mele — {current_user}")
        df_p = st.session_state.prog_df.copy()
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            view_mode = st.selectbox("Vizualizare Perioadă", ["Toate", "Azi", "Mâine", "Săptămâna aceasta", "Săptămâna viitoare", "Luna aceasta", "Programări Viitoare", "Programări Trecute"])
        with col_f2:
            # MULTISELECT STILIZAT AURIU
            fil_stilist = st.multiselect("Alege Stilist", options=stilisti_disponibili, default=[current_user] if current_user in stilisti_disponibili else stilisti_disponibili, key="admin_fil_stilist_ms")
        with col_f3:
            # MULTISELECT STILIZAT AURIU
            fil_status = st.multiselect("Alege Status Programare", options=["Confirmat", "În Așteptare"], default=["Confirmat", "În Așteptare"], key="admin_fil_status_ms")

        today = date.today()
        if not df_p.empty:
            df_p = df_p[(df_p["Status"] == "Confirmat") | (df_p["Status Modificare"] == "În Așteptare") | (df_p["Status"] == "În Așteptare")]
            
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

            if fil_stilist:
                df_p = df_p[df_p["Stilist"].isin(fil_stilist)]
            if fil_status:
                df_p = df_p[df_p["Status"].isin(fil_status)]
            
            if "Dată_dt" in df_p.columns:
                df_p = df_p.drop(columns=["Dată_dt"])

        if not df_p.empty:
            df_p["is_waiting"] = df_p["Status"].apply(lambda x: 0 if str(x) == "În Așteptare" else 1)
            df_p = df_p.sort_values(by=["is_waiting", "Dată", "Ora Start"]).drop(columns=["is_waiting"])

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
            st.markdown(render_lux_table(df_display_admin), unsafe_allow_html=True)
            
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
                        format_func=lambda x: f"Client: {progs_on_date[progs_on_date['Nr. Programare']==x].iloc[0]['Client']} ({progs_on_date[progs_on_date['Nr. Programare']==x].iloc[0]['Ora Start']})"
                    )
                else:
                    selected_prog_wa_nr = None
                    st.info("Nu există programări în data selectată.")

            if selected_prog_wa_nr:
                row_sel_wa = df_p[df_p["Nr. Programare"] == selected_prog_wa_nr].iloc[0]
                cli_phone_wa = row_sel_wa["Telefon"]
                wa_msg_admin = f"Salut {row_sel_wa['Client']}, te contactam de la Denis Concept Salon in legatura cu programarea ta din data de {format_ro_date(row_sel_wa['Dată'])} la ora {row_sel_wa['Ora Start']}."
                wa_link_admin = get_whatsapp_link(cli_phone_wa, wa_msg_admin)
                st.markdown(f'<a href="{wa_link_admin}" target="_blank" class="whatsapp-btn">💬 Trimite WhatsApp către {row_sel_wa["Client"]}</a>', unsafe_allow_html=True)
        else:
            st.info("Nu există programări care să corespundă filtrelor selectate.")

    else:
        st.markdown(f"### ⚙️ Programări curente & modificări programări — {current_user}")
        client_name = current_user
        df_p_all = st.session_state.prog_df.copy()
        client_progs = df_p_all[df_p_all["Client"].str.contains(client_name, case=False, na=False)] if not df_p_all.empty else pd.DataFrame()
        
        approved_modifs_client = client_progs[client_progs["Status Modificare"] == "Aprobat"]
        if not approved_modifs_client.empty:
            st.toast("Solicitarea ta de modificare a fost aprobată de către stilist!", icon="🟢")

        if "cancel_success_alert" in st.session_state:
            st.toast(st.session_state["cancel_success_alert"], icon="✅")
            del st.session_state["cancel_success_alert"]

        st.markdown("##### 📅 Programări curente")
        current_active_progs = client_progs[(client_progs["Dată"] >= str(date.today())) & (client_progs["Status"] == "Confirmat")]
        if not current_active_progs.empty:
            df_curr_display = current_active_progs[["Dată", "Ora Start", "Ora Sfârșit", "Serviciu", "Stilist", "Preț", "Durată", "Status", "Status Modificare"]].copy()
            df_curr_display["Status Modificare"] = df_curr_display["Status Modificare"].apply(lambda x: "" if str(x) in ["Niciuna", "nan", "NaN", ""] else x)
            st.markdown(render_lux_table(df_curr_display), unsafe_allow_html=True)
        else:
            st.info("Nu ai programări active momentan.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.markdown("##### ✏️ Modificare sau Anulare Programări")
        viitoare = client_progs[(client_progs["Dată"] >= str(date.today())) & (client_progs["Status"] == "Confirmat")]
        
        if not viitoare.empty:
            prog_options = {}
            for _, r in viitoare.iterrows():
                label = f"Data: {format_ro_date(r['Dată'])} | Ora: {r['Ora Start']} | Serviciu: {r['Serviciu']} | Stilist: {r['Stilist']}"
                prog_options[label] = int(r['Nr. Programare'])
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 16px 20px; border-radius: 12px; border: 2px solid #e5c158; margin-bottom: 10px; box-shadow: 0 6px 20px rgba(212, 175, 55, 0.35);">
                <b style="color: #e5c158; font-size: 15px;">👇 Alege programarea pe care vrei sa o modifici:</b>
            </div>
            """, unsafe_allow_html=True)
            
            selected_label = st.selectbox("Alege programarea pe care vrei sa o modifici", list(prog_options.keys()), label_visibility="collapsed", key="client_hist_sel_prog")
            nr_selected = prog_options[selected_label]
            selected_row = client_progs[client_progs["Nr. Programare"] == nr_selected].iloc[0]

            st.markdown(f"""
            <div class="highlight-box">
                ✨ <b style="color: #e5c158; font-size: 16px;">Programarea selectată pentru acțiune:</b><br><br>
                📅 Dată & Oră: <b style="color: #6ee7b7; font-size: 15px;">{format_ro_date(selected_row['Dată'])} | {selected_row['Ora Start']} - {selected_row['Ora Sfârșit']}</b><br>
                ✂️ Serviciu: <b>{selected_row['Serviciu']}</b> &nbsp;|&nbsp; 💈 Stilist: <b>{selected_row['Stilist']}</b>
            </div>
            """, unsafe_allow_html=True)

            tab_m1, tab_m2 = st.tabs(["❌ Anulare Programare", "✏️ Solicită Modificare Programare"])
            
            with tab_m1:
                st.markdown("<p style='color: #fca5a5; font-weight: 600;'>Apăsând butonul de mai jos, programarea de mai sus va fi anulată definitiv, iar stilistul va fi înștiințat automat prin WhatsApp cu detaliile complete.</p>", unsafe_allow_html=True)
                if st.button("❌ Confirmă Anularea Programării Selectate", key="client_cancel_btn", use_container_width=True):
                    p_dt = datetime.strptime(f"{selected_row['Dată']} {selected_row['Ora Start']}", "%Y-%m-%d %H:%M")
                    ore_ramase = (p_dt - datetime.now()).total_seconds() / 3600
                    
                    if ore_ramase < 24:
                        st.toast(f"Anularea nu este permisă! Mai sunt doar {ore_ramase:.1f} ore până la programare (limita este de 24 ore).", icon="❌")
                    else:
                        stilist_alocat = selected_row["Stilist"]
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Status"] = "Anulat"
                        save_all()
                        
                        stylist_user_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == stilist_alocat]
                        if not stylist_user_row.empty:
                            st_phone = stylist_user_row.iloc[0]["Telefon"]
                            st_apikey = stylist_user_row.iloc[0]["APIKey"]
                            
                            wa_cancel_msg = (
                                f"ANULARE PROGRAMARE\n"
                                f"Stilist: {stilist_alocat}\n"
                                f"Client: {current_user}\n"
                                f"Data & Ora: {format_ro_date(selected_row['Dată'])} | {selected_row['Ora Start']} - {selected_row['Ora Sfârșit']}\n"
                                f"Serviciu: {selected_row['Serviciu']}"
                            )
                            success_wa = send_free_automatic_whatsapp(st_phone, wa_cancel_msg, st_apikey)
                            if success_wa:
                                st.session_state["cancel_success_alert"] = "Programarea a fost anulată și înștiințarea a fost trimisă stilistului pe WhatsApp!"
                            else:
                                st.session_state["cancel_success_alert"] = "Programarea a fost anulată cu succes în sistem!"
                        else:
                            st.session_state["cancel_success_alert"] = "Programarea a fost anulată cu succes în sistem!"

                        trigger_rerun()

            with tab_m2:
                st.markdown("""
                <div class="info-alert">
                    ⚠️ <b>ATENȚIE:</b> Alege data dorită, iar sistemul îți va afișa în dropdown <b>doar sloturile orare disponibile</b>. Modificarea necesită aprobare!
                </div>
                """, unsafe_allow_html=True)
                
                new_date = st.date_input("Noua Dată Dorită", value=datetime.strptime(selected_row["Dată"], "%Y-%m-%d").date(), min_value=date.today(), key=f"client_nd_{nr_selected}")
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
                
                if st.button("✏️ Trimite Solicitarea de Modificare", use_container_width=True, key=f"btn_send_mod_{nr_selected}"):
                    if not new_ora:
                        st.toast("Te rog selectează un slot orar valid!", icon="❌")
                    else:
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Status Modificare"] = "În Așteptare"
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noua Dată"] = date_str_n
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noua Ora"] = new_ora
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == nr_selected, "Noul Serviciu"] = new_serv
                        save_all()
                        
                        stylist_user_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == stilist_alocat]
                        if not stylist_user_row.empty:
                            st_phone = stylist_user_row.iloc[0]["Telefon"]
                            st_apikey = stylist_user_row.iloc[0]["APIKey"]
                            wa_mod_msg = f"SOLICITARE MODIFICARE\nClient: {current_user}\nData: {format_ro_date(date_str_n)}\nOra: {new_ora}"
                            send_free_automatic_whatsapp(st_phone, wa_mod_msg, st_apikey)

                        st.session_state["client_mod_sent_success"] = True
                        trigger_rerun()

            if st.session_state.get("client_mod_sent_success", False):
                st.toast("Solicitarea de modificare a fost trimisă spre aprobare stilistului!", icon="✅")
                del st.session_state["client_mod_sent_success"]
        else:
            st.info("Nu ai programări viitoare pe care să le poți modifica sau anula.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.markdown("##### 📜 Istoric")
        past_history_progs = client_progs[(client_progs["Dată"] < str(date.today())) | (client_progs["Status"] != "Confirmat")]
        if not past_history_progs.empty:
            df_hist_display = past_history_progs[["Dată", "Ora Start", "Ora Sfârșit", "Serviciu", "Stilist", "Preț", "Durată", "Status", "Status Modificare"]].copy()
            df_hist_display["Status Modificare"] = df_hist_display["Status Modificare"].apply(lambda x: "" if str(x) in ["Niciuna", "nan", "NaN", ""] else x)
            st.markdown(render_lux_table(df_hist_display), unsafe_allow_html=True)
        else:
            st.info("Nu există istoric anterior înregistrat.")

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
                    st.markdown(f"**Client:** {req_r['Client']} | **Stilist Asignat:** {req_r['Stilist']}")
                    st.markdown(f"📅 Data actuală: `{format_ro_date(req_r['Dată'])} {req_r['Ora Start']}` ➡️ **Solicitat nou:** `{format_ro_date(req_r['Noua Dată'])} {req_r['Noua Ora']}` | Serviciu nou: *{req_r['Noul Serviciu']}*")
                    
                    req_dur = int(float(req_r["Durată"])) if pd.notna(req_r["Durată"]) else 30
                    has_ov_req, _ = check_overlap(req_r["Stilist"], req_r["Noua Dată"], req_r["Noua Ora"], req_dur, exclude_nr=req_r["Nr. Programare"])
                    if has_ov_req:
                        st.markdown("""
                        <div class="overlap-alert">
                            ⚠️ <b>ATENȚIE SUPRAPUNERE:</b> Noul interval orar solicitat se suprapune cu o altă programare existentă pentru acest stilist!
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button(f"🔍 Deschide Pop-up Aprobare (Client: {req_r['Client']})", key=f"open_pop_{req_r['Nr. Programare']}"):
                        approval_popup(req_r)
            st.markdown("---")

        if not df_all_mgmt.empty:
            col_mg1, col_mg2 = st.columns(2)
            with col_mg1:
                filter_mg_date = st.date_input("📅 Selectează Data pentru Gestionare", value=date.today(), key="mgmt_date_picker")
            
            date_str_mg = filter_mg_date.strftime("%Y-%m-%d")
            filtered_mgmt_progs = df_all_mgmt[df_all_mgmt["Dată"] == date_str_mg]
            
            with col_mg2:
                stilist_filter_mg = st.selectbox("💈 Filtrează după Stilist", stilisti_disponibili, index=stilisti_disponibili.index(current_user) if current_user in stilisti_disponibili else 0, key="mgmt_stilist_filter")
            
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
                        q_data = st.date_input("Dată", value=datetime.strptime(curr_mgmt_row["Dată"], "%Y-%m-%d").date(), min_value=date.today())
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
                                st.toast("Atenție: Programarea modificată se suprapune cu alta existentă!", icon="⚠️")
                            
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
                            st.toast("Programarea a fost actualizată cu succes!", icon="✅")
                            trigger_rerun()

                col_btn_m1, col_btn_m2, col_btn_m3 = st.columns(3)
                with col_btn_m1:
                    if st.button("Marchează ca Efectuat"):
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Status"] = "Efectuat"
                        save_all()
                        st.toast("Programare marcată ca efectuat!", icon="✅")
                        trigger_rerun()
                with col_btn_m2:
                    if st.button("Marchează ca Anulat"):
                        st.session_state.prog_df.loc[st.session_state.prog_df["Nr. Programare"] == sel_mg_nr, "Status"] = "Anulat"
                        save_all()
                        st.toast("Programare anulată.", icon="⚠️")
                        trigger_rerun()
                with col_btn_m3:
                    if st.button("Șterge Definitiv", type="primary"):
                        st.session_state.prog_df = st.session_state.prog_df[st.session_state.prog_df["Nr. Programare"] != sel_mg_nr]
                        save_all()
                        st.toast("Programare ștersă definitiv.", icon="🗑️")
                        trigger_rerun()
            else:
                st.info("Nu există programări înregistrate pentru data selectată cu filtrele curente.")
        else:
            st.info("Nu există programări în sistem.")

# ==========================================
# TAB 4: SERVICII & PREȚURI (Admin & Stilist)
# ==========================================
if is_admin_or_stylist:
    with tabs[3]:
        st.markdown("### 💇‍♂️ Gestiune & Catalog Servicii în funcție de Stilist")
        df_serv = st.session_state.serv_df.copy()
        
        # MULTISELECT STILIZAT AURIU
        sel_serv_filter = st.multiselect("Alege Stilist pentru Catalog", options=stilisti_disponibili, default=[current_user] if current_user in stilisti_disponibili else stilisti_disponibili, key="serv_stilist_multiselect")
        
        if sel_serv_filter:
            df_serv_filtered = df_serv[df_serv["Stilist"].isin(sel_serv_filter)]
        else:
            df_serv_filtered = df_serv

        st.markdown(render_lux_table(df_serv_filtered), unsafe_allow_html=True)

        st.markdown("---")
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.markdown("#### ➕ Adaugă Serviciu Nou")
            with st.form("add_serv"):
                ns_nume = st.text_input("Nume Serviciu")
                ns_stilist = st.selectbox("Asignat Stilist", stilisti_disponibili, index=default_stylist_idx)
                ns_pret = st.number_input("Preț (RON)", min_value=0, value=50)
                ns_durata = st.number_input("Durată (minute)", min_value=5, value=30)
                if st.form_submit_button("Adaugă"):
                    if ns_nume:
                        new_s = pd.DataFrame([{"Serviciu": ns_nume, "Preț": ns_pret, "Durată (min)": ns_durata, "Stilist": ns_stilist}])
                        st.session_state.serv_df = pd.concat([st.session_state.serv_df, new_s], ignore_index=True)
                        save_all()
                        st.toast("Serviciul a fost adăugat cu succes!", icon="✅")
                        trigger_rerun()
                        
        with col_s2:
            st.markdown("#### ✏️ Editează Serviciu")
            edit_target = st.selectbox("Alege serviciul de modificat", df_serv["Serviciu"].tolist() if not df_serv.empty else [])
            if edit_target:
                s_curr = df_serv[df_serv["Serviciu"] == edit_target].iloc[0]
                with st.form("edit_serv_form"):
                    e_nume = st.text_input("Nume nou", value=s_curr["Serviciu"])
                    e_stilist = st.selectbox("Stilist", stilisti_disponibili, index=stilisti_disponibili.index(s_curr["Stilist"]) if s_curr["Stilist"] in stilisti_disponibili else default_stylist_idx)
                    e_pret = st.number_input("Preț nou (RON)", min_value=0, value=int(float(s_curr["Preț"]) if pd.notna(s_curr["Preț"]) else 50))
                    e_durata = st.number_input("Durată nouă (min)", min_value=5, value=int(float(s_curr["Durată (min)"]) if pd.notna(s_curr["Durată (min)"]) else 30))
                    if st.form_submit_button("Salvează Modificări"):
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Serviciu"] = e_nume
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Stilist"] = e_stilist
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Preț"] = e_pret
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, "Durată (min)"] = e_durata
                        save_all()
                        st.toast("Serviciul a fost actualizat cu succes!", icon="✅")
                        trigger_rerun()
                        
        with col_s3:
            st.markdown("#### 🗑️ Șterge Serviciu")
            with st.form("del_serv_form"):
                del_serv = st.selectbox("Alege serviciul de șters", df_serv["Serviciu"].tolist() if not df_serv.empty else [])
                if st.form_submit_button("Șterge Serviciul"):
                    st.session_state.serv_df = st.session_state.serv_df[st.session_state.serv_df["Serviciu"] != del_serv]
                    save_all()
                    st.toast("Serviciul a fost șters.", icon="🗑️")
                    trigger_rerun()

# ==========================================
# TAB 5: RECENZII PENTRU STILIST
# ==========================================
if is_admin_or_stylist:
    with tabs[4]:
        st.markdown("### ⭐ Moderare Recenzii & Istoric Complet")
        rev_df = st.session_state.rev_df.copy()
        
        # MULTISELECT STILIZAT AURIU
        sel_rev_stilist = st.multiselect("Alege Stilist pentru Recenzii", options=stilisti_disponibili, default=[current_user] if current_user in stilisti_disponibili else stilisti_disponibili, key="rev_stilist_multiselect")
        
        if sel_rev_stilist:
            rev_df_filtered = rev_df[rev_df["Stilist"].isin(sel_rev_stilist)]
        else:
            rev_df_filtered = rev_df

        st.markdown("#### 🔔 Recenzii în Așteptare pentru Moderare")
        pending_revs = rev_df_filtered[rev_df_filtered["Status"] == "În așteptare"] if not rev_df_filtered.empty else pd.DataFrame()
        
        if not pending_revs.empty:
            rev_options = {}
            for _, r in pending_revs.iterrows():
                label = f"Client: {r['Client']} | Stilist: {r['Stilist']} | Rating: {r['Rating']}⭐ | Comentariu: {str(r['Comentariu'])[:35]}..."
                rev_options[label] = int(r['ID']) if pd.notna(r['ID']) else 0

            sel_rev_label = st.selectbox("Selectează Recenzia din Așteptare", list(rev_options.keys()))
            sel_rev_id = rev_options[sel_rev_label]
            
            rev_display = rev_df[rev_df["ID"] == sel_rev_id].drop(columns=["ID"], errors="ignore")
            st.markdown(render_lux_table(rev_display), unsafe_allow_html=True)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.button("✅ Aprobă Publicarea Recenziei"):
                    st.session_state.rev_df.loc[st.session_state.rev_df["ID"] == sel_rev_id, "Status"] = "Aprobat"
                    save_all()
                    st.toast("Recenzia a fost aprobată!", icon="✅")
                    trigger_rerun()
            with col_m2:
                if st.button("🗑️ Șterge Recenzia", type="primary"):
                    st.session_state.rev_df = st.session_state.rev_df[st.session_state.rev_df["ID"] != sel_rev_id]
                    save_all()
                    st.toast("Recenzia a fost ștersă.", icon="🗑️")
                    trigger_rerun()
        else:
            st.info("Nu există nicio recenzie în așteptarea moderării pentru selecția curentă.")

        st.markdown("---")
        st.markdown("#### 📜 Istoric Recenzii Aprobate")
        aprobate_filtered = rev_df_filtered[rev_df_filtered["Status"] == "Aprobat"] if not rev_df_filtered.empty else pd.DataFrame()

        if not aprobate_filtered.empty:
            st.markdown(render_lux_table(aprobate_filtered.drop(columns=["ID"], errors="ignore")), unsafe_allow_html=True)
        else:
            st.info("Nu există recenzii aprobate în istoric pentru selecția curentă.")

# ==========================================
# RAPORT FINANCIAR PENTRU STILIST SAU ADMIN
# ==========================================
if is_stylist:
    with tabs[5]:
        st.markdown(f"### 📊 Raport Financiar Personal — {current_user}")
        df_f = st.session_state.prog_df.copy()

        if not df_f.empty and "Preț" in df_f.columns:
            df_f = df_f[df_f["Stilist"] == current_user]
            
            df_f["Dată_dt"] = pd.to_datetime(df_f["Dată"], errors="coerce")
            df_f["Lună"] = df_f["Dată_dt"].dt.strftime("%Y-%m")

            luni_disponibile = ["Toate"] + sorted(df_f["Lună"].dropna().unique().tolist())
            sel_luna = st.selectbox("Filtrează Lunar", luni_disponibile, key="stilist_fin_luna")

            if sel_luna != "Toate":
                df_f = df_f[df_f["Lună"] == sel_luna]

            total_incasari_efectuate = df_f[df_f["Status"] == "Efectuat"]["Preț"].sum()
            total_programari = len(df_f)

            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Încasările Tale Reale</div><div class="metric-val">{total_incasari_efectuate} RON</div></div>', unsafe_allow_html=True)
            with c_f2:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Programări Asignate</div><div class="metric-val">{total_programari}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if not df_f.empty:
                df_f["Dată_Ro"] = df_f["Dată"].apply(format_ro_date)
                fig = px.bar(
                    df_f, x="Dată_Ro", y="Preț", color="Status",
                    title=f"Încasările Tale pe Dată ({current_user})",
                    template="plotly_dark",
                    color_discrete_sequence=["#e5c158", "#38bdf8", "#34d399", "#f43f5e"]
                )
                max_p = df_f["Preț"].max() if not df_f.empty else 100
                fig.update_layout(yaxis=dict(range=[0, max_p * 1.25]))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există date financiare înregistrate.")

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
                stilisti_raport = ["Toți"] + stilisti_disponibili
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
                df_f["Dată_Ro"] = df_f["Dată"].apply(format_ro_date)
                fig = px.bar(
                    df_f, x="Dată_Ro", y="Preț", color="Stilist", barmode="group",
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
        st.markdown(render_lux_table(st.session_state.users_df[["Utilizator", "Rol", "Telefon", "APIKey"]]), unsafe_allow_html=True)

        users_list = st.session_state.users_df["Utilizator"].tolist()
        sel_user_mgmt = st.selectbox("Selectează Utilizator pentru Setarea cheii API WhatsApp sau Adaugă", ["-- Adaugă Utilizator Nou --"] + users_list)

        if sel_user_mgmt == "-- Adaugă Utilizator Nou --":
            with st.form("add_new_user_form"):
                n_user = st.text_input("Nume Utilizator Nou")
                n_pass = st.text_input("Parolă", type="password")
                n_rol = st.selectbox("Rol", ["Administrator", "Stilist", "Client"])
                n_tel = st.text_input("Telefon contact", value="+40 ", placeholder="+40 7xxxxxxxx sau +357...")
                n_apikey = st.text_input("API Key WhatsApp (CallMeBot)", placeholder="opțional pentru stilisti")
                
                if st.form_submit_button("Adaugă Utilizator"):
                    if n_user and n_pass:
                        if n_user in st.session_state.users_df["Utilizator"].values:
                            st.toast("Utilizatorul există deja!", icon="❌")
                        else:
                            formatted_new_tel = format_phone_input(n_tel)
                            new_u = pd.DataFrame([{"Utilizator": n_user, "Parolă": n_pass, "Rol": n_rol, "Telefon": formatted_new_tel, "APIKey": n_apikey}])
                            st.session_state.users_df = pd.concat([st.session_state.users_df, new_u], ignore_index=True)
                            save_all()
                            st.toast(f"Utilizatorul {n_user} a fost adăugat cu succes!", icon="✅")
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
                    st.toast("Utilizatorul a fost actualizat cu succes!", icon="✅")
                    trigger_rerun()
                if del_mod:
                    if sel_user_mgmt in ["Alex", "Denis", "Adrian", "Andreea"]:
                        st.toast("Nu poți șterge membrii principali ai echipei!", icon="❌")
                    else:
                        st.session_state.users_df = st.session_state.users_df[st.session_state.users_df["Utilizator"] != sel_user_mgmt]
                        save_all()
                        st.toast(f"Utilizatorul {sel_user_mgmt} a fost șters!", icon="🗑️")
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
            r_stilist = st.selectbox("Stilistul vizitat", stilisti_disponibili, index=default_stylist_idx)
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
                    st.toast("Recenzia a fost trimisă cu succes spre moderare!", icon="✅")
                    trigger_rerun()
