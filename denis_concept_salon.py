import os
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st

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
    .success-alert { background-color: rgba(6, 78, 59, 0.85); color: #6ee7b7; padding: 14px; border-radius: 10px; border: 1px solid #10b981; font-weight: 600; margin-bottom: 12px;}
    
    /* Stil Banner Rulant Recenzii */
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
        animation: marquee 35s linear infinite;
        color: #f3f4f6;
        font-size: 14px;
        font-weight: 500;
    }
    .marquee-content span {
        margin-right: 60px;
        color: #e5c158;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
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

def init_csvs():
    today_str = date.today().strftime("%Y-%m-%d")
    future_str = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    if not os.path.exists(PROG_FILE):
        df_p = pd.DataFrame([
            {"ID": 1, "Dată": today_str, "Ora Start": "10:00", "Ora Sfârșit": "10:45", "Client": "Alex", "Telefon": "0722000000", "Serviciu": "Tuns + Barbă Fade", "Stilist": "Adrian", "Preț": 90, "Durată": 45, "Status": "Confirmat", "Observații": "Test programare Alex"},
            {"ID": 2, "Dată": future_str, "Ora Start": "11:30", "Ora Sfârșit": "12:30", "Client": "Ionuț", "Telefon": "0733111222", "Serviciu": "Tuns Lung & Coafat", "Stilist": "Andreea", "Preț": 120, "Durată": 60, "Status": "Confirmat", "Observații": "Test programare Ionuț"}
        ])
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
            {"Utilizator": "Alex", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0722000000"},
            {"Utilizator": "Denis", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0733000000"},
            {"Utilizator": "Adrian", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0744111222"},
            {"Utilizator": "Andreea", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0755222333"},
            {"Utilizator": "Ionuț", "Parolă": "client123", "Rol": "Client", "Telefon": "0733111222"},
        ])
        df_u.to_csv(USER_FILE, index=False)

    if not os.path.exists(REV_FILE):
        df_r = pd.DataFrame([
            {"ID": 1, "Client": "Alex", "Stilist": "Adrian", "Rating": 5, "Comentariu": "Serviciu impecabil și profesionalism!", "Status": "Aprobat"},
            {"ID": 2, "Client": "Ionuț", "Stilist": "Andreea", "Rating": 5, "Comentariu": "Atmosferă excelentă și atenție la detalii.", "Status": "Aprobat"}
        ])
        df_r.to_csv(REV_FILE, index=False)

init_csvs()

def load_data():
    st.session_state.prog_df = pd.read_csv(PROG_FILE)
    st.session_state.serv_df = pd.read_csv(SERV_FILE)
    st.session_state.users_df = pd.read_csv(USER_FILE)
    st.session_state.rev_df = pd.read_csv(REV_FILE)

if "prog_df" not in st.session_state:
    load_data()

def save_all():
    st.session_state.prog_df.to_csv(PROG_FILE, index=False)
    st.session_state.serv_df.to_csv(SERV_FILE, index=False)
    st.session_state.users_df.to_csv(USER_FILE, index=False)
    st.session_state.rev_df.to_csv(REV_FILE, index=False)

def render_marquee_banner():
    rev_aprobate_banner = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
    if not rev_aprobate_banner.empty:
        marquee_items = ""
        for _, r_row in rev_aprobate_banner.iterrows():
            stars = "⭐" * int(r_row['Rating'])
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
    # Afișare banner recenzii și pe pagina de login
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
current_user = st.session_state.user

# ==========================================
# BANNER RULANT (MARQUEE) CU RECENZII (În aplicație)
# ==========================================
render_marquee_banner()

# ==========================================
# SIDEBAR / MENIU LATERAL
# ==========================================
st.sidebar.markdown(f"### ✂️ **{current_user}**")
st.sidebar.markdown(f"Rol: <span class='role-tag'>{st.session_state.role}</span>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Deconectare", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    trigger_rerun()

st.sidebar.markdown("---")

# ==========================================
# LOGICA DE SUPRAPUNERE DATĂ + ORA
# ==========================================
def check_overlap(stilist, data_str, ora_start_str, durata_min, exclude_id=None):
    try:
        t_start = datetime.strptime(ora_start_str, "%H:%M").time()
        start_dt = datetime.combine(datetime.strptime(data_str, "%Y-%m-%d"), t_start)
        end_dt = start_dt + timedelta(minutes=int(durata_min))
    except:
        return False, []

    df = st.session_state.prog_df
    conflicts = []
    
    for idx, row in df.iterrows():
        if exclude_id is not None and str(row.get("ID")) == str(exclude_id):
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
# TAB-URI PRINCIPALE (Diferențiate Client / Admin)
# ==========================================
if is_admin:
    tabs = st.tabs(["📅 Programări & Calendar", "➕ Adaugă Programare", "💇‍♂️ Servicii & Prețuri", "⭐ Recenzii", "📊 Raport Financiar", "⚙️ Setări & Utilizatori"])
else:
    tabs = st.tabs(["📅 Programările Mele & Disponibilitate", "➕ Programare Nouă", "⭐ Recenzii Salon"])

# ==========================================
# TAB 1: PROGRAMĂRI & CALENDAR / DISPONIBILITATE
# ==========================================
with tabs[0]:
    if is_admin:
        st.markdown("### 📅 Vizualizator Programări & Calendar")
        df_p = st.session_state.prog_df.copy()
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            view_mode = st.selectbox("Vizualizare Perioadă", ["Toate", "Săptămâna aceasta", "Săptămâna viitoare", "Luna aceasta", "Programări Viitoare", "Programări Trecute"])
        with col_f2:
            stilisti_opt = ["Toți"] + ["Adrian", "Andreea", "Alex", "Denis"]
            fil_stilist = st.selectbox("Filtru Stilist / Barber", stilisti_opt)
        with col_f3:
            fil_status = st.selectbox("Filtru Status", ["Toate", "Confirmat", "Efectuat", "Anulat"])

        today = date.today()
        if not df_p.empty:
            df_p["Dată_dt"] = pd.to_datetime(df_p["Dată"], errors="coerce")
            
            if view_mode == "Săptămâna aceasta":
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
            def highlight_overlaps(row):
                has_ov, _ = check_overlap(row["Stilist"], row["Dată"], row["Ora Start"], row.get("Durată", 30), exclude_id=row.get("ID"))
                if has_ov or row["Status"] == "Anulat":
                    return ['background-color: rgba(127, 29, 29, 0.4); color: #fca5a5'] * len(row)
                return [''] * len(row)

            st.dataframe(df_p.style.apply(highlight_overlaps, axis=1), use_container_width=True)
            
            st.markdown("#### ⚙️ Gestionare Programare Existentă")
            sel_id = st.selectbox("Selectează ID Programare", df_p["ID"].tolist() if "ID" in df_p.columns else [])
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("Marchează Efectuat"):
                    st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == sel_id, "Status"] = "Efectuat"
                    save_all()
                    st.success("Programare marcată ca efectuat și adăugată la totalul încasărilor!")
                    trigger_rerun()
            with col_act2:
                if st.button("Anulează Programarea"):
                    st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == sel_id, "Status"] = "Anulat"
                    save_all()
                    st.warning("Programare anulată de administrator.")
                    trigger_rerun()
            with col_act3:
                if st.button("Șterge Definitiv", type="primary"):
                    st.session_state.prog_df = st.session_state.prog_df[st.session_state.prog_df["ID"] != sel_id]
                    save_all()
                    st.error("Programare ștersă.")
                    trigger_rerun()
        else:
            st.info("Nu există programări care să corespundă filtrelor selectate.")

    else:
        st.markdown(f"### 📅 Programările Mele & Disponibilitatea Stilistilor")
        client_name = current_user
        df_p_all = st.session_state.prog_df.copy()
        client_progs = df_p_all[df_p_all["Client"].str.contains(client_name, case=False, na=False)] if not df_p_all.empty else pd.DataFrame()
        
        st.markdown(f"#### Bun venit, {current_user}! Istoricul programărilor tale:")
        if not client_progs.empty:
            st.dataframe(client_progs[["ID", "Dată", "Ora Start", "Ora Sfârșit", "Serviciu", "Stilist", "Preț", "Durată", "Status"]], use_container_width=True)
            
            st.markdown("---")
            st.markdown("##### ❌ Anulare Programare (Regulă: cu cel puțin 24h înainte)")
            viitoare = client_progs[(client_progs["Dată"] >= str(date.today())) & (client_progs["Status"] == "Confirmat")]
            if not viitoare.empty:
                id_anulat = st.selectbox("Alege programarea de anulat", viitoare["ID"].tolist())
                if st.button("Confirmă Anularea"):
                    prog_row = client_progs[client_progs["ID"] == id_anulat].iloc[0]
                    p_dt = datetime.strptime(f"{prog_row['Dată']} {prog_row['Ora Start']}", "%Y-%m-%d %H:%M")
                    ore_ramase = (p_dt - datetime.now()).total_seconds() / 3600
                    
                    if ore_ramase < 24:
                        st.error(f"❌ Anularea nu este permisă! Mai sunt doar {ore_ramase:.1f} ore până la programare (limita minimă este de 24 de ore).")
                    else:
                        stilist_alocat = prog_row["Stilist"]
                        st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == id_anulat, "Status"] = "Anulat"
                        save_all()
                        st.success("Programarea a fost anulată cu succes!")
                        st.info(f"🔔 Notificare trimisă stilistului **{stilist_alocat}**: Clientul {current_user} a anulat programarea ID {id_anulat}.")
                        trigger_rerun()
            else:
                st.info("Nu ai programări viitoare active pe care să le poți anula.")
        else:
            st.info("Nu ai nicio programare înregistrată momentan.")

        st.markdown("---")
        st.markdown("#### 🕒 Verifică Disponibilitatea Stilistilor (Săptămâna Cursă, Viitoare & Până Luna Viitoare)")
        
        sel_stilist_disp = st.selectbox("Alege stilistul pentru a vedea disponibilitatea", ["Adrian", "Andreea", "Alex", "Denis"], key="disp_stilist")
        
        today = date.today()
        st.markdown(f"Vizualizare programări și intervale ocupate pentru **{sel_stilist_disp}** de la data de **{today.strftime('%Y-%m-%d')}** înainte:")
        
        if not df_p_all.empty:
            df_stilist_prog = df_p_all[(df_p_all["Stilist"] == sel_stilist_disp) & (df_p_all["Status"] != "Anulat") & (df_p_all["Dată"] >= str(today))]
            if not df_stilist_prog.empty:
                st.dataframe(df_stilist_prog[["Dată", "Ora Start", "Ora Sfârșit", "Serviciu"]], use_container_width=True)
            else:
                st.success(f"✨ Stilistul **{sel_stilist_disp}** nu are programări înregistrate în perioada următoare. Multe sloturi disponibile!")

# ==========================================
# TAB 2: ADAUGĂ PROGRAMARE
# ==========================================
with tabs[1]:
    st.markdown("### ➕ Programare Nouă")
    
    if "msg_status" in st.session_state:
        if st.session_state["msg_status"]["type"] == "error":
            st.markdown(f'<div class="overlap-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
        del st.session_state["msg_status"]

    existent_clients = st.session_state.prog_df[["Client", "Telefon"]].drop_duplicates().to_dict(orient="records") if not st.session_state.prog_df.empty else []

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        client_nume = st.text_input("👤 Nume Client", value=current_user if not is_admin else "", key="input_client_nuum")
        
        matched_c = [c for c in existent_clients if c["Client"].lower() == client_nume.lower()]
        default_tel = str(matched_c[0].get("Telefon", "")) if matched_c else ""
        client_tel = st.text_input("📞 Telefon Client", value=default_tel, placeholder="07xxxxxxxx", key="input_client_tel")

        p_data = st.date_input("📅 Dată Programare", value=date.today())
        p_stilist = st.selectbox("💈 Stilist / Barber", ["Adrian", "Andreea", "Alex", "Denis"], key="prog_stilist")

    with col_in2:
        df_serv_all = st.session_state.serv_df
        serv_filtered = df_serv_all[df_serv_all["Stilist"] == p_stilist]
        if serv_filtered.empty:
            serv_filtered = df_serv_all
            
        serv_opt = serv_filtered["Serviciu"].tolist()
        
        p_serviciu = st.selectbox("✂️ Alege Serviciul Dorit din Listă", serv_opt)
        
        s_row = df_serv_all[df_serv_all["Serviciu"] == p_serviciu]
        p_pret = int(s_row["Preț"].values[0]) if not s_row.empty else 50
        p_durata = int(s_row["Durată (min)"].values[0]) if not s_row.empty else 30
        
        st.markdown(f"""
        <div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.3); margin-top: 10px;">
            ⏱️ Durată estimată: <b>{p_durata} minute</b><br>
            💰 <b>Total de Plată: {p_pret} RON</b>
        </div>
        """, unsafe_allow_html=True)

        slot_options = [
            "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
            "18:00", "18:30", "19:00", "19:30"
        ]
        p_ora = st.selectbox("⏰ Alege Slot Orar", slot_options)
        p_obs = st.text_area("📝 Observații / Preferințe")

    try:
        t_start_obj = datetime.strptime(p_ora, "%H:%M")
        t_end_obj = t_start_obj + timedelta(minutes=p_durata)
        ora_sfarsit = t_end_obj.strftime("%H:%M")
    except:
        ora_sfarsit = "10:30"

    st.markdown("<br>", unsafe_allow_html=True)

    data_str = p_data.strftime("%Y-%m-%d")
    has_ov, conflicts = check_overlap(p_stilist, data_str, p_ora, p_durata)
    if has_ov:
        st.markdown(f'<div class="overlap-alert">⚠️ ATENȚIE SUPRAPUNERE: Stilistul {p_stilist} are deja o programare în această dată ({data_str}) la ora {p_ora} - {ora_sfarsit}!</div>', unsafe_allow_html=True)

    def action_save():
        if not client_nume:
            st.session_state["msg_status"] = {"type": "error", "text": "Te rog introdu numele clientului!"}
            return
        
        if not is_admin and has_ov:
            st.session_state["msg_status"] = {"type": "error", "text": "❌ Slotul orar selectat se suprapune cu o altă programare existentă! Clienții nu pot face programări suprapuse (doar administratorul poate face acest lucru)."}
            return
        
        new_id = int(st.session_state.prog_df["ID"].max() + 1) if not st.session_state.prog_df.empty and "ID" in st.session_state.prog_df.columns else 1
        
        new_row = pd.DataFrame([{
            "ID": new_id,
            "Dată": data_str,
            "Ora Start": p_ora,
            "Ora Sfârșit": ora_sfarsit,
            "Client": client_nume,
            "Telefon": client_tel if client_tel else "Nespecificat",
            "Serviciu": p_serviciu,
            "Stilist": p_stilist,
            "Preț": p_pret,
            "Durată": p_durata,
            "Status": "Confirmat",
            "Observații": p_obs
        }])

        st.session_state.prog_df = pd.concat([st.session_state.prog_df, new_row], ignore_index=True)
        save_all()
        
        msg = f"✅ Programarea a fost salvată cu succes! Total de plată: **{p_pret} RON**. Stilistul **{p_stilist}** a fost notificat."
        st.session_state["msg_status"] = {"type": "success", "text": msg}
        trigger_rerun()

    st.button("💾 Salvează Programarea", type="primary", use_container_width=True, on_click=action_save)

# ==========================================
# TAB 3: SERVICII & PREȚURI (Doar Admin) sau RECENZII (Client)
# ==========================================
if is_admin:
    with tabs[2]:
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
                    e_pret = st.number_input("Preț nou (RON)", min_value=0, value=int(s_curr["Preț"]))
                    e_durata = st.number_input("Durată nouă (min)", min_value=5, value=int(s_curr["Durată (min)"]))
                    if st.form_submit_button("Salvează Modificări"):
                        st.session_state.serv_df.loc[st.session_state.serv_df["Serviciu"] == edit_target, ["Serviciu", "Stilist", "Preț", "Durată (min)"]] = [e_nume, e_stilist, e_pret, e_durata]
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

    with tabs[3]:
        st.markdown("### ⭐ Moderare Recenzii (Acord Admin)")
        rev_df = st.session_state.rev_df.copy()
        if not rev_df.empty:
            st.dataframe(rev_df, use_container_width=True)
            sel_rev_id = st.selectbox("Selectează ID Recenzie", rev_df["ID"].tolist())
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
            st.info("Nu există recenzii înregistrate.")

    with tabs[4]:
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

    with tabs[5]:
        st.markdown("### ⚙️ Panou Setări & Gestiune Utilizatori")
        st.dataframe(st.session_state.users_df, use_container_width=True)

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("##### Creează / Modifică Utilizator")
            with st.form("add_user_form"):
                n_user = st.text_input("Nume Utilizator")
                n_pass = st.text_input("Parolă", type="password")
                n_rol = st.selectbox("Rol", ["Administrator", "Client"])
                n_tel = st.text_input("Telefon contact")
                
                if st.form_submit_button("Salvează Utilizator"):
                    if n_user and n_pass:
                        users = st.session_state.users_df
                        if n_user in users["Utilizator"].values:
                            st.session_state.users_df.loc[st.session_state.users_df["Utilizator"] == n_user, ["Parolă", "Rol", "Telefon"]] = [n_pass, n_rol, n_tel]
                        else:
                            new_u = pd.DataFrame([{"Utilizator": n_user, "Parolă": n_pass, "Rol": n_rol, "Telefon": n_tel}])
                            st.session_state.users_df = pd.concat([st.session_state.users_df, new_u], ignore_index=True)
                        save_all()
                        st.success(f"Utilizatorul {n_user} a fost salvat!")
                        trigger_rerun()
        
        with col_u2:
            st.markdown("##### Șterge Utilizator")
            del_user_target = st.selectbox("Alege utilizatorul de șters", st.session_state.users_df["Utilizator"].tolist())
            if st.button("Șterge Utilizatorul", type="primary"):
                if del_user_target in ["Alex", "Denis", "Adrian", "Andreea"]:
                    st.error("Nu poți șterge membrii principali ai echipei!")
                else:
                    st.session_state.users_df = st.session_state.users_df[st.session_state.users_df["Utilizator"] != del_user_target]
                    save_all()
                    st.success("Utilizator șters cu succes.")
                    trigger_rerun()

else:
    with tabs[2]:
        st.markdown("### ⭐ Recenzii Salon (Toți Stiliștii)")
        
        st.markdown("#### 💬 Ce spun clienții noștri")
        aprobate = st.session_state.rev_df[st.session_state.rev_df["Status"] == "Aprobat"] if not st.session_state.rev_df.empty else pd.DataFrame()
        
        if not aprobate.empty:
            for idx, row in aprobate.iterrows():
                with st.container(border=True):
                    st.markdown(f"**👤 {row['Client']}** | Stilist: *{row['Stilist']}* | Rating: {'⭐' * int(row['Rating'])}")
                    st.markdown(f"> *{row['Comentariu']}*")
        else:
            st.info("Nu există recenzii aprobate momentan.")

        st.markdown("---")
        st.markdown("#### ✍️ Adaugă o Recenzie Nouă (Necesită acordul administratorului pentru a fi publicată)")
        with st.form("add_review_form"):
            r_stilist = st.selectbox("Stilistul vizitat", ["Adrian", "Andreea", "Alex", "Denis"])
            r_rating = st.slider("Rating (Stele)", 1, 5, 5)
            r_comentariu = st.text_area("Scrie experiența ta...")
            if st.form_submit_button("Trimite Recenzia spre Aprobare"):
                if r_comentariu:
                    new_rev_id = int(st.session_state.rev_df["ID"].max() + 1) if not st.session_state.rev_df.empty and "ID" in st.session_state.rev_df.columns else 1
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
                    st.success("Recenzia ta a fost trimisă! Va fi afișată în bannerul public imediat ce administratorul o va aproba.")
                    trigger_rerun()
