"""
CSS profesional para Plataforma de Procesos Transversales IMEMSA
Diseño replicado de la app de Motores Yamaha
"""

NAVY = "#0D2B6E"
RED = "#C41E2E"


def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Source+Sans+3:wght@300;400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Source Sans 3', sans-serif; background: #F0F3F9;
    }
    h1,h2,h3,h4 { font-family: 'Barlow Condensed', sans-serif; letter-spacing:.5px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D2B6E 0%, #091D4E 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * { color: #E8EDF7 !important; }
    [data-testid="stSidebar"] .sidebar-divider {
        border-top: 1px solid rgba(255,255,255,.15); margin: 12px 0;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        background: rgba(255,255,255,.08) !important;
        border: 1px solid rgba(255,255,255,.18) !important;
        color: #fff !important; border-radius: 8px !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 600 !important; transition: background .2s;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover {
        background: rgba(255,255,255,.18) !important;
    }

    .main .block-container { padding: 1.5rem 2rem 3rem 2rem; max-width:1400px; }

    /* ── Metric Cards ── */
    .metric-card {
        background: #fff; border-radius: 12px; padding: 20px 24px;
        box-shadow: 0 1px 6px rgba(13,43,110,.10);
        border-left: 4px solid var(--card-accent, #0D2B6E);
        transition: transform .15s, box-shadow .15s;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(13,43,110,.14); }
    .metric-card .mc-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.4rem; font-weight: 800; line-height: 1; color: #0D2B6E;
    }
    .metric-card .mc-label {
        font-size: .82rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: .6px; color: #8592A3; margin-top: 4px;
    }
    .metric-card.green { --card-accent: #22C55E; }
    .metric-card.green .mc-value { color: #065F46; }
    .metric-card.yellow { --card-accent: #F59E0B; }
    .metric-card.yellow .mc-value { color: #92400E; }
    .metric-card.red { --card-accent: #EF4444; }
    .metric-card.red .mc-value { color: #991B1B; }

    /* ── Process/Order Cards ── */
    .process-card {
        background: #fff; border-radius: 12px; padding: 20px 22px;
        box-shadow: 0 1px 6px rgba(13,43,110,.09); margin-bottom: 14px;
        border-top: 3px solid #0D2B6E; transition: transform .15s, box-shadow .15s;
    }
    .process-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(13,43,110,.14); }
    .process-folio {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.15rem; font-weight: 700; color: #0D2B6E;
    }
    .process-desc { font-size: .85rem; color: #4B5563; margin-top: 2px; }

    /* ── Badges ── */
    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px;
    }
    .badge-en-proceso, .badge-activa { background: #DBEAFE; color: #1E40AF; }
    .badge-completada, .badge-completado { background: #D1FAE5; color: #065F46; }
    .badge-cancelado { background: #F3F4F6; color: #6B7280; }
    .badge-pendiente { background: #F3F4F6; color: #6B7280; }
    .badge-vencida { background: #FEE2E2; color: #991B1B; }
    .badge-en-riesgo { background: #FEF3C7; color: #92400E; }
    .badge-vigente { background: #D1FAE5; color: #065F46; }
    .badge-consumida { background: #DBEAFE; color: #1E40AF; }
    .badge-revocada { background: #FEE2E2; color: #991B1B; }
    .badge-borrador { background: #FEF3C7; color: #92400E; }

    /* ── Progress Bar ── */
    .progress-wrap { background: #E5E7EB; border-radius: 6px; height: 8px; overflow:hidden; margin: 8px 0; }
    .progress-fill { height: 8px; border-radius: 6px;
                     background: linear-gradient(90deg, #0D2B6E, #2563EB); transition: width .4s; }

    /* ── Semaphore Dots ── */
    .semaphore-dot {
        display: inline-block; width: 12px; height: 12px;
        border-radius: 50%; margin-right: 6px; vertical-align: middle;
    }
    .sem-green  { background: #22C55E; box-shadow: 0 0 6px #22C55E88; }
    .sem-yellow { background: #F59E0B; box-shadow: 0 0 6px #F59E0B88; }
    .sem-red    { background: #EF4444; box-shadow: 0 0 6px #EF444488; animation: pulse-red 1.2s infinite; }
    .sem-gray   { background: #D1D5DB; }
    @keyframes pulse-red {
        0%,100% { box-shadow: 0 0 6px #EF444488; }
        50%      { box-shadow: 0 0 14px #EF4444CC; }
    }

    /* ── Activity Rows ── */
    .act-row {
        background: #fff; border-radius: 10px; padding: 14px 18px; margin-bottom: 8px;
        border-left: 4px solid var(--act-color, #D1D5DB);
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
        transition: transform .12s, box-shadow .12s;
    }
    .act-row:hover { transform: translateX(3px); box-shadow: 0 2px 8px rgba(0,0,0,.08); }
    .act-row-completada  { --act-color: #22C55E; background: #F0FDF4; }
    .act-row-activa      { --act-color: #2563EB; }
    .act-row-en-riesgo   { --act-color: #F59E0B; background: #FFFBEB; }
    .act-row-pendiente   { --act-color: #D1D5DB; }
    .act-row-vencida     { --act-color: #EF4444; background: #FEF2F2; }
    .act-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.05rem; font-weight: 700; color: #0D2B6E;
    }
    .act-meta { font-size: .78rem; color: #8592A3; margin-top: 2px; }

    /* ── Phase Chip ── */
    .phase-chip {
        display: inline-block; padding: 2px 10px; border-radius: 12px;
        font-size: .70rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: .5px; background: #EEF2FF; color: #3730A3; margin-right: 6px;
    }

    /* ── Phase Header ── */
    .phase-header {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.1rem; font-weight: 700; color: #0D2B6E;
        background: linear-gradient(90deg, #EEF2FF, transparent);
        padding: 8px 14px; border-radius: 8px;
        border-left: 4px solid #3730A3;
        margin: 16px 0 8px 0;
    }

    /* ── Section Header ── */
    .section-header {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.5rem; font-weight: 800; color: #0D2B6E;
        border-bottom: 3px solid #C41E2E;
        padding-bottom: 6px; margin-bottom: 20px; letter-spacing: .4px;
    }

    /* ── Avatar ── */
    .avatar {
        display: inline-flex; align-items:center; justify-content:center;
        width: 38px; height: 38px; border-radius: 50%;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 800; font-size: 1rem; color: #fff; margin-right: 8px;
        vertical-align: middle;
    }

    /* ── Days Badge ── */
    .days-badge {
        font-size: .68rem; font-weight: 700; padding: 2px 8px;
        border-radius: 12px; display: inline-block;
    }
    .days-ok { background: #D1FAE5; color: #065F46; }
    .days-warn { background: #FEF3C7; color: #92400E; }
    .days-over { background: #FEE2E2; color: #991B1B; }

    /* ── Instance Header Card ── */
    .instance-header {
        background: #fff; border-radius: 12px; padding: 24px;
        box-shadow: 0 1px 6px rgba(13,43,110,.10);
        border-top: 4px solid #0D2B6E; margin-bottom: 20px;
    }
    .instance-folio {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.5rem; font-weight: 800; color: #0D2B6E;
    }

    /* ── Template Card ── */
    .template-card {
        background: #fff; border-radius: 12px; padding: 18px 22px;
        box-shadow: 0 1px 6px rgba(13,43,110,.09); margin-bottom: 14px;
        border-left: 4px solid #0D2B6E;
        transition: transform .15s, box-shadow .15s;
    }
    .template-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(13,43,110,.14); }

    /* ── Info/Warning/Success Boxes ── */
    .info-box {
        background: #EEF2FF; border-left: 4px solid #3730A3;
        padding: 12px 16px; border-radius: 0 8px 8px 0;
        font-size: .9rem; color: #1E1B4B; margin: 8px 0;
    }
    .warning-box {
        background: #FEF3C7; border-left: 4px solid #F59E0B;
        padding: 12px 16px; border-radius: 0 8px 8px 0;
        font-size: .9rem; color: #92400E; margin: 8px 0;
    }
    .success-box {
        background: #D1FAE5; border-left: 4px solid #22C55E;
        padding: 12px 16px; border-radius: 0 8px 8px 0;
        font-size: .9rem; color: #065F46; margin: 8px 0;
    }
    .error-box {
        background: #FEE2E2; border-left: 4px solid #EF4444;
        padding: 12px 16px; border-radius: 0 8px 8px 0;
        font-size: .9rem; color: #991B1B; margin: 8px 0;
    }

    /* ── Comment Card ── */
    .comment-card {
        background: #F8FAFC; padding: 10px 16px; border-radius: 8px;
        margin-bottom: 8px; border-left: 3px solid #D1D9E8;
    }

    /* ── Login Card ── */
    .login-card {
        max-width: 400px; margin: 0 auto; background: #fff;
        padding: 36px 32px; border-radius: 16px;
        box-shadow: 0 8px 40px rgba(13,43,110,.15);
        border-top: 4px solid #0D2B6E;
    }

    /* ── Form Inputs ── */
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] select,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {
        border-radius: 8px !important;
        border: 1.5px solid #D1D9E8 !important;
        font-family: 'Source Sans 3', sans-serif !important;
        background: #FFFFFF !important; color: #1F2937 !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder { color: #9CA3AF !important; }

    [data-testid="stSelectbox"] > div > div {
        background: #FFFFFF !important;
        border: 1.5px solid #D1D9E8 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] p,
    [data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #1F2937 !important;
    }
    .main [data-testid="stWidgetLabel"] p,
    .main [data-testid="stWidgetLabel"] span,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    [data-testid="stForm"] label,
    .main label p, .main label span { color: #1F2937 !important; }

    /* ── Tabs ── */
    [data-testid="stTabs"] [data-baseweb="tab"] p,
    [data-testid="stTabs"] [data-baseweb="tab"] span,
    [data-testid="stTabs"] button[role="tab"] p,
    [data-testid="stTabs"] button[role="tab"] span,
    [data-testid="stTabs"] button[role="tab"] { color: #0D2B6E !important; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #0D2B6E !important; font-weight: 700 !important;
        border-bottom: 3px solid #C41E2E !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #E8EDF7 !important; }

    /* ── Primary Button ── */
    [data-testid="stButton"] button[kind="primary"] {
        background: #0D2B6E !important; border: none !important;
        border-radius: 8px !important; font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 700 !important; letter-spacing: .3px !important;
        transition: background .2s !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover { background: #C41E2E !important; }

    .stAlert { border-radius: 8px !important; }

    /* ── Expander ── */
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] details summary p {
        color: #0D2B6E !important; font-weight: 600 !important;
    }
    [data-testid="stExpander"] {
        background: #EEF2FF !important;
        border: 1.5px solid #C7D2FE !important; border-radius: 8px !important;
    }

    /* ── Hide Streamlit defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    </style>
    """


# ── Component Helpers ──

def badge(text, tipo=None):
    if tipo is None:
        tipo = text.lower().replace(" ", "-")
    return f'<span class="badge badge-{tipo}">{text}</span>'


AVATAR_COLORS = [
    "#0D2B6E", "#C41E2E", "#2563EB", "#059669", "#7C3AED",
    "#DB2777", "#EA580C", "#0891B2", "#4F46E5", "#9333EA"
]

def avatar(name, size=38):
    initials = "".join([p[0].upper() for p in name.split()[:2]]) if name else "?"
    color_idx = sum(ord(c) for c in name) % len(AVATAR_COLORS) if name else 0
    color = AVATAR_COLORS[color_idx]
    return (f'<span class="avatar" style="width:{size}px;height:{size}px;'
            f'background:{color};font-size:{size*0.38}px;">{initials}</span>')


def metric_card(value, label, color=""):
    cls = f"metric-card {color}" if color else "metric-card"
    return f"""<div class="{cls}">
        <div class="mc-value">{value}</div>
        <div class="mc-label">{label}</div>
    </div>"""


def progress_bar(pct):
    pct = max(0, min(100, pct))
    return (f'<div class="progress-wrap">'
            f'<div class="progress-fill" style="width:{pct}%;"></div>'
            f'</div><span style="font-size:.75rem;color:#8592A3;">{pct}% completado</span>')


def days_badge(days):
    if days is None:
        return ""
    if days > 2:
        return f'<span class="days-badge days-ok">⏱ {days}d restantes</span>'
    elif days >= 0:
        return f'<span class="days-badge days-warn">⚠️ {days}d restantes</span>'
    else:
        return f'<span class="days-badge days-over">🔴 {abs(days)}d vencida</span>'


def sem_dot(color):
    return f'<span class="semaphore-dot sem-{color}"></span>'
