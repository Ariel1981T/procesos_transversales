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

from styles import get_css, badge, avatar, metric_card, progress_bar, days_badge, sem_dot



st.set_page_config(
    page_title="IMEMSA · Procesos Transversales",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
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
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@300;400;600;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse 90% 70% at 50% -5%,
            #1a3a8f 0%, #0a1d5e 28%, #020b22 65%) !important;
        min-height: 100vh;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .main .block-container { padding-top: 0 !important; }

    [data-testid="stAppViewContainer"]::before {
        content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
        background: repeating-linear-gradient(
            0deg, transparent, transparent 3px,
            rgba(0,0,0,0.07) 3px, rgba(0,0,0,0.07) 4px);
    }

    [data-testid="stAppViewContainer"] [data-testid="stVerticalBlock"],
    [data-testid="stAppViewContainer"] [data-testid="column"] > div:first-child,
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: transparent !important; border: none !important; box-shadow: none !important;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] label p,
    [data-testid="stTextInput"] label span,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 13px !important; letter-spacing: 3px !important;
        text-transform: uppercase !important;
    }

    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.93) !important;
        border: none !important; border-radius: 7px !important;
        color: #1a2a5e !important;
        font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important;
        transition: box-shadow 0.25s !important;
    }
    [data-testid="stTextInput"] input:focus { box-shadow: 0 0 0 2px #C41E2E !important; }
    [data-testid="stTextInput"] input::placeholder { color: #8899bb !important; }

    [data-testid="stForm"] {
        background: rgba(13,43,110,0.45) !important;
        border: 1px solid rgba(100,150,255,0.18) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        backdrop-filter: blur(10px) !important;
    }

    [data-testid="stFormSubmitButton"] button {
        width: 100% !important;
        background: linear-gradient(135deg, #d42030 0%, #a8151f 100%) !important;
        border: none !important; border-radius: 8px !important; color: #ffffff !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 20px !important; letter-spacing: 5px !important; padding: 13px !important;
        box-shadow: 0 4px 20px rgba(196,30,46,0.55) !important; transition: all 0.25s !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 28px rgba(196,30,46,0.7) !important;
    }

    [data-testid="stAlert"] {
        background: rgba(196,30,46,0.12) !important;
        border: 1px solid rgba(196,30,46,0.35) !important;
        border-radius: 8px !important; color: #f07080 !important;
    }

    .corner-tl, .corner-tr, .corner-bl, .corner-br {
        position: fixed; width: 40px; height: 40px; z-index: 100; pointer-events: none;
    }
    .corner-tl { top:16px; left:16px;  border-top:2px solid #C41E2E; border-left:2px solid #C41E2E; }
    .corner-tr { top:16px; right:16px; border-top:2px solid #C41E2E; border-right:2px solid #C41E2E; }
    .corner-bl { bottom:16px; left:16px;  border-bottom:2px solid #C41E2E; border-left:2px solid #C41E2E; }
    .corner-br { bottom:16px; right:16px; border-bottom:2px solid #C41E2E; border-right:2px solid #C41E2E; }

    @keyframes rise-bubble {
        0%   { transform: translateY(0); opacity: 0.65; }
        80%  { opacity: 0.15; }
        100% { transform: translateY(-105vh); opacity: 0; }
    }
    .bbl {
        position: fixed; border-radius: 50%;
        background: rgba(180,210,255,0.20); border: 1px solid rgba(180,210,255,0.32);
        animation: rise-bubble linear infinite; pointer-events: none; z-index: 1; bottom: -20px;
    }
    </style>

    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="bbl" style="width:5px;height:5px;left:4%;animation-duration:9s;animation-delay:-2s;"></div>
    <div class="bbl" style="width:8px;height:8px;left:10%;animation-duration:14s;animation-delay:-7s;"></div>
    <div class="bbl" style="width:4px;height:4px;left:17%;animation-duration:11s;animation-delay:-1s;"></div>
    <div class="bbl" style="width:10px;height:10px;left:24%;animation-duration:16s;animation-delay:-11s;"></div>
    <div class="bbl" style="width:5px;height:5px;left:31%;animation-duration:8s;animation-delay:-4s;"></div>
    <div class="bbl" style="width:7px;height:7px;left:38%;animation-duration:13s;animation-delay:-9s;"></div>
    <div class="bbl" style="width:3px;height:3px;left:45%;animation-duration:10s;animation-delay:-0s;"></div>
    <div class="bbl" style="width:9px;height:9px;left:52%;animation-duration:17s;animation-delay:-6s;"></div>
    <div class="bbl" style="width:4px;height:4px;left:59%;animation-duration:12s;animation-delay:-13s;"></div>
    <div class="bbl" style="width:6px;height:6px;left:66%;animation-duration:9s;animation-delay:-3s;"></div>
    <div class="bbl" style="width:11px;height:11px;left:72%;animation-duration:15s;animation-delay:-8s;"></div>
    <div class="bbl" style="width:4px;height:4px;left:79%;animation-duration:11s;animation-delay:-5s;"></div>
    <div class="bbl" style="width:7px;height:7px;left:85%;animation-duration:13s;animation-delay:-10s;"></div>
    <div class="bbl" style="width:5px;height:5px;left:91%;animation-duration:8s;animation-delay:-15s;"></div>
    <div class="bbl" style="width:9px;height:9px;left:97%;animation-duration:16s;animation-delay:-2s;"></div>
    <div class="bbl" style="width:3px;height:3px;left:13%;animation-duration:10s;animation-delay:-18s;"></div>
    <div class="bbl" style="width:6px;height:6px;left:55%;animation-duration:12s;animation-delay:-16s;"></div>
    <div class="bbl" style="width:8px;height:8px;left:42%;animation-duration:7s;animation-delay:-12s;"></div>

    <div style="position:fixed;bottom:18px;right:22px;z-index:100;
        font-size:9px;letter-spacing:3px;color:rgba(200,216,240,0.3);
        text-transform:uppercase;font-family:'Rajdhani',sans-serif;">
        Sistema v1.0 · 2026</div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:5vh'></div>", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("""
        <div style="background:rgba(13,43,110,0.60);border:1px solid rgba(100,150,255,0.20);
            border-radius:12px;padding:22px 24px 18px;text-align:center;
            backdrop-filter:blur(8px);margin-bottom:20px;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:46px;letter-spacing:6px;
                color:#ffffff;text-shadow:0 0 30px rgba(100,150,255,0.5);line-height:1;">IMEMSA</div>
            <div style="width:200px;height:2px;margin:10px auto;
                background:linear-gradient(to right,transparent,#C41E2E 30%,#C41E2E 70%,transparent);
                box-shadow:0 0 10px rgba(196,30,46,0.55);"></div>
            <div style="font-size:11px;letter-spacing:6px;color:#c8d8f0;opacity:0.7;
                text-transform:uppercase;font-family:'Rajdhani',sans-serif;">Procesos Transversales</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="text-align:center;margin-bottom:18px;font-size:14px;letter-spacing:1px;
            color:#c8d8f0;line-height:1.6;font-family:'Rajdhani',sans-serif;">
            Sistema de Seguimiento ·
            <span style="color:#ffffff;font-weight:600;">Procesos Transversales</span><br>
            Grupo IMEMSA
        </p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("📧  Correo Institucional", placeholder="tucorreo@imemsa.com.mx")
            password = st.text_input("🔒  Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar al Sistema",
                                              use_container_width=True, type="primary")

        if submitted:
            if not email:
                st.error("Ingresa tu correo electrónico.")
                return
            if not password:
                st.error("Ingresa tu contraseña.")
                return
            if not sm.validate_domain(email):
                st.error(f"Dominio no autorizado.")
                return
            user = sm.find_user_by_email(email)
            if not user:
                st.error("Correo no registrado en el sistema.")
                return
            if str(user.get("Activo", "Sí")).strip().lower() in ["no", "false", "0"]:
                st.error("Tu cuenta está desactivada.")
                return
            if user.get("Password", "") != password:
                st.error("Contraseña incorrecta.")
                return
            st.session_state.logged_in = True
            st.session_state.user = user
            sm.log_action(user["Nombre"], "Login", "Sistema", "", f"Acceso desde {email}")
            st.rerun()

        st.markdown(
            '<p style="text-align:center;color:rgba(255,255,255,.30);font-size:.72rem;'
            'margin-top:20px;font-family:\'Rajdhani\',sans-serif;">'
            '© 2026 IMEMSA — Uso interno. Acceso restringido.</p>',
            unsafe_allow_html=True,
        )


def header():
    user = st.session_state.user
    nombre = user.get('Nombre', '')
    rol = user.get('Rol', '')
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
        <div>
            <span class="section-header" style="border-bottom:none;margin-bottom:0;">
                📋 Procesos Transversales
            </span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
            {avatar(nombre)}
            <div>
                <div style="font-weight:700;color:#0D2B6E;font-size:.95rem;">{nombre}</div>
                <div style="font-size:.75rem;color:#8592A3;">{rol}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def navigation():
    user = st.session_state.user
    rol = user.get("Rol", "Responsable")

    with st.sidebar:
        st.markdown(
            '<div style="padding:16px 16px 10px 16px;text-align:center;">'
            '<div style="font-family:Barlow Condensed,sans-serif;font-size:1.8rem;'
            'font-weight:800;color:#fff;letter-spacing:1px;">IMEMSA</div>'
            '<div style="font-family:Source Sans 3,sans-serif;font-size:.7rem;'
            'font-weight:600;color:#8EA8D8;letter-spacing:2.5px;margin-top:2px;">'
            'PROCESOS TRANSVERSALES</div>'
            '<div style="height:2px;background:#C41E2E;border-radius:1px;margin-top:10px;"></div>'
            '</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if st.button("🏠  Inicio", use_container_width=True, key="nav_inicio"):
            st.session_state.page = "inicio"
            st.session_state.selected_instance = None
            st.rerun()

        if st.button("📥  Mis Tareas", use_container_width=True, key="nav_mis_tareas"):
            st.session_state.page = "mis_tareas"
            st.rerun()

        if st.button("📅  Calendario", use_container_width=True, key="nav_calendario"):
            st.session_state.page = "calendario"
            st.rerun()

        if rol in ["Gerente", "PM", "Admin"]:
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.7rem;font-weight:600;letter-spacing:1.5px;'
                        'color:#8EA8D8;padding:0 12px;">GESTIÓN</div>', unsafe_allow_html=True)

            if st.button("📚  Biblioteca", use_container_width=True, key="nav_biblioteca"):
                st.session_state.page = "biblioteca"
                st.rerun()
            if st.button("📊  Mis Procesos", use_container_width=True, key="nav_mis_procesos"):
                st.session_state.page = "mis_procesos"
                st.rerun()

        if rol in ["PM", "Admin"]:
            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.7rem;font-weight:600;letter-spacing:1.5px;'
                        'color:#8EA8D8;padding:0 12px;">ADMINISTRACIÓN</div>', unsafe_allow_html=True)

            if st.button("👔  Panel PM", use_container_width=True, key="nav_pm_panel"):
                st.session_state.page = "pm_panel"
                st.rerun()

        if rol == "Admin":
            if st.button("⚙️  Admin", use_container_width=True, key="nav_admin"):
                st.session_state.page = "admin"
                st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if st.button("🔑  Cambiar Contraseña", use_container_width=True, key="nav_pwd"):
            st.session_state.page = "cambiar_pwd"
            st.rerun()

        if st.button("🚪  Cerrar Sesión", use_container_width=True, key="nav_salir"):
            for k in DEFAULTS:
                st.session_state[k] = DEFAULTS[k]
            st.rerun()


# ════════════════════════════════════════════
# PAGE: INICIO / DASHBOARD
# ════════════════════════════════════════════
def page_inicio():
    user = st.session_state.user
    rol = user.get("Rol", "Responsable")
    email = user.get("Correo", "").strip().lower()
    st.markdown('<div class="section-header">📊 Dashboard General</div>', unsafe_allow_html=True)

    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    avances = sm.get_all_records(C.HOJA_AVANCE)

    # Filter: Responsables only see processes where they have tasks
    if rol == "Responsable":
        my_inst_ids = set(a.get("ID_Instancia") for a in avances
                          if a.get("Correo", "").strip().lower() == email)
        instances = [i for i in instances if i.get("ID_Instancia") in my_inst_ids]
        avances = [a for a in avances if a.get("ID_Instancia") in my_inst_ids]
    elif rol == "Gerente":
        instances = [i for i in instances if i.get("Gerente_Responsable") == user.get("Nombre")]
        inst_ids = set(i.get("ID_Instancia") for i in instances)
        avances = [a for a in avances if a.get("ID_Instancia") in inst_ids]

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
        st.markdown('<div class="section-header">📋 Procesos Activos</div>', unsafe_allow_html=True)
        for inst in active:
            pct = inst.get("Porcentaje_Avance", 0)
            try:
                pct = int(float(str(pct).replace("%", "")))
            except (ValueError, TypeError):
                pct = 0
            folio = inst.get("ID_Instancia", "")
            nombre = inst.get("Nombre_Instancia", "")

            # Find active activity for this instance
            inst_avs = [a for a in avances if a.get("ID_Instancia") == folio
                        and a.get("Estatus") in ["Activa", "Vencida"]]
            active_act = inst_avs[0] if inst_avs else None

            if active_act:
                remaining = sm.remaining_business_days(active_act.get("Fecha_Limite", ""))
                if remaining < 0:
                    sem = "red"
                    days_html = days_badge(remaining)
                elif remaining <= C.DIAS_ALERTA_AMARILLA:
                    sem = "yellow"
                    days_html = days_badge(remaining)
                else:
                    sem = "green"
                    days_html = days_badge(remaining)
                act_info = (
                    f'{sem_dot(sem)} '
                    f'Actividad activa: <strong>{active_act.get("Actividad","")}</strong>'
                    f' &nbsp;·&nbsp; Resp: {avatar(active_act.get("Responsable",""), 28)}'
                    f'<span style="font-size:.82rem;">{active_act.get("Responsable","")}</span>'
                    f' &nbsp;{days_html}'
                )
            else:
                act_info = '<span style="color:var(--color-text-tertiary);">Sin actividad activa</span>'

            st.markdown(
                f'<div class="process-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                f'  <div>'
                f'    <div class="process-folio">{folio}</div>'
                f'    <div class="process-desc">{nombre}</div>'
                f'  </div>'
                f'  <div style="text-align:right;">'
                f'    {badge(inst.get("Estatus","En Proceso"))}'
                f'    <div style="font-size:.78rem;color:#8592A3;margin-top:4px;">'
                f'    Creado: {inst.get("Fecha_Creacion","")}</div>'
                f'  </div>'
                f'</div>'
                f'<div style="margin-top:10px;">{progress_bar(pct)}</div>'
                f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px;font-size:.82rem;color:#4B5563;">'
                f'  {act_info}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("Ver actividades →", key=f"ver_{folio}", use_container_width=False):
                st.session_state.selected_instance = folio
                st.session_state.page = "ver_instancia"
                st.rerun()


# ════════════════════════════════════════════
# PAGE: MIS TAREAS (Bandeja del Responsable)
# ════════════════════════════════════════════
def page_mis_tareas():
    user = st.session_state.user
    email = user.get("Correo", "").strip().lower()
    st.markdown('<div class="section-header">📥 Mis Tareas Pendientes</div>', unsafe_allow_html=True)

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
        upload_key = f"ev_{inst_id}_{task.get('Numero_Actividad','')}"
        uploaded_flag = f"uploaded_{inst_id}_{task.get('Numero_Actividad','')}"

        with col1:
            uploaded = st.file_uploader("📎 Subir evidencia", key=upload_key)
            if uploaded and not st.session_state.get(uploaded_flag):
                if st.button("📤 Confirmar subida", key=f"btn_ev_{inst_id}_{task.get('Numero_Actividad','')}",
                             type="primary"):
                    try:
                        import unicodedata, re, os
                        original_name = uploaded.name
                        name_part, ext_part = os.path.splitext(original_name)
                        clean_name = unicodedata.normalize('NFKD', name_part).encode('ascii', 'ignore').decode('ascii')
                        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', clean_name)
                        ts = datetime.now().strftime('%Y%m%d%H%M%S')
                        safe_filename = f"{ts}_{clean_name}{ext_part.lower()}"
                        storage_path = f"{inst_id}/{safe_filename}"

                        sb = sm.get_client()
                        file_bytes = uploaded.getvalue()
                        sb.storage.from_('evidencias').upload(
                            storage_path, file_bytes,
                            {"content-type": uploaded.type or "application/octet-stream"}
                        )
                        public_url = sb.storage.from_('evidencias').get_public_url(storage_path)

                        ev_id = f"EV-{ts}"
                        sm.append_row(C.HOJA_EVIDENCIAS, [
                            ev_id, inst_id, task.get("Numero_Actividad", ""),
                            original_name, public_url, storage_path,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user.get("Nombre", "")
                        ])
                        sm.update_row_by_id(C.HOJA_AVANCE, "ID_Avance", task.get("ID_Avance", ""),
                                            {"Tiene_Evidencia": "Sí"})
                        sm.log_action(user["Nombre"], "Subir evidencia", "Actividad",
                                      task.get("ID_Avance", ""), uploaded.name)
                        st.session_state[uploaded_flag] = True
                        st.success(f"✅ Evidencia '{uploaded.name}' subida correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al subir evidencia: {e}")
            elif st.session_state.get(uploaded_flag):
                st.success("✅ Evidencia subida")
                has_evidence = True

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

    # Find manager email for notifications
    gerente_nombre = inst.get("Gerente_Responsable", "")
    gerente_user = None
    all_users = sm.get_all_records(C.HOJA_USUARIOS)
    for u in all_users:
        if u.get("Nombre", "") == gerente_nombre:
            gerente_user = u
            break
    gerente_email = gerente_user.get("Correo", "") if gerente_user else ""

    # Notify manager
    if gerente_email:
        notif.notify_task_completed(
            gerente_email, gerente_nombre,
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

    # Update instance progress - re-read fresh from DB
    fresh_avances = sm.get_all_records(C.HOJA_AVANCE)
    fresh_inst_avances = [a for a in fresh_avances if a["ID_Instancia"] == inst_id]
    total = len(fresh_inst_avances)
    completed = len([a for a in fresh_inst_avances if a.get("Estatus") == "Completada"])
    pct = int((completed / total) * 100) if total > 0 else 0

    updates = {"Porcentaje_Avance": pct}
    if completed >= total:
        updates["Estatus"] = "Completado"
        updates["Fecha_Real_Fin"] = fecha_cierre
        if gerente_email:
            notif.notify_process_completed(
                gerente_email, gerente_nombre,
                inst.get("Nombre_Instancia", ""), inst_id
            )
    sm.update_row_by_id(C.HOJA_INSTANCIAS, "ID_Instancia", inst_id, updates)

    st.success("✅ Actividad completada exitosamente.")
    st.rerun()


# ════════════════════════════════════════════
# PAGE: BIBLIOTECA DE PLANTILLAS
# ════════════════════════════════════════════
def page_biblioteca():
    st.markdown('<div class="section-header">📚 Biblioteca de Plantillas</div>', unsafe_allow_html=True)

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
                if st.button("🚣 Navegar", key=f"launch_{tpl.get('ID_Plantilla', '')}"):
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
    st.markdown('<div class="section-header">📤 Crear Nueva Plantilla</div>', unsafe_allow_html=True)

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
            notif.notify_welcome(nu["Correo"], nu["Nombre"], nombre, first_act, nu.get("Password", ""))

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

    st.markdown(f'<div class="section-header">🚣 Navegar en la Instancia de: {tpl.get("Nombre", "")}</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
        📋 <strong>Plantilla:</strong> {tpl.get('Nombre', '')} (v{tpl.get('Version', 1)})<br>
        🔢 <strong>Actividades:</strong> {tpl.get('Num_Actividades', 0)} &nbsp;|&nbsp;
        📅 <strong>Días teóricos:</strong> {tpl.get('Dias_Teoricos_Total', 0)} &nbsp;|&nbsp;
        🏢 <strong>Área:</strong> {tpl.get('Area_Origen', '')} &nbsp;|&nbsp;
        🔄 <strong>Usos anteriores:</strong> {tpl.get('Veces_Utilizada', 0)}
    </div>
    """, unsafe_allow_html=True)

    # Load template activities
    all_acts = sm.get_all_records(C.HOJA_ACTIVIDADES_PLANTILLA)
    tpl_acts = [a for a in all_acts if a["ID_Plantilla"] == tpl_id]
    tpl_acts.sort(key=lambda x: int(x.get("Numero", 0)))

    if not tpl_acts:
        st.error("La plantilla no tiene actividades definidas.")
        return

    st.markdown("""
    <div class="warning-box">
        👥 <strong>Revisa y ajusta los responsables.</strong> Los campos de Actividad, Fase, Días y Descripción
        no se pueden modificar. Puedes cambiar el <strong>Responsable, Correo y Teléfono</strong> de cada actividad
        si necesitas asignar personas diferentes para esta ejecución.<br><br>
        ⏱ Al dar clic en <em>Confirmar y Lanzar</em>, el sistema activará la primera actividad
        y comenzará a contabilizar los días hábiles.
    </div>
    """, unsafe_allow_html=True)

    with st.form("launch_with_responsables"):
        edited_acts = []
        for act in tpl_acts:
            num = int(act.get("Numero", 0))
            ev_req = str(act.get("Evidencia_Requerida", "")).lower() in ["sí", "si", "yes", "true", "1"]
            st.markdown(
                f'<div class="act-row act-row-pendiente" style="margin-bottom:4px;">'
                f'<div style="display:flex;align-items:center;gap:8px;">'
                f'<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:.85rem;'
                f'font-weight:700;color:#8592A3;min-width:22px;">{num:02d}</span>'
                f'<div>'
                f'<div class="act-name">{act.get("Actividad", "")}</div>'
                f'<div class="act-meta">{act.get("Fase", "")} · {act.get("Dias_Teoricos", "")} días hábiles'
                f'{"  ·  📎 Evidencia requerida" if ev_req else ""}'
                f'</div></div></div></div>',
                unsafe_allow_html=True,
            )
            c1, c2, c3 = st.columns(3)
            resp = c1.text_input("Responsable", value=act.get("Responsable", ""),
                                  key=f"resp_{tpl_id}_{num}")
            correo = c2.text_input("Correo", value=act.get("Correo", ""),
                                    key=f"correo_{tpl_id}_{num}")
            tel = c3.text_input("Teléfono", value=str(act.get("Telefono", "")),
                                 key=f"tel_{tpl_id}_{num}")
            edited_acts.append({
                **act,
                "Responsable": resp,
                "Correo": correo,
                "Telefono": tel,
            })
            st.markdown("---")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("🚣 Confirmar y Navegar", type="primary",
                                          use_container_width=True)
        cancel = col2.form_submit_button("❌ Cancelar", use_container_width=True)

    if cancel:
        st.session_state.show_launch = False
        st.session_state.selected_template = None
        st.rerun()

    if submit:
        # Validate emails
        errors = []
        for ea in edited_acts:
            if not ea.get("Responsable", "").strip():
                errors.append(f"Act {ea.get('Numero','')}: Responsable vacío")
            if "@" not in str(ea.get("Correo", "")):
                errors.append(f"Act {ea.get('Numero','')}: Correo inválido")
            elif not sm.validate_domain(ea.get("Correo", "")):
                errors.append(f"Act {ea.get('Numero','')}: Dominio no autorizado ({ea.get('Correo','')})")
        if errors:
            st.error("❌ Errores:\n" + "\n".join(errors[:10]))
            return

        # Auto-register new users
        df_users = pd.DataFrame(edited_acts)
        new_users, _ = sm.auto_register_users(df_users)
        if new_users:
            st.info(f"👥 {len(new_users)} usuario(s) nuevo(s) registrado(s).")

        # Create instance
        user = st.session_state.user
        inst_id = sm.get_next_instance_id()
        now = datetime.now()
        dias_total = int(tpl.get("Dias_Teoricos_Total", 0))
        fecha_est_fin = sm.add_business_days(now.date(), dias_total).strftime("%Y-%m-%d")
        nombre_inst = tpl.get("Nombre", "")

        sm.append_row(C.HOJA_INSTANCIAS, [
            inst_id, tpl_id, nombre_inst, "", user.get("Nombre", ""),
            now.strftime("%Y-%m-%d"), fecha_est_fin, "", "En Proceso", 0,
            tpl.get("ID_Autorizacion", "Plantilla aprobada"), "", ""
        ])

        # Create avance records with edited responsables
        for act in edited_acts:
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
        first = edited_acts[0]
        dias_first = int(first.get("Dias_Teoricos", 1))
        f_limite_first = sm.add_business_days(now.date(), dias_first).strftime("%Y-%m-%d")
        notif.notify_task_activated(
            first.get("Correo", ""), first.get("Responsable", ""),
            nombre_inst, first.get("Actividad", ""), dias_first, f_limite_first
        )

        # Send welcome to new users
        for nu in new_users:
            first_act = edited_acts[0].get("Actividad", "") if edited_acts else ""
            notif.notify_welcome(nu["Correo"], nu["Nombre"], nombre_inst,
                                  first_act, nu.get("Password", ""))

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
    st.markdown('<div class="section-header">📊 Mis Procesos</div>', unsafe_allow_html=True)

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

    user = st.session_state.user
    rol = user.get("Rol", "Responsable")
    email = user.get("Correo", "").strip().lower()
    if rol == "Responsable":
        my_tasks_here = [a for a in inst_avances if a.get("Correo", "").strip().lower() == email]
        if not my_tasks_here:
            st.error("No tienes acceso a este proceso.")
            return

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
    total = len(inst_avances)
    completed_count = len([a for a in inst_avances if a.get("Estatus") == "Completada"])
    overdue_count = len([a for a in inst_avances if a.get("Estatus") == "Activa"
                         and sm.remaining_business_days(a.get("Fecha_Limite", "")) < 0])
    at_risk_count = len([a for a in inst_avances if a.get("Estatus") == "Activa"
                         and 0 <= sm.remaining_business_days(a.get("Fecha_Limite", "")) <= C.DIAS_ALERTA_AMARILLA])
    on_time_count = len([a for a in inst_avances if a.get("Estatus") == "Activa"
                         and sm.remaining_business_days(a.get("Fecha_Limite", "")) > C.DIAS_ALERTA_AMARILLA])

    # Back button
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Regresar", use_container_width=True):
            st.session_state.selected_instance = None
            st.session_state.page = "mis_procesos"
            st.rerun()

    # ── Instance Header Card (Motores style) ──
    st.markdown(
        f'<div style="background:#fff;border-radius:12px;padding:20px 24px;'
        f'margin-bottom:18px;box-shadow:0 1px 6px rgba(13,43,110,.10);border-top:4px solid #0D2B6E;">'
        f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">'
        f'<div>'
        f'  <div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.5rem;font-weight:800;color:#0D2B6E;">'
        f'  📋 {inst_id}</div>'
        f'  <div style="font-size:.85rem;color:#4B5563;margin-top:3px;">'
        f'  {inst.get("Nombre_Instancia", "")} {" · " + inst.get("Descripcion", "") if inst.get("Descripcion") else ""}</div>'
        f'</div>'
        f'<div style="text-align:right;">{badge(estatus)}'
        f'  <div style="font-size:.78rem;color:#8592A3;margin-top:4px;">Creado: {inst.get("Fecha_Creacion","")}</div>'
        f'</div></div>'
        f'<div style="margin-top:14px;">{progress_bar(pct)}</div>'
        f'<div style="margin-top:6px;font-size:.82rem;color:#4B5563;">'
        f'  🏭 Proceso iniciado por <strong>{inst.get("Gerente_Responsable","")}</strong>'
        f'  el <strong>{inst.get("Fecha_Creacion","")}</strong></div>'
        f'<div style="margin-top:8px;display:flex;gap:14px;flex-wrap:wrap;">'
        f'  {sem_dot("green")}<span style="font-size:.8rem;">{on_time_count} en tiempo</span>'
        f'  {sem_dot("yellow")}<span style="font-size:.8rem;">{at_risk_count} en riesgo</span>'
        f'  {sem_dot("red")}<span style="font-size:.8rem;">{overdue_count} vencidas</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Export button
    col_exp, _ = st.columns([1, 4])
    with col_exp:
        if st.button("⬇️  Exportar a Excel", use_container_width=True):
            export_instance_to_excel(inst, inst_avances, inst_evidencias, inst_comentarios)

    st.markdown(f'<div class="section-header">🔢 Actividades del Proceso ({total})</div>',
                unsafe_allow_html=True)

    # ── Activities grouped by phase ──
    current_phase = ""
    for act in inst_avances:
        phase = act.get("Fase", "")
        if phase != current_phase:
            current_phase = phase
            phase_acts = [a for a in inst_avances if a.get("Fase") == phase]
            phase_done = len([a for a in phase_acts if a.get("Estatus") == "Completada"])
            st.markdown(
                f'<div style="margin:18px 0 8px;display:flex;align-items:center;gap:8px;">'
                f'<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.1rem;'
                f'font-weight:700;color:#0D2B6E;">{phase}</span>'
                f'<span style="font-size:.72rem;color:#8592A3;">({phase_done}/{len(phase_acts)} completadas)</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        _render_activity_row(act, inst, inst_evidencias, inst_comentarios, user)


def _render_activity_row(act, inst, inst_evidencias, inst_comentarios, user):
    """Render a single activity row with Motores-style design."""
    inst_id = inst.get("ID_Instancia", "")
    estatus_act = act.get("Estatus", "Pendiente")
    remaining = sm.remaining_business_days(act.get("Fecha_Limite", "")) if act.get("Fecha_Limite") else None
    act_num = act.get("Numero_Actividad", "")
    responsable = act.get("Responsable", "")

    # Determine row class and semaphore
    if estatus_act == "Completada":
        row_cls = "act-row-completada"
        sem = "green"
        status_label = "✅ Completada"
    elif estatus_act == "Activa" and remaining is not None and remaining < 0:
        row_cls = "act-row-vencida"
        sem = "red"
        status_label = "Vencida"
    elif estatus_act == "Activa" and remaining is not None and remaining <= C.DIAS_ALERTA_AMARILLA:
        row_cls = "act-row-en-riesgo"
        sem = "yellow"
        status_label = "En Riesgo"
    elif estatus_act == "Activa":
        row_cls = "act-row-activa"
        sem = "green"
        status_label = "En Proceso"
    else:
        row_cls = "act-row-pendiente"
        sem = "gray"
        status_label = "Pendiente"

    days_html = days_badge(remaining) if estatus_act in ("Activa",) else ""

    # Dates
    dates_parts = []
    dates_parts.append(f"Plazo: {act.get('Dias_Teoricos', '')} días hábiles")
    if act.get("Fecha_Inicio"):
        dates_parts.append(f"Inicio: {act['Fecha_Inicio']}")
    if act.get("Fecha_Limite"):
        dates_parts.append(f"Límite: {act['Fecha_Limite']}")
    if act.get("Fecha_Cierre"):
        dates_parts.append(f"Cierre: {act['Fecha_Cierre']}")

    # Evidence indicator
    act_evidencias = [e for e in inst_evidencias
                      if str(e.get("Numero_Actividad")) == str(act_num)]
    ev_line = ""
    if act_evidencias:
        ev_names = ", ".join([e.get("Nombre_Archivo", "") for e in act_evidencias])
        ev_line = f'<div style="margin-top:4px;font-size:.75rem;color:#6B7280;">📎 Evidencia: {ev_names}</div>'

    st.markdown(
        f'<div class="act-row {row_cls}">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;">'
        f'  <div style="display:flex;align-items:center;gap:8px;">'
        f'    <span style="font-family:\'Barlow Condensed\',sans-serif;font-size:.85rem;'
        f'    font-weight:700;color:#8592A3;min-width:22px;">{int(act_num):02d}</span>'
        f'    {sem_dot(sem)}'
        f'    <div><div class="act-name">{act.get("Actividad", "")}</div></div>'
        f'  </div>'
        f'  <div style="text-align:right;">'
        f'    <span style="font-size:.75rem;padding:3px 10px;border-radius:20px;'
        f'    background:#F3F4F6;color:#374151;font-weight:600;">{status_label}</span>'
        f'    <div class="act-meta" style="margin-top:4px;">'
        f'    Resp: {avatar(responsable, 32)}'
        f'    {responsable}</div>'
        f'  </div>'
        f'</div>'
        f'<div class="act-meta" style="margin-top:6px;">'
        f'  {"  ·  ".join(dates_parts)}  {days_html}'
        f'</div>'
        f'{ev_line}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Evidence Expander ──
    ev_label = f"📸  Evidencias  ({len(act_evidencias)})" if act_evidencias else "📸  Evidencias"
    with st.expander(ev_label, expanded=False):
        if act_evidencias:
            for ev in act_evidencias:
                url = ev.get("URL_Cloudinary", "")
                name = ev.get("Nombre_Archivo", "archivo")
                subido = ev.get("Subido_Por", "")
                fecha = ev.get("Fecha_Subida", "")
                # Append download parameter for Supabase Storage
                dl_url = f"{url}?download={name}" if "supabase" in url else url
                col_info, col_btn = st.columns([3, 1])
                with col_info:
                    st.markdown(
                        f'<div style="padding:6px 10px;border-left:3px solid #0D2B6E;'
                        f'background:#F8FAFF;border-radius:0 6px 6px 0;">'
                        f'<span style="font-size:.85rem;font-weight:600;color:#0D2B6E;">📄 {name}</span>'
                        f'<br><span style="font-size:.72rem;color:#6B7280;">'
                        f'Subido por {subido} · {fecha}</span></div>',
                        unsafe_allow_html=True,
                    )
                with col_btn:
                    st.link_button("⬇️ Descargar", dl_url, use_container_width=True)
        else:
            st.caption("Sin evidencias adjuntas.")

    # ── Comments Expander ──
    act_comments = [c for c in inst_comentarios
                    if str(c.get("Numero_Actividad")) == str(act_num)]
    com_label = f"💬  Comentarios  ({len(act_comments)})" if act_comments else "💬  Agregar comentario"
    with st.expander(com_label, expanded=False):
        for cm in act_comments:
            st.markdown(
                f'<div style="padding:6px 10px;border-left:3px solid #C41E2E;'
                f'margin-bottom:6px;background:#FFF8F8;border-radius:0 6px 6px 0;">'
                f'<span style="font-size:.72rem;color:#6B7280;">{cm.get("Fecha","")}</span>  '
                f'<strong style="font-size:.80rem;color:#C41E2E;">{cm.get("Autor","")}</strong><br>'
                f'<span style="font-size:.82rem;color:#374151;">{cm.get("Texto","")}</span></div>',
                unsafe_allow_html=True,
            )
        with st.form(f"comment_form_{inst_id}_{act_num}"):
            new_comment = st.text_area("Nuevo comentario", height=70, label_visibility="collapsed",
                                       placeholder="Escribe un comentario sobre esta actividad…")
            if st.form_submit_button("➕  Agregar comentario", use_container_width=True):
                if new_comment.strip():
                    com_id = f"COM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{act_num}"
                    sm.append_row(C.HOJA_COMENTARIOS, [
                        com_id, inst_id, act_num, user.get("Nombre", ""),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_comment.strip()
                    ])
                    sm.log_action(user["Nombre"], "Comentario", "Actividad",
                                  act.get("ID_Avance", ""), new_comment.strip()[:80])
                    st.success("💬 Comentario agregado.")
                    st.rerun()
                else:
                    st.warning("El comentario no puede estar vacío.")


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
    st.markdown('<div class="section-header">👔 Panel del Project Manager</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔑 Autorizaciones", "📊 Dashboard Global", "👥 Usuarios", "📥 Plantilla Excel"])

    with tab1:
        pm_autorizaciones()
    with tab2:
        pm_dashboard()
    with tab3:
        pm_usuarios()
    with tab4:
        st.markdown("Descarga la plantilla Excel modelo para que los gerentes llenen sus procesos.")
        if st.button("📥 Generar Plantilla Modelo", key="pm_gen_tpl"):
            generate_template_excel()


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
            pwd = sm.generate_password()
            sm.append_row(C.HOJA_USUARIOS, [uid, nombre, correo, telefono, area, rol, "Sí", pwd])
            sm.log_action(st.session_state.user["Nombre"], "Agregar usuario", "Usuario", uid, nombre)
            st.success(f"✅ Usuario {nombre} agregado ({uid}).")
            st.markdown(f"""
            <div class="info-box">
                🔑 <strong>Contraseña generada:</strong> <code>{pwd}</code><br>
                📧 <strong>Correo:</strong> {correo}<br>
                <em>Comparte esta contraseña al usuario de forma segura.</em>
            </div>
            """, unsafe_allow_html=True)

    # Reset password section
    st.markdown("### 🔄 Restablecer Contraseña")
    with st.form("reset_pwd"):
        reset_email = st.text_input("Correo del usuario")
        reset_submit = st.form_submit_button("🔄 Generar nueva contraseña")

    if reset_submit and reset_email:
        target_user = sm.find_user_by_email(reset_email)
        if not target_user:
            st.error("Correo no encontrado.")
        else:
            new_pwd = sm.generate_password()
            sm.update_cell_by_id(C.HOJA_USUARIOS, "ID_Usuario",
                                  target_user["ID_Usuario"], "Password", new_pwd)
            sm.log_action(st.session_state.user["Nombre"], "Reset contraseña",
                          "Usuario", target_user["ID_Usuario"], reset_email)
            st.success(f"✅ Nueva contraseña generada para {target_user.get('Nombre', '')}.")
            st.markdown(f"""
            <div class="info-box">
                🔑 <strong>Nueva contraseña:</strong> <code>{new_pwd}</code><br>
                <em>Comparte esta contraseña al usuario de forma segura.</em>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# PAGE: ADMIN
# ════════════════════════════════════════════
def page_admin():
    st.markdown('<div class="section-header">⚙️ Administración del Sistema</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Log del Sistema", "📥 Plantilla Excel", "📧 Prueba de Correo"])

    with tab1:
        logs = sm.get_all_records(C.HOJA_LOG)
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df.sort_values("Fecha_Hora", ascending=False).head(50),
                         use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros en el log.")

    with tab2:
        st.markdown("Descarga la plantilla Excel modelo para que los gerentes llenen sus procesos.")
        if st.button("📥 Generar Plantilla Modelo"):
            generate_template_excel()

    with tab3:
        st.markdown("Envía un correo de prueba para verificar que el motor de notificaciones funciona correctamente.")
        with st.form("test_email_form"):
            test_to = st.text_input("📧 Correo destino", value=st.session_state.user.get("Correo", ""))
            test_submit = st.form_submit_button("📧 Enviar correo de prueba", type="primary")
        if test_submit and test_to:
            result = notif.test_email(test_to)
            if result:
                st.success(f"✅ Correo de prueba enviado a {test_to}.")
            else:
                st.error("❌ No se pudo enviar el correo. Revisa los mensajes de error arriba.")


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
# PAGE: CAMBIAR CONTRASEÑA
# ════════════════════════════════════════════
def page_cambiar_pwd():
    st.markdown('<div class="section-header">🔑 Cambiar Contraseña</div>', unsafe_allow_html=True)

    user = st.session_state.user
    with st.form("change_pwd"):
        current_pwd = st.text_input("🔒 Contraseña actual", type="password")
        new_pwd = st.text_input("🔑 Nueva contraseña", type="password")
        confirm_pwd = st.text_input("🔑 Confirmar nueva contraseña", type="password")
        submit = st.form_submit_button("✅ Cambiar Contraseña", type="primary")

    if submit:
        if not current_pwd or not new_pwd or not confirm_pwd:
            st.error("Completa todos los campos.")
        elif user.get("Password", "") != current_pwd:
            st.error("La contraseña actual es incorrecta.")
        elif len(new_pwd) < 6:
            st.error("La nueva contraseña debe tener al menos 6 caracteres.")
        elif new_pwd != confirm_pwd:
            st.error("Las contraseñas no coinciden.")
        else:
            sm.update_cell_by_id(C.HOJA_USUARIOS, "ID_Usuario",
                                  user["ID_Usuario"], "Password", new_pwd)
            st.session_state.user["Password"] = new_pwd
            sm.log_action(user["Nombre"], "Cambiar contraseña", "Usuario",
                          user["ID_Usuario"], "")
            st.success("✅ Contraseña cambiada exitosamente.")


# ════════════════════════════════════════════
# PAGE: CALENDARIO GANTT
# ════════════════════════════════════════════
def page_calendario():
    user = st.session_state.user
    rol = user.get("Rol", "Responsable")
    email = user.get("Correo", "").strip().lower()
    st.markdown('<div class="section-header">📅 Calendario de Procesos</div>', unsafe_allow_html=True)

    instances = sm.get_all_records(C.HOJA_INSTANCIAS)
    avances = sm.get_all_records(C.HOJA_AVANCE)

    # Filter by role
    if rol == "Responsable":
        my_inst_ids = set(a.get("ID_Instancia") for a in avances
                          if a.get("Correo", "").strip().lower() == email)
        instances = [i for i in instances if i.get("ID_Instancia") in my_inst_ids]
    elif rol == "Gerente":
        instances = [i for i in instances if i.get("Gerente_Responsable") == user.get("Nombre")]

    active_instances = [i for i in instances if i.get("Estatus") == "En Proceso"]
    if not active_instances:
        st.markdown('<div class="info-box">No hay procesos activos para mostrar en el calendario.</div>',
                    unsafe_allow_html=True)
        return

    import json as _json
    processes_js = []
    all_dates = []

    for inst in active_instances:
        inst_id = inst.get("ID_Instancia", "")
        inst_avs = [a for a in avances if a.get("ID_Instancia") == inst_id]
        inst_avs.sort(key=lambda x: int(x.get("Numero_Actividad", 0)))

        # Calculate estimated dates for pending tasks
        last_end = None
        activities_js = []
        for a in inst_avs:
            start = a.get("Fecha_Inicio", "")
            limite = a.get("Fecha_Limite", "")
            cierre = a.get("Fecha_Cierre", "")
            estatus = a.get("Estatus", "Pendiente")
            dias = int(a.get("Dias_Teoricos", 1)) if a.get("Dias_Teoricos") else 1

            if estatus == "Completada" and start:
                bar_start = start
                bar_end = cierre if cierre else limite
                last_end = bar_end
                estatus_display = "completada"
            elif estatus == "Activa" and start and limite:
                bar_start = start
                bar_end = limite
                last_end = limite
                remaining = sm.remaining_business_days(limite)
                if remaining < 0:
                    estatus_display = "vencida"
                elif remaining <= C.DIAS_ALERTA_AMARILLA:
                    estatus_display = "en-riesgo"
                else:
                    estatus_display = "activa"
            elif estatus == "Pendiente":
                estatus_display = "pendiente"
                if last_end:
                    try:
                        from datetime import datetime as dtc
                        ref = dtc.strptime(last_end, "%Y-%m-%d").date()
                        est_start = sm.add_business_days(ref, 0)
                        est_end = sm.add_business_days(ref, dias)
                        bar_start = est_start.strftime("%Y-%m-%d")
                        bar_end = est_end.strftime("%Y-%m-%d")
                        last_end = bar_end
                    except (ValueError, TypeError):
                        bar_start = ""
                        bar_end = ""
                else:
                    bar_start = ""
                    bar_end = ""
            else:
                bar_start = start if start else ""
                bar_end = limite if limite else ""
                estatus_display = "pendiente"

            if bar_start:
                all_dates.append(bar_start)
            if bar_end:
                all_dates.append(bar_end)

            activities_js.append({
                "num": int(a.get("Numero_Actividad", 0)),
                "name": a.get("Actividad", ""),
                "phase": a.get("Fase", ""),
                "resp": a.get("Responsable", ""),
                "start": bar_start,
                "end": bar_end,
                "status": estatus_display,
                "days": dias,
            })

        processes_js.append({
            "id": inst_id,
            "name": inst.get("Nombre_Instancia", inst_id),
            "activities": activities_js,
        })

    if all_dates:
        sorted_dates = sorted([d for d in all_dates if d])
        min_date = sorted_dates[0]
        max_date = sorted_dates[-1]
    else:
        min_date = datetime.now().strftime("%Y-%m-%d")
        max_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    from datetime import datetime as dtc2
    start_dt = dtc2.strptime(min_date, "%Y-%m-%d") - timedelta(days=2)
    end_dt = dtc2.strptime(max_date, "%Y-%m-%d") + timedelta(days=5)
    total_days = (end_dt - start_dt).days
    start_date_str = start_dt.strftime("%Y-%m-%d")
    today_str = datetime.now().strftime("%Y-%m-%d")
    data_json = _json.dumps(processes_js)
    dw = 22
    grid_min = max(800, total_days * dw)

    gantt_html = f"""
    <style>
    .g-wrap{{font-family:var(--font-sans)}}
    .g-tabs{{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}}
    .g-tab{{padding:5px 12px;border-radius:8px;font-size:11px;cursor:pointer;border:0.5px solid var(--color-border-secondary);background:var(--color-background-primary);color:var(--color-text-secondary);transition:all .15s}}
    .g-tab:hover{{border-color:#0D2B6E;color:#0D2B6E}}
    .g-tab.active{{background:#0D2B6E;color:#fff;border-color:#0D2B6E}}
    .g-legend{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:10px;font-size:10px;color:var(--color-text-secondary)}}
    .g-legend span{{display:flex;align-items:center;gap:4px}}
    .g-ldot{{width:8px;height:8px;border-radius:2px}}
    .g-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;margin-bottom:12px}}
    .g-card{{background:var(--color-background-secondary);border-radius:8px;padding:8px 10px}}
    .g-card-v{{font-size:18px;font-weight:500;color:var(--color-text-primary)}}
    .g-card-l{{font-size:9px;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.3px;margin-top:1px}}
    .g-container{{overflow-x:auto}}
    .g-grid{{display:grid;min-width:{grid_min}px;grid-template-columns:160px 1fr}}
    .g-label{{padding:3px 6px;font-size:10px;display:flex;align-items:center;gap:4px;border-bottom:0.5px solid var(--color-border-tertiary);min-height:26px;color:var(--color-text-primary);overflow:hidden}}
    .g-label .gn{{font-weight:500;color:var(--color-text-tertiary);min-width:16px;font-size:9px;flex-shrink:0}}
    .g-label-txt{{overflow:hidden;min-width:0}}
    .g-label .ga{{font-weight:500;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}}
    .g-label .gr{{font-size:9px;color:var(--color-text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}}
    .g-tl{{position:relative;border-bottom:0.5px solid var(--color-border-tertiary);min-height:26px}}
    .g-bar{{position:absolute;height:16px;top:5px;border-radius:3px;display:flex;align-items:center;padding:0 3px;font-size:8px;font-weight:500;color:#fff;transition:all .15s;cursor:default;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:4px}}
    .g-bar:hover{{filter:brightness(1.12);transform:scaleY(1.25)}}
    .g-bar.completada{{background:#22C55E}}
    .g-bar.activa{{background:#2563EB}}
    .g-bar.en-riesgo{{background:#F59E0B}}
    .g-bar.vencida{{background:#EF4444;animation:gpulse 1.5s infinite}}
    .g-bar.pendiente{{background:#D1D5DB}}
    @keyframes gpulse{{0%,100%{{opacity:1}}50%{{opacity:.7}}}}
    .g-dh{{text-align:center;font-size:8px;color:var(--color-text-tertiary);padding:2px 0;border-bottom:0.5px solid var(--color-border-tertiary);border-left:0.5px solid var(--color-border-tertiary)}}
    .g-dh.we{{background:var(--color-background-secondary)}}
    .g-today{{position:absolute;top:0;bottom:0;width:2px;background:#C41E2E;z-index:10;pointer-events:none}}
    .g-today-lbl{{position:absolute;top:-14px;font-size:7px;color:#C41E2E;font-weight:500;transform:translateX(-50%);white-space:nowrap}}
    .g-phase{{background:var(--color-background-secondary);padding:2px 8px;font-size:10px;font-weight:500;color:#3730A3;grid-column:1/-1}}
    .g-tip{{position:fixed;background:var(--color-background-primary);border:0.5px solid var(--color-border-secondary);border-radius:8px;padding:8px 12px;font-size:11px;color:var(--color-text-primary);z-index:100;pointer-events:none;display:none;max-width:240px;line-height:1.5}}
    .g-we-bg{{position:absolute;top:0;bottom:0;background:var(--color-background-secondary)}}
    </style>
    <div class="g-wrap">
    <div class="g-cards" id="gCards"></div>
    <div class="g-tabs" id="gTabs"></div>
    <div class="g-legend">
      <span><span class="g-ldot" style="background:#22C55E"></span>Completada</span>
      <span><span class="g-ldot" style="background:#2563EB"></span>En proceso</span>
      <span><span class="g-ldot" style="background:#F59E0B"></span>En riesgo</span>
      <span><span class="g-ldot" style="background:#EF4444"></span>Vencida</span>
      <span><span class="g-ldot" style="background:#D1D5DB"></span>Pendiente</span>
    </div>
    <div class="g-container" id="gCont"></div>
    <div class="g-tip" id="gTip"></div>
    </div>
    <script>
    const P={data_json};const S='{start_date_str}';const D={total_days};const T='{today_str}';const W={dw};
    let aP='all';
    function dd(a,b){{return Math.round((new Date(a)-new Date(b))/864e5);}}
    function isW(d){{const x=d.getDay();return x===0||x===6;}}
    function fm(s){{if(!s)return'';const d=new Date(s);const m=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];return d.getUTCDate()+' '+m[d.getUTCMonth()];}}
    function gA(){{let r=[];P.forEach(p=>p.activities.forEach(a=>r.push({{...a,proc:p.name}})));return r;}}
    function cA(){{if(aP==='all')return gA();const p=P.find(x=>x.id===aP);return p?p.activities.map(a=>({{...a,proc:p.name}})):[];}}
    function rT(){{const e=document.getElementById('gTabs');let h='<button class="g-tab'+(aP==='all'?' active':'')+'" onclick="aP=\\'all\\';rr()">Todos</button>';P.forEach(p=>{{const s=p.name.length>20?p.name.substring(0,20)+'…':p.name;h+='<button class="g-tab'+(aP===p.id?' active':'')+'" onclick="aP=\\''+p.id+'\\';rr()">'+s+'</button>';}});e.innerHTML=h;}}
    function rC(){{const a=cA();const c=a.filter(x=>x.status==='completada').length;const ac=a.filter(x=>x.status==='activa').length;const rk=a.filter(x=>x.status==='en-riesgo'||x.status==='vencida').length;const pc=a.length?Math.round(c/a.length*100):0;document.getElementById('gCards').innerHTML='<div class="g-card"><div class="g-card-v">'+a.length+'</div><div class="g-card-l">Actividades</div></div><div class="g-card"><div class="g-card-v" style="color:#22C55E">'+c+'</div><div class="g-card-l">Completadas</div></div><div class="g-card"><div class="g-card-v" style="color:#2563EB">'+ac+'</div><div class="g-card-l">En proceso</div></div><div class="g-card"><div class="g-card-v" style="color:#F59E0B">'+rk+'</div><div class="g-card-l">Riesgo/Vencidas</div></div><div class="g-card"><div class="g-card-v">'+pc+'%</div><div class="g-card-l">Avance</div></div>';}}
    function rG(){{const a=cA();const tw=D*W;const e=document.getElementById('gCont');let h='<div class="g-grid" style="grid-template-columns:160px '+tw+'px;">';h+='<div style="border-bottom:0.5px solid var(--color-border-tertiary);padding:0 6px;display:flex;align-items:end;padding-bottom:2px;font-size:9px;font-weight:500;color:var(--color-text-secondary)">Actividad</div><div style="display:flex;">';for(let i=0;i<D;i++){{const d=new Date(S);d.setDate(d.getDate()+i);const we=isW(d);const dn=d.getDate();const mo=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][d.getMonth()];const lb=dn===1||i===0?dn+' '+mo:we?'':dn;h+='<div class="g-dh'+(we?' we':'')+'" style="width:'+W+'px;min-width:'+W+'px;">'+lb+'</div>';}}h+='</div>';let cp='';a.forEach(x=>{{if(x.phase!==cp&&aP!=='all'){{cp=x.phase;h+='<div class="g-phase">'+x.phase+'</div>';}}const pl=aP==='all'?' <span style="font-size:8px;color:var(--color-text-tertiary)">'+x.proc.substring(0,12)+'</span>':'';h+='<div class="g-label"><span class="gn">'+String(x.num).padStart(2,'0')+'</span><div class="g-label-txt"><span class="ga">'+x.name+'</span>'+pl+'<span class="gr">'+x.resp+'</span></div></div>';const off=x.start?Math.max(0,dd(x.start,S)):0;const dur=x.start&&x.end?Math.max(1,dd(x.end,x.start)):1;const l=off*W;const w=Math.max(dur*W,4);h+='<div class="g-tl">';for(let i=0;i<D;i++){{const d=new Date(S);d.setDate(d.getDate()+i);if(isW(d))h+='<div class="g-we-bg" style="left:'+(i*W)+'px;width:'+W+'px;"></div>';}}if(x.start){{const tp=x.name+'|'+x.resp+'|'+fm(x.start)+' → '+fm(x.end)+'|'+x.days+'d hábiles|'+x.status;const mc=Math.floor(w/6);const tx=mc>4?x.name.substring(0,mc):'';h+='<div class="g-bar '+x.status+'" style="left:'+l+'px;width:'+w+'px;" data-tip="'+tp+'">'+tx+'</div>';}}const to=dd(T,S);if(to>=0&&to<D)h+='<div class="g-today" style="left:'+(to*W+W/2)+'px;"><div class="g-today-lbl">Hoy</div></div>';h+='</div>';}});h+='</div>';e.innerHTML=h;const tp=document.getElementById('gTip');e.querySelectorAll('.g-bar').forEach(b=>{{b.addEventListener('mouseenter',ev=>{{const p=b.dataset.tip.split('|');const sm={{completada:'Completada',activa:'En proceso','en-riesgo':'En riesgo',vencida:'Vencida',pendiente:'Pendiente (estimado)'}};tp.innerHTML='<div style="font-weight:500;margin-bottom:3px">'+p[0]+'</div><div style="color:var(--color-text-secondary)">'+p[1]+'</div><div style="color:var(--color-text-secondary)">'+p[2]+'</div><div style="color:var(--color-text-secondary)">'+p[3]+'</div><div style="margin-top:3px;font-weight:500">'+(sm[p[4]]||p[4])+'</div>';tp.style.display='block';tp.style.left=Math.min(ev.pageX+10,window.innerWidth-260)+'px';tp.style.top=(ev.pageY-90)+'px';}});b.addEventListener('mouseleave',()=>{{tp.style.display='none';}});}});}}
    function rr(){{rT();rC();rG();}}
    rr();
    </script>
    """

    import streamlit.components.v1 as components
    all_acts_count = sum(len([a for a in avances if a.get("ID_Instancia") == p.get("ID_Instancia")])
                         for p in active_instances)
    chart_height = max(450, all_acts_count * 30 + 180)
    components.html(gantt_html, height=chart_height, scrolling=True)

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
    elif page == "cambiar_pwd":
        page_cambiar_pwd()
    elif page == "calendario":
        page_calendario()
    else:
        page_inicio()


if __name__ == "__main__":
    main()
