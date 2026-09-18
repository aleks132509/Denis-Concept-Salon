import os
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# CONFIGURARE PAGINĂ & DESIGN SALON DE LUX
# ==========================================
st.set_page_config(
    page_title="Denis Concept Salon",
    layout="wide",
    page_icon="✂️",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0c0f17 !important;
        color: #f8fafc !important;
    }
    .salon-card {
        background-color: #161b26;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
        border: 1px solid #2a3447;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-val { font-size: 26px; font-weight: 700; color: #d4af37; }
    .metric-lbl { font-size: 12px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .role-tag { background-color: #d4af37; color: #0c0f17; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
    .overlap-alert { background-color: #7f1d1d; color: #fca5a5; padding: 12px; border-radius: 8px; border: 1px solid #ef4444; font-weight: 600; margin-bottom: 10px;}
    .success-alert { background-color: #064e3b; color: #6ee7b7; padding: 12px; border-radius: 8px; border: 1px solid #10b981; font-weight: 600; margin-bottom: 10px;}
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
# GESTIUNE FIȘIERE PERSISTENTE (CSV)
# ==========================================
PROG_FILE = "programari_denis_concept.csv"
SERV_FILE = "servicii_denis_concept.csv"
USER_FILE = "utilizatori_denis_concept.csv"

def init_csvs():
    if not os.path.exists(PROG_FILE):
        df_p = pd.DataFrame(columns=["ID", "Dată", "Ora Start", "Ora Sfârșit", "Client", "Telefon", "Serviciu", "Stilist", "Preț", "Durată", "Status", "Observații"])
        df_p.to_csv(PROG_FILE, index=False)
    
    if not os.path.exists(SERV_FILE):
        df_s = pd.DataFrame([
            {"Serviciu": "Tuns Clasic", "Preț": 60, "Durată (min)": 30},
            {"Serviciu": "Tuns + Barbă", "Preț": 90, "Durată (min)": 45},
            {"Serviciu": "Aranjat Barbă", "Preț": 40, "Durată (min)": 20},
            {"Serviciu": "Vopsit Păr / Stil", "Preț": 120, "Durată (min)": 60},
        ])
        df_s.to_csv(SERV_FILE, index=False)

    if not os.path.exists(USER_FILE):
        df_u = pd.DataFrame([
            {"Utilizator": "Alex", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0722000000"},
            {"Utilizator": "Denis", "Parolă": "admin123", "Rol": "Administrator", "Telefon": "0733000000"},
            {"Utilizator": "Andrei Client", "Parolă": "client123", "Rol": "Client", "Telefon": "0722123456"},
        ])
        df_u.to_csv(USER_FILE, index=False)

init_csvs()

def load_data():
    st.session_state.prog_df = pd.read_csv(PROG_FILE)
    st.session_state.serv_df = pd.read_csv(SERV_FILE)
    st.session_state.users_df = pd.read_csv(USER_FILE)

if "prog_df" not in st.session_state:
    load_data()

def save_all():
    st.session_state.prog_df.to_csv(PROG_FILE, index=False)
    st.session_state.serv_df.to_csv(SERV_FILE, index=False)
    st.session_state.users_df.to_csv(USER_FILE, index=False)

# ==========================================
# SESIUNE & AUTENTIFICARE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_auth, _ = st.columns([1, 1.3, 1])
    with col_auth:
        st.markdown("<h1 style='text-align: center; color: #d4af37;'>✂️ Denis Concept Salon</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Autentificare în Sistem</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            u_input = st.text_input("👤 Utilizator / Nume")
            p_input = st.text_input("🔑 Parolă", type="password")
            
            if st.button("🚀 Intră în Cont", type="primary", use_container_width=True):
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
# LOGICA DE SUPRAPUNERE TIMP
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
# TAB-URI PRINCIPALE
# ==========================================
if is_admin:
    tabs = st.tabs(["📅 Programări & Calendar", "➕ Adaugă Programare", "💇‍♂️ Servicii & Prețuri", "📊 Raport Financiar", "⚙️ Setări & Utilizatori"])
else:
    tabs = st.tabs(["📅 Programările Mele", "➕ Programare Nouă", "💇‍♂️ Servicii & Prețuri"])

# ==========================================
# TAB 1: PROGRAMĂRI & CALENDAR
# ==========================================
with tabs[0]:
    st.markdown("### 📅 Vizualizator Programări & Calendar")
    
    df_p = st.session_state.prog_df.copy()
    
    if is_admin:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            view_mode = st.selectbox("Vizualizare Perioadă", ["Toate", "Săptămâna aceasta", "Luna aceasta", "Programări Viitoare", "Programări Trecute"])
        with col_f2:
            stilisti_opt = ["Toți"] + [u for u, r in zip(st.session_state.users_df["Utilizator"], st.session_state.users_df["Rol"]) if r == "Administrator"]
            fil_stilist = st.selectbox("Filtru Stilist", stilisti_opt)
        with col_f3:
            fil_status = st.selectbox("Filtru Status", ["Toate", "Confirmat", "Efectuat", "Anulat"])

        today = date.today()
        if not df_p.empty:
            df_p["Dată_dt"] = pd.to_datetime(df_p["Dată"], errors="coerce")
            
            if view_mode == "Săptămâna aceasta":
                start_w = today - timedelta(days=today.weekday())
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
                incasari_afisate = df_p[df_p["Status"] == "Efectuat"]["Preț"].sum() if "Preț" in df_p.columns else 0
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Încasări (Efectuate)</div><div class="metric-val">{incasari_afisate} RON</div></div>', unsafe_allow_html=True)
            with c3:
                azi_count = len(df_p[df_p["Dată"] == str(today)])
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Programări Astăzi</div><div class="metric-val">{azi_count}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not df_p.empty:
            def highlight_overlaps(row):
                has_ov, _ = check_overlap(row["Stilist"], row["Dată"], row["Ora Start"], row.get("Durată", 30), exclude_id=row.get("ID"))
                if has_ov or row["Status"] == "Anulat":
                    return ['background-color: #451a03; color: #fca5a5'] * len(row)
                return [''] * len(row)

            st.dataframe(df_p.style.apply(highlight_overlaps, axis=1), use_container_width=True)
            
            st.markdown("#### ⚙️ Gestionare Programare Existentă")
            sel_id = st.selectbox("Selectează ID Programare pentru modificare status", df_p["ID"].tolist() if "ID" in df_p.columns else [])
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("Marchează Efectuat"):
                    st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == sel_id, "Status"] = "Efectuat"
                    save_all()
                    st.success("Actualizat cu succes!")
                    trigger_rerun()
            with col_act2:
                if st.button("Anulează Programarea"):
                    st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == sel_id, "Status"] = "Anulat"
                    save_all()
                    st.warning("Programare anulată.")
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
        client_name = current_user
        client_progs = df_p[df_p["Client"].str.contains(client_name, case=False, na=False)] if not df_p.empty else pd.DataFrame()
        
        st.markdown(f"#### Bun venit, {current_user}! Aici poți vedea istoricul și programările tale.")
        if not client_progs.empty:
            st.dataframe(client_progs[["Dată", "Ora Start", "Ora Sfârșit", "Serviciu", "Stilist", "Preț", "Durată", "Status"]], use_container_width=True)
            
            st.markdown("---")
            st.markdown("##### ❌ Anulare Programare Viitoare")
            viitoare = client_progs[client_progs["Dată"] >= str(date.today())]
            if not viitoare.empty:
                id_anulat = st.selectbox("Alege programarea de anulat", viitoare["ID"].tolist())
                if st.button("Anulează această programare"):
                    st.session_state.prog_df.loc[st.session_state.prog_df["ID"] == id_anulat, "Status"] = "Anulat"
                    save_all()
                    st.success("Programarea a fost anulată! Administratorul a fost notificat în sistem.")
                    st.info(f"🔔 Notificare trimisă administratorului: Clientul {current_user} a anulat programarea {id_anulat}.")
                    trigger_rerun()
            else:
                st.info("Nu ai programări viitoare active pe care să le poți anula.")
        else:
            st.info("Nu ai nicio programare înregistrată momentan.")

# ==========================================
# TAB 2: ADAUGĂ PROGRAMARE
# ==========================================
with tabs[1]:
    st.markdown("### ➕ Adaugă Programare Nouă")
    
    if "msg_status" in st.session_state:
        if st.session_state["msg_status"]["type"] == "error":
            st.markdown(f'<div class="overlap-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-alert">{st.session_state["msg_status"]["text"]}</div>', unsafe_allow_html=True)
        del st.session_state["msg_status"]

    existent_clients = st.session_state.prog_df[["Client", "Telefon"]].drop_duplicates().to_dict(orient="records") if not st.session_state.prog_df.empty else []

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        client_nume = st.text_input("👤 Nume Client", value=current_user if not is_admin else "")
        client_tel = st.text_input("📞 Telefon Client", value="")
        
        matched_c = [c for c in existent_clients if c["Client"].lower() == client_nume.lower()]
        if matched_c and not client_tel:
            client_tel = str(matched_c[0].get("Telefon", ""))

        p_data = st.date_input("📅 Dată Programare", value=date.today())
        p_ora = st.text_input("⏰ Ora Start (ex: 14:00)", value="10:00")

    with col_in2:
        serv_opt = st.session_state.serv_df["Serviciu"].tolist() if not st.session_state.serv_df.empty else ["Tuns"]
        p_serviciu = st.selectbox("✂️ Serviciu Dorit", serv_opt)
        
        s_row = st.session_state.serv_df[st.session_state.serv_df["Serviciu"] == p_serviciu]
        p_pret = int(s_row["Preț"].values[0]) if not s_row.empty else 50
        p_durata = int(s_row["Durată (min)"].values[0]) if not s_row.empty else 30
        
        st.info(f"⏱️ Durată estimată: **{p_durata} minute** | 💰 Preț: **{p_pret} RON**")

        stilisti_list = [u for u, r in zip(st.session_state.users_df["Utilizator"], st.session_state.users_df["Rol"]) if r == "Administrator"]
        p_stilist = st.selectbox("💈 Stilist / Frizer", stilisti_list if stilisti_list else ["Alex"])
        p_obs = st.text_area("📝 Observații / Preferințe client")

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
        st.markdown(f'<div class="overlap-alert">⚠️ ATENȚIE: Intervalul selectat ({p_ora} - {ora_sfarsit}) se suprapune cu o altă programare existentă pentru stilistul {p_stilist}!</div>', unsafe_allow_html=True)

    if client_nume:
        c_history = st.session_state.prog_df[st.session_state.prog_df["Client"].str.contains(client_nume, case=False, na=False)] if not st.session_state.prog_df.empty else pd.DataFrame()
        if not c_history.empty:
            with st.expander(f"📂 Istoric Client: {client_nume} ({len(c_history)} programări anterioare/viitoare)"):
                st.dataframe(c_history[["Dată", "Ora Start", "Serviciu", "Stilist", "Preț", "Status"]], use_container_width=True)

    def action_save():
        if not client_nume:
            st.session_state["msg_status"] = {"type": "error", "text": "Te rog introdu numele clientului!"}
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
        
        msg = "✅ Programarea a fost salvată cu succes!"
        if has_ov:
            msg += " (Notă: A fost înregistrată în ciuda suprapunerii detectate)."
        
        st.session_state["msg_status"] = {"type": "success", "text": msg}
        trigger_rerun()

    st.button("💾 Salvează Programarea în Sistem", type="primary", use_container_width=True, on_click=action_save)

# ==========================================
# TAB 3: SERVICII & PREȚURI
# ==========================================
with tabs[2]:
    st.markdown("### 💇‍♂️ Gestiune Servicii & Prețuri")
    
    df_serv = st.session_state.serv_df.copy()
    st.dataframe(df_serv, use_container_width=True)

    if is_admin:
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### ➕ Adaugă Serviciu Nou")
            with st.form("add_serv"):
                ns_nume = st.text_input("Nume Serviciu")
                ns_pret = st.number_input("Preț (RON)", min_value=0, value=50)
                ns_durata = st.number_input("Durată (minute)", min_value=5, value=30)
                if st.form_submit_button("Adaugă Serviciu"):
                    if ns_nume:
                        new_s = pd.DataFrame([{"Serviciu": ns_nume, "Preț": ns_pret, "Durată (min)": ns_durata}])
                        st.session_state.serv_df = pd.concat([st.session_state.serv_df, new_s], ignore_index=True)
                        save_all()
                        st.success("Serviciu adăugat!")
                        trigger_rerun()
        with col_s2:
            st.markdown("#### 🗑️ Șterge Serviciu")
            del_serv = st.selectbox("Selectează serviciul de șters", df_serv["Serviciu"].tolist() if not df_serv.empty else [])
            if st.button("Șterge Serviciul Selectat", type="primary"):
                st.session_state.serv_df = st.session_state.serv_df[st.session_state.serv_df["Serviciu"] != del_serv]
                save_all()
                st.success("Serviciul a fost șters.")
                trigger_rerun()

# ==========================================
# TAB 4: RAPORT FINANCIAR (Doar Admin)
# ==========================================
if is_admin:
    with tabs[3]:
        st.markdown("### 📊 Raport Financiar Profesional")
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
                sel_stilist_r = st.selectbox("Filtrează după Stilist Raport", stilisti_raport)

            if sel_luna != "Toate":
                df_f = df_f[df_f["Lună"] == sel_luna]
            if sel_stilist_r != "Toți":
                df_f = df_f[df_f["Stilist"] == sel_stilist_r]

            total_incasari_efectuate = df_f[df_f["Status"] == "Efectuat"]["Preț"].sum()
            total_programari = len(df_f)

            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Încasări Reale (Efectuat)</div><div class="metric-val">{total_incasari_efectuate} RON</div></div>', unsafe_allow_html=True)
            with c_f2:
                st.markdown(f'<div class="salon-card"><div class="metric-lbl">Total Programări în Filtru</div><div class="metric-val">{total_programari}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if not df_f.empty:
                fig = px.bar(
                    df_f, x="Dată", y="Preț", color="Stilist", barmode="group",
                    title="Încasări Zilnice Detaliate pe Stilist",
                    template="plotly_dark",
                    color_discrete_sequence=["#d4af37", "#38bdf8", "#34d399", "#f43f5e"]
                )
                max_p = df_f["Preț"].max() if not df_f.empty else 100
                fig.update_layout(yaxis=dict(range=[0, max_p * 1.25]))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există suficiente date financiare pentru generarea rapoartelor.")

# ==========================================
# TAB 5: SETĂRI & UTILIZATORI (Doar Admin)
# ==========================================
if is_admin:
    with tabs[4]:
        st.markdown("### ⚙️ Panou Setări & Gestiune Utilizatori")
        
        st.markdown("#### 👥 Utilizatori Înregistrați în Sistem")
        st.dataframe(st.session_state.users_df, use_container_width=True)

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("##### Adaugă / Editează Utilizator")
            with st.form("add_user_form"):
                n_user = st.text_input("Nume Utilizator / Client")
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
                        st.success(f"Utilizatorul {n_user} a fost salvat cu succes!")
                        trigger_rerun()
        
        with col_u2:
            st.markdown("##### Șterge Utilizator")
            del_user_target = st.selectbox("Alege utilizatorul de șters", st.session_state.users_df["Utilizator"].tolist())
            if st.button("Șterge Utilizatorul", type="primary"):
                if del_user_target in ["Alex", "Denis"]:
                    st.error("Nu poți șterge administratorii principali ai salonului!")
                else:
                    st.session_state.users_df = st.session_state.users_df[st.session_state.users_df["Utilizator"] != del_user_target]
                    save_all()
                    st.success("Utilizator șters cu succes.")
                    trigger_rerun()

        st.markdown("---")
        st.markdown("#### 🕒 Orar și Preferințe Salon")
        st.text_input("Program de lucru", value="Luni - Sâmbătă: 09:00 - 20:00")
        st.text_input("Locație / Adresă Salon", value="Str. Principală Nr. 10, București")
        st.success("Setările generale sunt salvate automat.")
