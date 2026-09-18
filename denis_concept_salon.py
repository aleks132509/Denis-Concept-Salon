import io
import os
from datetime import date, datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# CONFIGURARE PAGINĂ & THEME (DARK MODE)
# ==========================================
st.set_page_config(
    page_title="Denis Concept Salon - Management",
    layout="wide",
    page_icon="✂️",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117 !important;
        color: #f1f5f9 !important;
    }
    .metric-card {
        background-color: #1e222d;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        border: 1px solid #2e3545;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-value { font-size: 24px; font-weight: 700; color: #38bdf8; }
    .metric-label { font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
    .role-badge { background-color: #0284c7; color: white; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
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
# FIȘIERE PERSISTENTE
# ==========================================
PROG_FILE = "programari_denis_concept.csv"
SERV_FILE = "servicii_denis_concept.csv"

def get_initial_appointments():
    if os.path.exists(PROG_FILE):
        try:
            return pd.read_csv(PROG_FILE)
        except:
            pass
    return pd.DataFrame([
        {"Dată": "2026-09-20", "Ora": "10:00", "Client": "Andrei Popescu", "Telefon": "0722123456", "Serviciu": "Tuns Clasic", "Stilist": "Alex", "Preț": 60, "Status": "Confirmat", "Observații": "Fără barbă"},
        {"Dată": "2026-09-20", "Ora": "11:00", "Client": "Mihai Ionescu", "Telefon": "0733987654", "Serviciu": "Tuns + Barbă", "Stilist": "Bogdan", "Preț": 90, "Status": "Confirmat", "Observații": "Degradat fin"},
    ])

def get_initial_services():
    if os.path.exists(SERV_FILE):
        try:
            return pd.read_csv(SERV_FILE)
        except:
            pass
    return pd.DataFrame([
        {"Serviciu": "Tuns Clasic", "Preț": 60, "Durată (min)": 30},
        {"Serviciu": "Tuns + Barbă", "Preț": 90, "Durată (min)": 45},
        {"Serviciu": "Aranjat Barbă", "Preț": 40, "Durată (min)": 20},
        {"Serviciu": "Vopsit Păr / Barbă", "Preț": 70, "Durată (min)": 30},
    ])

def save_files():
    st.session_state.prog_df.to_csv(PROG_FILE, index=False)
    st.session_state.serv_df.to_csv(SERV_FILE, index=False)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "users" not in st.session_state:
    st.session_state.users = {
        "Denis": {"pass": "admin123", "role": "Administrator"},
        "Alex": {"pass": "stilist123", "role": "Stilist"},
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if "prog_df" not in st.session_state:
    st.session_state.prog_df = get_initial_appointments()
if "serv_df" not in st.session_state:
    st.session_state.serv_df = get_initial_services()

# ==========================================
# AUTENTIFICARE
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_b, _ = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>✂️ Denis Concept Salon</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Sistem Gestiune & Programări</p>", unsafe_allow_html=True)
        with st.container(border=True):
            username = st.text_input("👤 Utilizator")
            password = st.text_input("🔑 Parolă", type="password")
            if st.button("🔓 Autentificare", type="primary", use_container_width=True):
                user_data = st.session_state.users.get(username)
                if user_data and user_data["pass"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    trigger_rerun()
                else:
                    st.error("Utilizator sau parolă incorectă!")
    st.stop()

current_role = st.session_state.users[st.session_state.user]["role"]
is_admin = current_role == "Administrator"

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown(f"### ✂️ **{st.session_state.user}**")
st.sidebar.markdown(f"Rol: <span class='role-badge'>{current_role}</span>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Deconectare", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    trigger_rerun()
st.sidebar.markdown("---")

# ==========================================
# TAB-URI PRINCIPALE
# ==========================================
tabs = st.tabs(["📅 Programări & Calendar", "➕ Adaugă Programare", "💇‍♂️ Servicii & Prețuri", "📊 Raport Financiar", "⚙️ Setări"])

# 1. PROGRAMĂRI
with tabs[0]:
    st.markdown("### 📅 Centralizator Programări - Denis Concept Salon")
    
    df_p = st.session_state.prog_df.copy()
    if not df_p.empty:
        col_k1, col_k2, col_k3 = st.columns(3)
        total_azi = len(df_p[df_p["Dată"] == str(date.today())])
        total_incasari = df_p[df_p["Status"] == "Efectuat"]["Preț"].sum() if "Preț" in df_p.columns else 0
        
        with col_k1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">📅 Programări Totale</div><div class="metric-value">{len(df_p)}</div></div>', unsafe_allow_html=True)
        with col_k2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">📌 Programări Astăzi</div><div class="metric-value">{total_azi}</div></div>', unsafe_allow_html=True)
        with col_k3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">💰 Încasări (Efectuate)</div><div class="metric-value">{total_incasari} RON</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_p, use_container_width=True)
    else:
        st.info("Nu există programări înregistrate.")

# 2. ADAUGĂ PROGRAMARE (CU BUTON SUS ȘI JOS)
with tabs[1]:
    st.markdown("### ➕ Adaugă Programare Nouă")

    if "success_msg" in st.session_state:
        st.success(st.session_state["success_msg"])
        del st.session_state["success_msg"]

    def action_save_prog():
        p_dat = st.session_state.get("inp_data").strftime("%Y-%m-%d")
        p_ora = st.session_state.get("inp_ora")
        p_cli = st.session_state.get("inp_client")
        p_tel = st.session_state.get("inp_tel")
        p_ser = st.session_state.get("inp_serviciu")
        p_sti = st.session_state.get("inp_stilist")
        p_obs = st.session_state.get("inp_obs")
        
        match_serv = st.session_state.serv_df[st.session_state.serv_df["Serviciu"] == p_ser]
        pret = int(match_serv["Preț"].values[0]) if not match_serv.empty else 50

        new_row = pd.DataFrame([{
            "Dată": p_dat, "Ora": p_ora, "Client": p_cli, "Telefon": p_tel,
            "Serviciu": p_ser, "Stilist": p_sti, "Preț": pret, "Status": "Confirmat", "Observații": p_obs
        }])
        st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
        save_files()
        st.session_state["success_msg"] = "✅ Programarea a fost salvată cu succes!"
        trigger_rerun()

    # 💾 BUTON SUS
    st.button("💾 Salvează Programarea (Sus)", type="primary", use_container_width=True, on_click=action_save_prog, key="top_save_prog")
    st.markdown("---")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.date_input("📅 Dată Programare", value=date.today(), key="inp_data")
        st.text_input("⏰ Ora (ex: 14:30)", value="10:00", key="inp_ora")
        st.text_input("👤 Nume Client", key="inp_client")
        st.text_input("📞 Telefon Client", key="inp_tel")
    with col_f2:
        servicii_list = st.session_state.serv_df["Serviciu"].tolist() if not st.session_state.serv_df.empty else ["Tuns"]
        st.selectbox("✂️ Serviciu", servicii_list, key="inp_serviciu")
        
        stilisti_list = [u for u, data in st.session_state.users.items()]
        st.selectbox("💈 Stilist / Frizer", stilisti_list, key="inp_stilist")
        st.text_area("📝 Observații (ex: preferințe tuns)", key="inp_obs")

    st.markdown("---")
    # 💾 BUTON JOS
    st.button("💾 Salvează Programarea (Jos)", type="primary", use_container_width=True, on_click=action_save_prog, key="bot_save_prog")

# 3. SERVICII & PREȚURI
with tabs[2]:
    st.markdown("### 💇‍♂️ Gestiune Servicii & Prețuri")
    st.dataframe(st.session_state.serv_df, use_container_width=True)
    
    if is_admin:
        with st.form("add_serv_form"):
            st.markdown("##### Adaugă Serviciu Nou")
            s_nume = st.text_input("Nume Serviciu")
            s_pret = st.number_input("Preț (RON)", min_value=0, value=50)
            s_durata = st.number_input("Durată (minute)", min_value=5, value=30)
            if st.form_submit_button("Adaugă în Listă", type="primary"):
                if s_nume:
                    new_s = pd.DataFrame([{"Serviciu": s_nume, "Preț": s_pret, "Durată (min)": s_durata}])
                    st.session_state.serv_df = pd.concat([st.session_state.serv_df, new_s], ignore_index=True)
                    save_files()
                    st.success("Serviciu adăugat!")
                    trigger_rerun()

# 4. RAPORT FINANCIAR & GRAFICE
with tabs[3]:
    st.markdown("### 📊 Raport Financiar și Grafice")
    df_f = st.session_state.prog_df.copy()
    if not df_f.empty and "Preț" in df_f.columns:
        fig = px.bar(df_f, x="Dată", y="Preț", color="Stilist", title="Încasări zilnice per Stilist", template="plotly_dark")
        max_incasari = df_f["Preț"].max() if not df_f.empty else 100
        fig.update_layout(yaxis=dict(range=[0, max_incasari * 1.25]))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Date insuficiente pentru generarea graficelor.")

# 5. SETĂRI
with tabs[4]:
    st.markdown("### ⚙️ Setări Denis Concept Salon")
    st.write("Panou de configurare pentru utilizatori, orar și preferințe salon.")