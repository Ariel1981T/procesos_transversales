"""
Plataforma de Procesos Transversales — Grupo IMEMSA
Aplicación principal
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

import config as C
import sheets_manager as sm
import notifications as notif
from styles import get_css, badge, avatar, metric_card, progress_bar

st.set_page_config(
    page_title="IMEMSA — Procesos Transversales",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(get_css(), unsafe_allow_html=True)

# ════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ════════════════════════════════════════════
DEFAULTS = {
    "logged_in": False, "user": None, "page": "inicio",
    "selected_instance": None, "selected_template": None,
    "show_upload": False, "show_launch": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════
# AUTHENTICATION
# ════════════════════════════════════════════
def login_page():
    st.markdown("""
    <div style="text-align:center;margin-top:3rem;">
        <h1 style="font-size:2.5rem;font-weight:800;color:#0D2B6E;margin-bottom:0;">IMEMSA</h1>
        <p style="color:#C41E2E;font-size:1rem;font-weight:600;margin-top:0.2rem;">
            Plataforma de Procesos Transversales</p>
        <p style="color:#666;font-size:0.9rem;">Grupo IMEMSA — Control y Seguimiento</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("---")
        email = st.text_input("📧 Correo institucional", placeholder="tucorreo@imemsa.com.mx")
        if st.button("🔐 Iniciar Sesión", use_container_width=True, type="primary"):
            if not email:
                st.error("Ingresa tu correo electrónico.")
                return
            if not sm.validate_domain(email):
                st.error(f"Dominio no autorizado. Dominios permitidos: {', '.join(C.DOMINIOS_PERMITIDOS)}")
                return
            user = sm.find_user_by_email(email)
            if not user:
                st.error("Correo no registrado en el sistema. Contacta al Project Manager o Administrador.")
                return
            if str(user.get("Activo", "Sí")).strip().lower() in ["no", "false", "0"]:
                st.error("Tu cuenta está desactivada. Contacta al Administrador.")
                return
            st.session_state.logged_in = True
            st.session_state.user = user
            sm.log_action(user["Nombre"], "Login", "Sistema", "", f"Acceso desde {email}")
            st.rerun()


def header():
    user = st.session_state.user
    role_emoji = {"PM": "👔", "Gerente": "🏭", "Responsable": "👤", "Admin": "⚙️"}
    emoji = role_emoji.get(user.get("Rol", ""), "👤")
    st.markdown(f"""
    <div class="imemsa-header">
        <div>
            <h1>📋 Procesos Transversales</h1>
            <div class="subtitle">Grupo IMEMSA — Control y Seguimiento</div>
        </div>
        <div class="user-badge">{emoji} {user.get('Nombre', '')} — {user.get('Rol', '')}</div>
    </div>
    """, unsafe_allow_html=True)


def navigation():
    user = st.session_state.user
    rol = user.get("Rol", "Responsable")
    pages = {"inicio": "🏠 Inicio", "mis_tareas": "📥 Mis Tareas"}
    if rol in ["Gerente", "PM", "Admin"]:
        pages["biblioteca"] = "📚 Biblioteca"
        pages["mis_procesos"] = "📊 Mis Procesos"
    if rol in ["PM", "Admin"]:
        pages["pm_panel"] = "👔 Panel PM"
    if rol == "Admin":
        pages["admin"] = "⚙️ Admin"

    cols = st.columns(len(pages) + 1)
    for i, (key, label) in enumerate(pages.items()):
        if cols[i].button(label, key=f"nav_{key}", use_container_width=True,
                          type="primary" if st.session_state.page == key else "secondary"):
            st.session_state.page = key
            st.session_state.selected_instance = None
            st.session_state.selected_template = None
            st.rerun()
    if cols[-1].button("🚪 Salir", use_container_width=True):
        for k in DEFAULTS:
            st.session_state[k] = DEFAULTS[k]
        st.rerun()


# ════════════════════════════════════════════
# PAGE: INICIO / DASHBOARD
# ════════════════════════════════════════════
def page_inicio():
    user = st.session_state.user
    rol = user.get("Rol", "Responsable")
    st.markdown('<div class="section-title">📊 Dashboard General</div>', unsafe_allow_html=True)

    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    avances = sm.get_all_records(C.HOJA_AVANCE)

    active = [i for i in instances if i.get("Estatus") == "En Proceso"]
    completed = [i for i in instances if i.get("Estatus") == "Completado"]
    overdue_activities = [a for a in avances if a.get("Estatus") == "Activa"
                          and sm.remaining_business_days(a.get("Fecha_Limite", "")) < 0]
    at_risk = [a for a in avances if a.get("Estatus") == "Activa"
               and 0 <= sm.remaining_business_days(a.get("Fecha_Limite", "")) <= C.DIAS_ALERTA_AMARILLA]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card(len(active), "Procesos Activos"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(len(completed), "Completados", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(len(at_risk), "Actividades en Riesgo", "yellow"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card(len(overdue_activities), "Actividades Vencidas", "red"), unsafe_allow_html=True)

    if active:
        st.markdown('<div class="section-title">📋 Procesos Activos</div>', unsafe_allow_html=True)
        for inst in active:
            pct = inst.get("Porcentaje_Avance", 0)
            try:
                pct = int(float(str(pct).replace("%", "")))
            except (ValueError, TypeError):
                pct = 0
            folio = inst.get("ID_Instancia", "")
            nombre = inst.get("Nombre_Instancia", "")

            with st.container():
                col1, col2, col3 = st.columns([3, 4, 1])
                with col1:
                    st.markdown(f"**{folio}**")
                    st.caption(nombre)
                with col2:
                    st.markdown(progress_bar(pct), unsafe_allow_html=True)
                with col3:
                    if st.button("Ver ➜", key=f"ver_{folio}"):
                        st.session_state.selected_instance = folio
                        st.session_state.page = "ver_instancia"
                        st.rerun()
                st.divider()


# ════════════════════════════════════════════
# PAGE: MIS TAREAS (Bandeja del Responsable)
# ════════════════════════════════════════════
def page_mis_tareas():
    user = st.session_state.user
    email = user.get("Correo", "").strip().lower()
    st.markdown('<div class="section-title">📥 Mis Tareas Pendientes</div>', unsafe_allow_html=True)

    avances = sm.get_all_records(C.HOJA_AVANCE)
    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    inst_map = {i["ID_Instancia"]: i for i in instances}

    my_tasks = [a for a in avances
                if a.get("Correo", "").strip().lower() == email
                and a.get("Estatus") in ["Activa", "Vencida"]]

    # Sort: overdue first, then at risk, then on time
    def sort_key(t):
        remaining = sm.remaining_business_days(t.get("Fecha_Limite", ""))
        return remaining
    my_tasks.sort(key=sort_key)

    if not my_tasks:
        st.markdown('<div class="success-box">🎉 ¡No tienes tareas pendientes!</div>', unsafe_allow_html=True)
        return

    overdue = [t for t in my_tasks if sm.remaining_business_days(t.get("Fecha_Limite", "")) < 0]
    at_risk = [t for t in my_tasks if 0 <= sm.remaining_business_days(t.get("Fecha_Limite", "")) <= C.DIAS_ALERTA_AMARILLA]
    on_time = [t for t in my_tasks if sm.remaining_business_days(t.get("Fecha_Limite", "")) > C.DIAS_ALERTA_AMARILLA]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(metric_card(len(my_tasks), "Total Pendientes"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(len(at_risk), "En Riesgo", "yellow"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(len(overdue), "Vencidas", "red"), unsafe_allow_html=True)

    st.markdown("---")

    for task in my_tasks:
        remaining = sm.remaining_business_days(task.get("Fecha_Limite", ""))
        inst_id = task.get("ID_Instancia", "")
        inst = inst_map.get(inst_id, {})

        if remaining < 0:
            css_class = "vencida"
            status_badge = badge("Vencida", "vencida")
            days_text = f"<strong style='color:#C41E2E;'>{abs(remaining)}d vencida</strong>"
        elif remaining <= C.DIAS_ALERTA_AMARILLA:
            css_class = "en-riesgo"
            status_badge = badge("En Riesgo", "en-riesgo")
            days_text = f"<strong style='color:#e6a800;'>{remaining}d restante(s)</strong>"
        else:
            css_class = "activa"
            status_badge = badge("Activa", "activa")
            days_text = f"<strong style='color:#28a745;'>{remaining}d restante(s)</strong>"

        st.markdown(f"""
        <div class="activity-card {css_class}">
            <div class="activity-header">
                <div>
                    <span class="activity-num">{task.get('Numero_Actividad','')}</span>
                    <span class="activity-title">{task.get('Actividad','')}</span>
                </div>
                <div>{status_badge}</div>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.3rem;">
                <span style="font-size:0.82rem;color:#666;">
                    🗂️ {inst.get('Nombre_Instancia', inst_id)} &nbsp;|&nbsp;
                    📅 Límite: {task.get('Fecha_Limite','')} &nbsp;|&nbsp; {days_text}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 2, 1])
        ev_required = str(task.get("Evidencia_Requerida", "")).lower() in ["sí", "si", "yes", "true", "1"]
        has_evidence = str(task.get("Tiene_Evidencia", "")).lower() in ["sí", "si", "yes", "true", "1"]

        with col1:
            uploaded = st.file_uploader(
                "📎 Subir evidencia", key=f"ev_{inst_id}_{task.get('Numero_Actividad','')}",
                help="Sube un archivo como evidencia de esta actividad"
            )
            if uploaded:
                try:
                    import cloudinary
                    import cloudinary.uploader
                    cloudinary.config(
                        cloud_name=st.secrets["cloudinary"]["cloud_name"],
                        api_key=st.secrets["cloudinary"]["api_key"],
                        api_secret=st.secrets["cloudinary"]["api_secret"]
                    )
                    result = cloudinary.uploader.upload(
                        uploaded.getvalue(),
                        resource_type="raw",
                        folder=f"imemsa-procesos/{inst_id}",
                        public_id=uploaded.name
                    )
                    ev_id = f"EV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    sm.append_row(C.HOJA_EVIDENCIAS, [
                        ev_id, inst_id, task.get("Numero_Actividad", ""),
                        uploaded.name, result["secure_url"], result["public_id"],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user.get("Nombre", "")
                    ])
                    sm.update_row_by_id(C.HOJA_AVANCE, "ID_Avance", task.get("ID_Avance", ""),
                                        {"Tiene_Evidencia": "Sí"})
                    sm.log_action(user["Nombre"], "Subir evidencia", "Actividad",
                                  task.get("ID_Avance", ""), uploaded.name)
                    st.success(f"✅ Evidencia '{uploaded.name}' subida correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al subir evidencia: {e}")

        with col2:
            comment = st.text_input("💬 Comentario", key=f"com_{inst_id}_{task.get('Numero_Actividad','')}")
            if comment and st.button("Enviar", key=f"btn_com_{inst_id}_{task.get('Numero_Actividad','')}"):
                com_id = f"COM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                sm.append_row(C.HOJA_COMENTARIOS, [
                    com_id, inst_id, task.get("Numero_Actividad", ""),
                    user.get("Nombre", ""), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment
                ])
                st.success("💬 Comentario agregado.")
                st.rerun()

        with col3:
            can_complete = True
            if ev_required and not has_evidence and not uploaded:
                can_complete = False
                st.caption("⚠️ Requiere evidencia")

            if st.button("✅ Completar", key=f"done_{inst_id}_{task.get('Numero_Actividad','')}",
                         disabled=not can_complete, type="primary"):
                complete_activity(task, inst)

        st.markdown("---")


def complete_activity(task, inst):
    user = st.session_state.user
    now = datetime.now()
    inst_id = task["ID_Instancia"]
    num_act = int(task["Numero_Actividad"])

    # Update current activity
    fecha_cierre = now.strftime("%Y-%m-%d")
    fecha_inicio = task.get("Fecha_Inicio", fecha_cierre)
    try:
        d_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        dias_reales = sm.business_days_between(d_inicio, now.date())
    except (ValueError, TypeError):
        dias_reales = 0
    dias_teoricos = int(task.get("Dias_Teoricos", 0))
    desviacion = dias_reales - dias_teoricos

    sm.update_row_by_id(C.HOJA_AVANCE, "ID_Avance", task["ID_Avance"], {
        "Fecha_Cierre": fecha_cierre,
        "Estatus": "Completada",
        "Dias_Reales": dias_reales,
        "Desviacion": desviacion
    })

    sm.log_action(user["Nombre"], "Completar actividad", "Actividad",
                  task["ID_Avance"], f"Act #{num_act} de {inst_id}")

    # Notify manager
    notif.notify_task_completed(
        inst.get("Gerente_Responsable", ""), inst.get("Gerente_Responsable", ""),
        task.get("Actividad", ""), user.get("Nombre", ""),
        inst.get("Nombre_Instancia", "")
    )

    # Activate next activity
    all_avances = sm.get_all_records(C.HOJA_AVANCE)
    inst_avances = [a for a in all_avances if a["ID_Instancia"] == inst_id]
    inst_avances.sort(key=lambda x: int(x.get("Numero_Actividad", 0)))

    next_task = None
    for a in inst_avances:
        if int(a.get("Numero_Actividad", 0)) == num_act + 1:
            next_task = a
            break

    if next_task:
        fecha_inicio_next = now.strftime("%Y-%m-%d")
        dias_next = int(next_task.get("Dias_Teoricos", 1))
        fecha_limite_next = sm.add_business_days(now.date(), dias_next).strftime("%Y-%m-%d")
        sm.update_row_by_id(C.HOJA_AVANCE, "ID_Avance", next_task["ID_Avance"], {
            "Fecha_Inicio": fecha_inicio_next,
            "Fecha_Limite": fecha_limite_next,
            "Estatus": "Activa"
        })
        notif.notify_task_activated(
            next_task.get("Correo", ""), next_task.get("Responsable", ""),
            inst.get("Nombre_Instancia", ""), next_task.get("Actividad", ""),
            dias_next, fecha_limite_next
        )

    # Update instance progress
    total = len(inst_avances)
    completed = len([a for a in inst_avances if a.get("Estatus") == "Completada"]) + 1
    pct = int((completed / total) * 100) if total > 0 else 0

    updates = {"Porcentaje_Avance": pct}
    if completed >= total:
        updates["Estatus"] = "Completado"
        updates["Fecha_Real_Fin"] = fecha_cierre
        notif.notify_process_completed(
            inst.get("Gerente_Responsable", ""), inst.get("Gerente_Responsable", ""),
            inst.get("Nombre_Instancia", ""), inst_id
        )
    sm.update_row_by_id(C.HOJA_INSTANCIAS, "ID_Instancia", inst_id, updates)

    st.success("✅ Actividad completada exitosamente.")
    st.rerun()


# ════════════════════════════════════════════
# PAGE: BIBLIOTECA DE PLANTILLAS
# ════════════════════════════════════════════
def page_biblioteca():
    st.markdown('<div class="section-title">📚 Biblioteca de Plantillas</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nueva Plantilla", type="primary", use_container_width=True):
            st.session_state.show_upload = True

    templates = sm.get_all_records(C.HOJA_PLANTILLAS)
    active_templates = [t for t in templates if t.get("Estatus") == "Activa"]

    if not active_templates:
        st.markdown('<div class="info-box">📭 No hay plantillas activas. Crea la primera subiendo un archivo Excel.</div>',
                    unsafe_allow_html=True)

    for tpl in active_templates:
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 1.5])
            with c1:
                st.markdown(f"**{tpl.get('Nombre', '')}**")
                st.caption(f"📁 {tpl.get('Area_Origen', '')} · 👤 {tpl.get('Gerente_Creador', '')} · "
                           f"v{tpl.get('Version', 1)}")
            with c2:
                st.metric("Actividades", tpl.get("Num_Actividades", 0))
            with c3:
                st.metric("Días Teóricos", tpl.get("Dias_Teoricos_Total", 0))
            with c4:
                veces = tpl.get("Veces_Utilizada", 0)
                st.metric("Usos", veces)
                if st.button("🚀 Lanzar", key=f"launch_{tpl.get('ID_Plantilla', '')}"):
                    st.session_state.selected_template = tpl.get("ID_Plantilla", "")
                    st.session_state.show_launch = True
                    st.rerun()
            st.divider()

    # ── Upload Excel Dialog ──
    if st.session_state.get("show_upload"):
        upload_template_form()

    # ── Launch Instance Dialog ──
    if st.session_state.get("show_launch"):
        launch_instance_form()


def upload_template_form():
    st.markdown('<div class="section-title">📤 Crear Nueva Plantilla</div>', unsafe_allow_html=True)

    with st.form("upload_form"):
        auth_code = st.text_input("🔑 Número de Confirmación del PM", placeholder="PT-2026-001")
        nombre = st.text_input("📋 Nombre del Proceso", placeholder="Ej. Compra de Motores Yamaha")
        descripcion = st.text_area("📝 Descripción del Proceso")
        area = st.text_input("🏢 Área de Origen", placeholder="Ej. Comercial")
        uploaded_file = st.file_uploader("📄 Archivo Excel de Actividades", type=["xlsx", "xls"])

        st.markdown("""
        <div class="info-box">
        📌 <strong>El archivo Excel debe contener estas columnas:</strong>
        No., Fase, Actividad, Responsable, Correo, Telefono, Días teoricos<br>
        <em>Opcionales: Descripción, Evidencia requerida</em>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("✅ Crear Plantilla", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("❌ Cancelar", use_container_width=True)

    if cancel:
        st.session_state.show_upload = False
        st.rerun()

    if submit:
        if not auth_code or not nombre or not uploaded_file:
            st.error("Completa todos los campos obligatorios.")
            return

        # Validate auth code
        auths = sm.get_all_records(C.HOJA_AUTORIZACIONES)
        auth_record = next((a for a in auths if a["ID_Autorizacion"] == auth_code.strip()), None)
        if not auth_record:
            st.error(f"❌ Número de confirmación '{auth_code}' no encontrado.")
            return
        if auth_record.get("Estatus") != "Vigente":
            st.error(f"❌ Número de confirmación con estatus: {auth_record.get('Estatus')}. Debe ser 'Vigente'.")
            return
        try:
            venc = datetime.strptime(auth_record.get("Fecha_Vencimiento", ""), "%Y-%m-%d").date()
            if datetime.now().date() > venc:
                sm.update_cell_by_id(C.HOJA_AUTORIZACIONES, "ID_Autorizacion", auth_code,
                                     "Estatus", "Vencida")
                st.error("❌ Número de confirmación vencido.")
                return
        except ValueError:
            pass

        # Parse Excel
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return

        # Validate columns
        df.columns = df.columns.str.strip()
        missing = [c for c in C.COLUMNAS_EXCEL_OBLIGATORIAS if c not in df.columns]
        if missing:
            st.error(f"❌ Columnas faltantes: {', '.join(missing)}")
            return

        # Validate data
        errors = []
        for i, row in df.iterrows():
            row_num = i + 2
            if pd.isna(row.get("Actividad")) or str(row.get("Actividad", "")).strip() == "":
                errors.append(f"Fila {row_num}: Actividad vacía")
            email = str(row.get("Correo", "")).strip()
            if "@" not in email:
                errors.append(f"Fila {row_num}: Correo inválido ({email})")
            elif not sm.validate_domain(email):
                errors.append(f"Fila {row_num}: Dominio no autorizado ({email})")

        if errors:
            st.error("❌ Errores de validación:\n" + "\n".join(errors[:10]))
            return

        # Auto-register new users
        new_users, discrepancies = sm.auto_register_users(df)
        if new_users:
            st.info(f"👥 {len(new_users)} usuario(s) nuevo(s) registrado(s) automáticamente.")
        if discrepancies:
            for d in discrepancies:
                st.warning(f"⚠️ {d['email']}: {d['campo']} diferente (existente: {d['existente']}, Excel: {d['nuevo']})")

        # Create template
        user = st.session_state.user
        tpl_id = sm.get_next_id("TPL-", C.HOJA_PLANTILLAS, "ID_Plantilla")
        fases = df["Fase"].nunique()
        dias_total = int(df["Días teoricos"].sum())

        sm.append_row(C.HOJA_PLANTILLAS, [
            tpl_id, nombre, descripcion, area, user.get("Nombre", ""),
            datetime.now().strftime("%Y-%m-%d"), 1, "Activa",
            len(df), fases, 0, auth_code, dias_total
        ])

        # Create activities
        for _, row in df.iterrows():
            act_id = f"ACT-{tpl_id}-{int(row['No.']):02d}"
            ev_req = str(row.get("Evidencia requerida", "No")).strip()
            ev_req = "Sí" if ev_req.lower() in ["sí", "si", "yes", "true", "1"] else "No"
            desc = str(row.get("Descripción", "")) if "Descripción" in df.columns else ""

            sm.append_row(C.HOJA_ACTIVIDADES_PLANTILLA, [
                act_id, tpl_id, int(row["No."]), row["Fase"], row["Actividad"],
                desc, row["Responsable"], str(row["Correo"]).strip(),
                str(int(row["Telefono"])) if pd.notna(row["Telefono"]) else "",
                int(row["Días teoricos"]), ev_req
            ])

        # Consume authorization
        sm.update_row_by_id(C.HOJA_AUTORIZACIONES, "ID_Autorizacion", auth_code, {
            "Estatus": "Consumida",
            "ID_Vinculado": tpl_id,
            "Fecha_Consumo": datetime.now().strftime("%Y-%m-%d")
        })

        sm.log_action(user["Nombre"], "Crear plantilla", "Plantilla", tpl_id,
                      f"{nombre} ({len(df)} actividades)")

        # Send welcome emails to new users
        for nu in new_users:
            first_act = df.iloc[0]["Actividad"] if len(df) > 0 else ""
            notif.notify_welcome(nu["Correo"], nu["Nombre"], nombre, first_act)

        st.session_state.show_upload = False
        st.success(f"✅ Plantilla '{nombre}' creada exitosamente con ID {tpl_id}")
        st.rerun()


def launch_instance_form():
    tpl_id = st.session_state.get("selected_template", "")
    templates = sm.get_all_records(C.HOJA_PLANTILLAS)
    tpl = next((t for t in templates if t["ID_Plantilla"] == tpl_id), None)
    if not tpl:
        st.error("Plantilla no encontrada.")
        return

    st.markdown(f'<div class="section-title">🚀 Lanzar Instancia de: {tpl.get("Nombre", "")}</div>',
                unsafe_allow_html=True)

    # Show template summary
    st.markdown(f"""
    <div class="info-box">
        📋 <strong>Plantilla:</strong> {tpl.get('Nombre', '')} (v{tpl.get('Version', 1)})<br>
        🔢 <strong>Actividades:</strong> {tpl.get('Num_Actividades', 0)} &nbsp;|&nbsp;
        📅 <strong>Días teóricos:</strong> {tpl.get('Dias_Teoricos_Total', 0)} &nbsp;|&nbsp;
        🏢 <strong>Área:</strong> {tpl.get('Area_Origen', '')} &nbsp;|&nbsp;
        🔄 <strong>Usos anteriores:</strong> {tpl.get('Veces_Utilizada', 0)}
    </div>
    """, unsafe_allow_html=True)

    with st.form("launch_form"):
        nombre_inst = st.text_input("📋 Nombre de la Instancia",
                                     placeholder="Ej. PROD. JULIO RECEP. SEPTIEMBRE 2026")
        descripcion = st.text_area("📝 Descripción / Detalles")
        c1, c2 = st.columns(2)
        unidades = c1.number_input("📦 Unidades (si aplica)", min_value=0, value=0)
        importe = c2.number_input("💰 Importe (si aplica)", min_value=0.0, value=0.0, format="%.2f")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("🚀 Lanzar Proceso", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("❌ Cancelar", use_container_width=True)

    if cancel:
        st.session_state.show_launch = False
        st.session_state.selected_template = None
        st.rerun()

    if submit:
        if not nombre_inst:
            st.error("Ingresa un nombre para la instancia.")
            return

        # Get template activities
        all_acts = sm.get_all_records(C.HOJA_ACTIVIDADES_PLANTILLA)
        tpl_acts = [a for a in all_acts if a["ID_Plantilla"] == tpl_id]
        tpl_acts.sort(key=lambda x: int(x.get("Numero", 0)))

        if not tpl_acts:
            st.error("La plantilla no tiene actividades definidas.")
            return

        # Create instance
        user = st.session_state.user
        inst_id = sm.get_next_instance_id()
        now = datetime.now()
        dias_total = int(tpl.get("Dias_Teoricos_Total", 0))
        fecha_est_fin = sm.add_business_days(now.date(), dias_total).strftime("%Y-%m-%d")

        sm.append_row(C.HOJA_INSTANCIAS, [
            inst_id, tpl_id, nombre_inst, descripcion, user.get("Nombre", ""),
            now.strftime("%Y-%m-%d"), fecha_est_fin, "", "En Proceso", 0,
            tpl.get("ID_Autorizacion", "Plantilla aprobada"),
            unidades if unidades > 0 else "",
            importe if importe > 0 else ""
        ])

        # Create avance records
        for act in tpl_acts:
            num = int(act.get("Numero", 0))
            avance_id = f"AV-{inst_id}-{num:02d}"

            if num == 1:
                f_inicio = now.strftime("%Y-%m-%d")
                dias = int(act.get("Dias_Teoricos", 1))
                f_limite = sm.add_business_days(now.date(), dias).strftime("%Y-%m-%d")
                estatus = "Activa"
            else:
                f_inicio = ""
                f_limite = ""
                estatus = "Pendiente"

            sm.append_row(C.HOJA_AVANCE, [
                avance_id, inst_id, num, act.get("Actividad", ""), act.get("Fase", ""),
                act.get("Responsable", ""), act.get("Correo", ""),
                act.get("Dias_Teoricos", 1), f_inicio, f_limite, "",
                estatus, "", "", act.get("Evidencia_Requerida", "No"), "No"
            ])

        # Notify first responsible
        first = tpl_acts[0]
        dias_first = int(first.get("Dias_Teoricos", 1))
        f_limite_first = sm.add_business_days(now.date(), dias_first).strftime("%Y-%m-%d")
        notif.notify_task_activated(
            first.get("Correo", ""), first.get("Responsable", ""),
            nombre_inst, first.get("Actividad", ""), dias_first, f_limite_first
        )

        # Update template usage count
        veces = int(tpl.get("Veces_Utilizada", 0)) + 1
        sm.update_cell_by_id(C.HOJA_PLANTILLAS, "ID_Plantilla", tpl_id, "Veces_Utilizada", veces)

        sm.log_action(user["Nombre"], "Lanzar instancia", "Instancia", inst_id, nombre_inst)

        st.session_state.show_launch = False
        st.session_state.selected_template = None
        st.success(f"✅ Proceso lanzado exitosamente: {inst_id}")
        st.rerun()


# ════════════════════════════════════════════
# PAGE: MIS PROCESOS
# ════════════════════════════════════════════
def page_mis_procesos():
    user = st.session_state.user
    st.markdown('<div class="section-title">📊 Mis Procesos</div>', unsafe_allow_html=True)

    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    rol = user.get("Rol", "")
    if rol in ["PM", "Admin"]:
        my_instances = instances
    else:
        my_instances = [i for i in instances if i.get("Gerente_Responsable") == user.get("Nombre")]

    if not my_instances:
        st.markdown('<div class="info-box">No tienes procesos registrados.</div>', unsafe_allow_html=True)
        return

    # Filters
    c1, c2 = st.columns(2)
    with c1:
        filter_status = st.selectbox("Filtrar por estatus", ["Todos"] + C.ESTATUS_INSTANCIA)
    with c2:
        search = st.text_input("🔍 Buscar", placeholder="Folio o nombre...")

    filtered = my_instances
    if filter_status != "Todos":
        filtered = [i for i in filtered if i.get("Estatus") == filter_status]
    if search:
        search_l = search.lower()
        filtered = [i for i in filtered if search_l in str(i.get("ID_Instancia", "")).lower()
                    or search_l in str(i.get("Nombre_Instancia", "")).lower()]

    for inst in filtered:
        folio = inst.get("ID_Instancia", "")
        pct = inst.get("Porcentaje_Avance", 0)
        try:
            pct = int(float(str(pct).replace("%", "")))
        except (ValueError, TypeError):
            pct = 0
        estatus = inst.get("Estatus", "En Proceso")

        with st.container():
            c1, c2, c3, c4 = st.columns([2.5, 3, 1.5, 1])
            with c1:
                st.markdown(f"**📋 {folio}**")
                st.caption(inst.get("Nombre_Instancia", ""))
            with c2:
                st.markdown(progress_bar(pct), unsafe_allow_html=True)
            with c3:
                st.markdown(badge(estatus), unsafe_allow_html=True)
                st.caption(f"Creado: {inst.get('Fecha_Creacion', '')}")
            with c4:
                if st.button("Ver ➜", key=f"vp_{folio}"):
                    st.session_state.selected_instance = folio
                    st.session_state.page = "ver_instancia"
                    st.rerun()
            st.divider()


# ════════════════════════════════════════════
# PAGE: VER INSTANCIA (Detalle completo)
# ════════════════════════════════════════════
def page_ver_instancia():
    inst_id = st.session_state.get("selected_instance")
    if not inst_id:
        st.warning("No se seleccionó ninguna instancia.")
        return

    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    inst = next((i for i in instances if i["ID_Instancia"] == inst_id), None)
    if not inst:
        st.error("Instancia no encontrada.")
        return

    avances = sm.get_all_records(C.HOJA_AVANCE)
    inst_avances = [a for a in avances if a["ID_Instancia"] == inst_id]
    inst_avances.sort(key=lambda x: int(x.get("Numero_Actividad", 0)))

    evidencias = sm.get_all_records(C.HOJA_EVIDENCIAS)
    inst_evidencias = [e for e in evidencias if e["ID_Instancia"] == inst_id]

    comentarios = sm.get_all_records(C.HOJA_COMENTARIOS)
    inst_comentarios = [c for c in comentarios if c["ID_Instancia"] == inst_id]

    pct = inst.get("Porcentaje_Avance", 0)
    try:
        pct = int(float(str(pct).replace("%", "")))
    except (ValueError, TypeError):
        pct = 0
    estatus = inst.get("Estatus", "En Proceso")

    # Back button
    if st.button("← Regresar"):
        st.session_state.selected_instance = None
        st.session_state.page = "mis_procesos"
        st.rerun()

    # Instance header
    st.markdown(f"""
    <div class="instance-header">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div class="instance-folio">📋 {inst_id}</div>
                <div style="font-size:1rem;color:#444;margin-top:0.3rem;">{inst.get('Nombre_Instancia','')}</div>
                <div style="font-size:0.82rem;color:#888;margin-top:0.2rem;">
                    {inst.get('Descripcion','')}
                </div>
            </div>
            <div style="text-align:right;">
                {badge(estatus)}
                <div style="font-size:0.8rem;color:#888;margin-top:0.5rem;">
                    Creado: {inst.get('Fecha_Creacion','')}<br>
                    Est. fin: {inst.get('Fecha_Estimada_Fin','')}
                </div>
            </div>
        </div>
        {progress_bar(pct)}
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    total = len(inst_avances)
    completed = len([a for a in inst_avances if a.get("Estatus") == "Completada"])
    overdue = len([a for a in inst_avances if a.get("Estatus") in ["Activa", "Vencida"]
                   and sm.remaining_business_days(a.get("Fecha_Limite", "")) < 0])
    at_risk = len([a for a in inst_avances if a.get("Estatus") == "Activa"
                   and 0 <= sm.remaining_business_days(a.get("Fecha_Limite", "")) <= C.DIAS_ALERTA_AMARILLA])
    on_time = len([a for a in inst_avances if a.get("Estatus") == "Activa"
                   and sm.remaining_business_days(a.get("Fecha_Limite", "")) > C.DIAS_ALERTA_AMARILLA])

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(metric_card(f"{completed}/{total}", "Completadas", "green"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(on_time, "En Tiempo"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(at_risk, "En Riesgo", "yellow"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card(overdue, "Vencidas", "red"), unsafe_allow_html=True)
    with c5:
        if inst.get("Unidades"):
            st.markdown(metric_card(inst.get("Unidades", ""), "Unidades"), unsafe_allow_html=True)
        if inst.get("Importe"):
            st.markdown(metric_card(f"${float(inst.get('Importe',0)):,.2f}", "Importe"), unsafe_allow_html=True)

    # Activities grouped by phase
    st.markdown('<div class="section-title">🔢 Actividades del Proceso</div>', unsafe_allow_html=True)

    current_phase = ""
    for act in inst_avances:
        phase = act.get("Fase", "")
        if phase != current_phase:
            current_phase = phase
            phase_acts = [a for a in inst_avances if a.get("Fase") == phase]
            phase_done = len([a for a in phase_acts if a.get("Estatus") == "Completada"])
            st.markdown(f'<div class="phase-header">📂 {phase} ({phase_done}/{len(phase_acts)} completadas)</div>',
                        unsafe_allow_html=True)

        estatus_act = act.get("Estatus", "Pendiente")
        remaining = sm.remaining_business_days(act.get("Fecha_Limite", "")) if act.get("Fecha_Limite") else None

        if estatus_act == "Completada":
            css_class = "completada"
            badge_html = badge("Completada", "completada")
        elif estatus_act == "Activa" and remaining is not None and remaining < 0:
            css_class = "vencida"
            badge_html = badge("Vencida", "vencida")
        elif estatus_act == "Activa" and remaining is not None and remaining <= C.DIAS_ALERTA_AMARILLA:
            css_class = "en-riesgo"
            badge_html = badge(f"⚠️ {remaining}d", "en-riesgo")
        elif estatus_act == "Activa":
            css_class = "activa"
            badge_html = badge(f"🟢 {remaining}d", "activa")
        else:
            css_class = "pendiente"
            badge_html = badge("Pendiente", "pendiente")

        # Dates info
        dates_html = ""
        if act.get("Fecha_Inicio"):
            dates_html += f"Inicio: {act['Fecha_Inicio']}"
        if act.get("Fecha_Limite"):
            dates_html += f" · Límite: {act['Fecha_Limite']}"
        if act.get("Fecha_Cierre"):
            dates_html += f" · Cierre: {act['Fecha_Cierre']}"

        # Evidence
        act_evidencias = [e for e in inst_evidencias if str(e.get("Numero_Actividad")) == str(act.get("Numero_Actividad"))]
        ev_html = ""
        if act_evidencias:
            ev_html = "📎 " + ", ".join([f"<a href='{e.get('URL_Cloudinary','')}' target='_blank'>{e.get('Nombre_Archivo','')}</a>"
                                          for e in act_evidencias])

        st.markdown(f"""
        <div class="activity-card {css_class}">
            <div class="activity-header">
                <div style="display:flex;align-items:center;">
                    <span class="activity-num">{act.get('Numero_Actividad','')}</span>
                    <div>
                        <span class="activity-title">{act.get('Actividad','')}</span>
                        <div class="activity-desc">
                            {avatar(act.get('Responsable',''))} {act.get('Responsable','')}
                            &nbsp;·&nbsp; Plazo: {act.get('Dias_Teoricos','')}d
                        </div>
                    </div>
                </div>
                <div>{badge_html}</div>
            </div>
            <div style="font-size:0.78rem;color:#888;margin-top:0.3rem;">
                {dates_html}
                {f' · {ev_html}' if ev_html else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Comments section
    if inst_comentarios:
        st.markdown('<div class="section-title">💬 Comentarios</div>', unsafe_allow_html=True)
        for com in inst_comentarios:
            st.markdown(f"""
            <div style="background:#f8f9fa;padding:0.6rem 1rem;border-radius:8px;margin-bottom:0.5rem;font-size:0.85rem;">
                {avatar(com.get('Autor',''), 24)}
                <strong>{com.get('Autor','')}</strong>
                <span style="color:#888;margin-left:0.5rem;">{com.get('Fecha','')}</span>
                <span style="color:#888;"> · Act #{com.get('Numero_Actividad','')}</span>
                <div style="margin-top:0.3rem;margin-left:2rem;">{com.get('Texto','')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Export button
    st.markdown("---")
    if st.button("📥 Exportar a Excel"):
        export_instance_to_excel(inst, inst_avances, inst_evidencias, inst_comentarios)


def export_instance_to_excel(inst, avances, evidencias, comentarios):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Avances sheet
        df_av = pd.DataFrame(avances)
        if not df_av.empty:
            df_av.to_excel(writer, sheet_name="Actividades", index=False)
        # Evidencias
        df_ev = pd.DataFrame(evidencias)
        if not df_ev.empty:
            df_ev.to_excel(writer, sheet_name="Evidencias", index=False)
        # Comentarios
        df_com = pd.DataFrame(comentarios)
        if not df_com.empty:
            df_com.to_excel(writer, sheet_name="Comentarios", index=False)
    output.seek(0)
    st.download_button(
        "⬇️ Descargar Excel",
        data=output.getvalue(),
        file_name=f"{inst.get('ID_Instancia','export')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ════════════════════════════════════════════
# PAGE: PANEL DEL PM
# ════════════════════════════════════════════
def page_pm_panel():
    st.markdown('<div class="section-title">👔 Panel del Project Manager</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔑 Autorizaciones", "📊 Dashboard Global", "👥 Usuarios"])

    with tab1:
        pm_autorizaciones()
    with tab2:
        pm_dashboard()
    with tab3:
        pm_usuarios()


def pm_autorizaciones():
    st.markdown("### Generar Número de Confirmación")

    with st.form("gen_auth"):
        c1, c2 = st.columns(2)
        solicitante = c1.text_input("👤 Solicitante (Gerente)")
        area = c2.text_input("🏢 Área")
        nombre_proceso = st.text_input("📋 Nombre tentativo del Proceso")
        tipo = st.selectbox("Tipo de Autorización", C.TIPOS_AUTORIZACION)
        vigencia = st.number_input("📅 Vigencia (días)", min_value=7, max_value=90,
                                    value=C.VIGENCIA_AUTORIZACION_DIAS)
        submit = st.form_submit_button("🔑 Generar Número", type="primary")

    if submit:
        if not solicitante or not nombre_proceso:
            st.error("Completa los campos obligatorios.")
        else:
            user = st.session_state.user
            auth_id = sm.get_next_auth_id()
            now = datetime.now()
            venc = (now + timedelta(days=vigencia)).strftime("%Y-%m-%d")

            sm.append_row(C.HOJA_AUTORIZACIONES, [
                auth_id, tipo, solicitante, area, nombre_proceso,
                user.get("Nombre", ""), now.strftime("%Y-%m-%d"), venc,
                "Vigente", "", ""
            ])

            sm.log_action(user["Nombre"], "Generar autorización", "Autorización", auth_id,
                          f"Para {solicitante}: {nombre_proceso}")

            # Find solicitor email and notify
            sol_user = None
            users = sm.get_all_records(C.HOJA_USUARIOS)
            for u in users:
                if u.get("Nombre", "").strip().lower() == solicitante.strip().lower():
                    sol_user = u
                    break
            if sol_user:
                notif.notify_confirmation_number(
                    sol_user["Correo"], solicitante, auth_id, nombre_proceso, venc
                )

            st.success(f"✅ Número de confirmación generado: **{auth_id}**")
            st.markdown(f"""
            <div style="background:#f0f4fa;padding:20px;border-radius:12px;text-align:center;margin:1rem 0;">
                <div style="font-size:2rem;font-weight:800;color:#0D2B6E;">{auth_id}</div>
                <div style="color:#666;margin-top:0.3rem;">Vigente hasta: {venc}</div>
            </div>
            """, unsafe_allow_html=True)

    # List existing authorizations
    st.markdown("### Autorizaciones Emitidas")
    auths = sm.get_all_records(C.HOJA_AUTORIZACIONES)
    if auths:
        for a in reversed(auths):
            est = a.get("Estatus", "")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0;border-bottom:1px solid #eee;">
                <div>
                    <strong>{a.get('ID_Autorizacion','')}</strong> — {a.get('Nombre_Proceso','')}
                    <br><span style="font-size:0.8rem;color:#888;">
                    {a.get('Solicitante','')} · {a.get('Area','')} · {a.get('Tipo','')} · Vence: {a.get('Fecha_Vencimiento','')}</span>
                </div>
                <div>{badge(est)}</div>
            </div>
            """, unsafe_allow_html=True)

            if est == "Vigente":
                if st.button("🚫 Revocar", key=f"rev_{a.get('ID_Autorizacion','')}"):
                    sm.update_cell_by_id(C.HOJA_AUTORIZACIONES, "ID_Autorizacion",
                                         a["ID_Autorizacion"], "Estatus", "Revocada")
                    sm.log_action(st.session_state.user["Nombre"], "Revocar autorización",
                                  "Autorización", a["ID_Autorizacion"], "")
                    st.rerun()


def pm_dashboard():
    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    avances = sm.get_all_records(C.HOJA_AVANCE)
    templates = sm.get_all_records(C.HOJA_PLANTILLAS)

    active = len([i for i in instances if i.get("Estatus") == "En Proceso"])
    completed = len([i for i in instances if i.get("Estatus") == "Completado"])
    total_tpls = len([t for t in templates if t.get("Estatus") == "Activa"])
    overdue = len([a for a in avances if a.get("Estatus") in ["Activa"]
                   and sm.remaining_business_days(a.get("Fecha_Limite", "")) < 0])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card(active, "Procesos Activos"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(completed, "Completados", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card(total_tpls, "Plantillas Activas"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card(overdue, "Act. Vencidas", "red"), unsafe_allow_html=True)

    if instances:
        st.markdown("### Todos los Procesos")
        for inst in instances:
            pct = inst.get("Porcentaje_Avance", 0)
            try:
                pct = int(float(str(pct).replace("%", "")))
            except (ValueError, TypeError):
                pct = 0

            c1, c2, c3 = st.columns([3, 4, 1])
            with c1:
                st.markdown(f"**{inst.get('ID_Instancia','')}** — {inst.get('Nombre_Instancia','')}")
                st.caption(f"Gerente: {inst.get('Gerente_Responsable','')} · {badge(inst.get('Estatus',''))}")
            with c2:
                st.markdown(progress_bar(pct), unsafe_allow_html=True)
            with c3:
                if st.button("Ver", key=f"pm_ver_{inst.get('ID_Instancia','')}"):
                    st.session_state.selected_instance = inst["ID_Instancia"]
                    st.session_state.page = "ver_instancia"
                    st.rerun()
            st.divider()


def pm_usuarios():
    users = sm.get_all_records(C.HOJA_USUARIOS)
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Agregar Usuario")
    with st.form("add_user"):
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Nombre completo")
        correo = c2.text_input("Correo")
        c3, c4 = st.columns(2)
        telefono = c3.text_input("Teléfono")
        area = c4.text_input("Área")
        rol = st.selectbox("Rol", C.ROLES)
        submit = st.form_submit_button("➕ Agregar", type="primary")

    if submit:
        if not nombre or not correo:
            st.error("Nombre y correo son obligatorios.")
        elif not sm.validate_domain(correo):
            st.error("Dominio no autorizado.")
        elif sm.find_user_by_email(correo):
            st.error("El correo ya está registrado.")
        else:
            uid = sm.get_next_id("USR-", C.HOJA_USUARIOS, "ID_Usuario")
            sm.append_row(C.HOJA_USUARIOS, [uid, nombre, correo, telefono, area, rol, "Sí"])
            sm.log_action(st.session_state.user["Nombre"], "Agregar usuario", "Usuario", uid, nombre)
            st.success(f"✅ Usuario {nombre} agregado ({uid}).")
            st.rerun()


# ════════════════════════════════════════════
# PAGE: ADMIN
# ════════════════════════════════════════════
def page_admin():
    st.markdown('<div class="section-title">⚙️ Administración del Sistema</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🗄️ Inicializar BD", "📋 Log del Sistema", "📥 Plantilla Excel Modelo"])

    with tab1:
        st.markdown("Crea todas las hojas necesarias en Google Sheets si no existen.")
        if st.button("🔧 Inicializar Hojas", type="primary"):
            sm.init_spreadsheet()
            st.success("✅ Hojas inicializadas correctamente.")

    with tab2:
        logs = sm.get_all_records(C.HOJA_LOG)
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df.sort_values("Fecha_Hora", ascending=False).head(50),
                         use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros en el log.")

    with tab3:
        st.markdown("Descarga la plantilla Excel modelo para que los gerentes llenen sus procesos.")
        if st.button("📥 Generar Plantilla Modelo"):
            generate_template_excel()


def generate_template_excel():
    output = io.BytesIO()
    data = {
        "No.": [1, 2, 3],
        "Fase": ["Planificación", "Planificación", "Ejecución"],
        "Actividad": ["Actividad ejemplo 1", "Actividad ejemplo 2", "Actividad ejemplo 3"],
        "Responsable": ["Nombre Completo", "Nombre Completo", "Nombre Completo"],
        "Correo": ["correo@imemsa.com.mx", "correo@imemsa.com.mx", "correo@imemsa.com.mx"],
        "Telefono": ["5512345678", "5512345678", "5512345678"],
        "Días teoricos": [3, 5, 2],
        "Descripción": ["Descripción opcional", "", ""],
        "Evidencia requerida": ["Sí", "No", "Sí"],
    }
    df = pd.DataFrame(data)
    df.to_excel(output, index=False, sheet_name="Actividades")
    output.seek(0)
    st.download_button(
        "⬇️ Descargar Plantilla Modelo",
        data=output.getvalue(),
        file_name="Plantilla_Proceso_Transversal_IMEMSA.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ════════════════════════════════════════════
# MAIN ROUTING
# ════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    header()
    navigation()

    page = st.session_state.page
    if page == "inicio":
        page_inicio()
    elif page == "mis_tareas":
        page_mis_tareas()
    elif page == "biblioteca":
        page_biblioteca()
    elif page == "mis_procesos":
        page_mis_procesos()
    elif page == "ver_instancia":
        page_ver_instancia()
    elif page == "pm_panel":
        page_pm_panel()
    elif page == "admin":
        page_admin()
    else:
        page_inicio()


if __name__ == "__main__":
    main()
