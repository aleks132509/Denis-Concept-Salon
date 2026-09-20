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
                        
                        # ==========================================
                        # TRIMITERE DINAMICĂ WHATSAPP CĂTRE STILIST / ADMIN
                        # ==========================================
                        cli_name_mg = curr_mgmt_row["Client"]
                        stilist_mg = curr_mgmt_row["Stilist"]
                        
                        # Căutăm stilistul/adminul în baza de date a utilizatorilor
                        stylist_u_row = st.session_state.users_df[st.session_state.users_df["Utilizator"] == stilist_mg]
                        
                        # Valori implicite (fallback la Alex / Master)
                        target_phone = "+35796005530"
                        target_apikey = MASTER_WHATSAPP_APIKEY
                        
                        if not stylist_u_row.empty:
                            r_user = stylist_u_row.iloc[0]
                            # Dacă stilistul are telefon setat în users_df, îl folosim pe al lui
                            if "Telefon" in r_user and pd.notna(r_user["Telefon"]) and str(r_user["Telefon"]).strip() != "":
                                target_phone = str(r_user["Telefon"]).strip()
                            
                            # Dacă stilistul are propriul APIKey setat, îl folosim pe al lui, altfel rămâne Master
                            if "APIKey" in r_user and pd.notna(r_user["APIKey"]) and str(r_user["APIKey"]).strip() != "":
                                target_apikey = str(r_user["APIKey"]).strip()
                        
                        wa_msg_admin = (
                            f"NOTIFICARE ANULARE\n"
                            f"Programarea #{sel_mg_nr} a fost anulata!\n"
                            f"Client: {cli_name_mg}\n"
                            f"Stilist: {stilist_mg}\n"
                            f"Data & Ora: {format_ro_date(curr_mgmt_row['Dată'])} | {curr_mgmt_row['Ora Start']}\n"
                            f"Serviciu: {curr_mgmt_row['Serviciu']}"
                        )
                        
                        # Trimite mesajul către numărul corect (al stilistului sau adminului) prin CallMeBot
                        if target_phone:
                            send_free_automatic_whatsapp(target_phone, wa_msg_admin, target_apikey)
                        
                        st.toast("Programare anulată și notificare trimisă pe WhatsApp!", icon="⚠️")
                        trigger_rerun()
                with col_btn_m3:
                    if st.button("Șterge Definitiv", type="primary"):
                        st.session_state.prog_df = st.session_state.prog_df[st.session_state.prog_df["Nr. Programare"] != sel_mg_nr]
                        save_all()
                        st.toast("Programare ștersă definitiv.", icon="🗑️")
                        trigger_rerun()
