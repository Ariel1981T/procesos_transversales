"""
CSS personalizado para la Plataforma de Procesos Transversales IMEMSA
"""

def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    .stApp { font-family: 'Inter', sans-serif; }
    .block-container { max-width: 1200px; padding-top: 1rem; }

    /* ── Header/Logo ── */
    .imemsa-header {
        background: linear-gradient(135deg, #0D2B6E 0%, #1a3f8a 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(13,43,110,0.3);
    }
    .imemsa-header h1 {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .imemsa-header .subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
        margin-top: 2px;
    }
    .user-badge {
        background: rgba(255,255,255,0.15);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ── Navigation Tabs ── */
    .nav-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .nav-btn {
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid #e0e0e0;
        background: white;
        color: #0D2B6E;
        text-decoration: none;
    }
    .nav-btn:hover { border-color: #0D2B6E; background: #F0F4FA; }
    .nav-btn.active {
        background: #0D2B6E;
        color: white;
        border-color: #0D2B6E;
    }

    /* ── Cards ── */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid #0D2B6E;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #0D2B6E;
        line-height: 1;
    }
    .metric-card .label {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card.red { border-left-color: #C41E2E; }
    .metric-card.red .value { color: #C41E2E; }
    .metric-card.green { border-left-color: #28a745; }
    .metric-card.green .value { color: #28a745; }
    .metric-card.yellow { border-left-color: #ffc107; }
    .metric-card.yellow .value { color: #e6a800; }

    /* ── Activity Card ── */
    .activity-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 5px solid #e0e0e0;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .activity-card:hover { box-shadow: 0 3px 15px rgba(0,0,0,0.1); }
    .activity-card.completada { border-left-color: #28a745; background: #f0faf3; }
    .activity-card.activa { border-left-color: #0D2B6E; background: #f0f4fa; }
    .activity-card.vencida { border-left-color: #C41E2E; background: #fdf0f0; }
    .activity-card.en-riesgo { border-left-color: #ffc107; background: #fffcf0; }
    .activity-card.pendiente { border-left-color: #ccc; }

    .activity-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }
    .activity-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px; height: 30px;
        border-radius: 50%;
        background: #0D2B6E;
        color: white;
        font-weight: 700;
        font-size: 0.8rem;
        margin-right: 0.6rem;
        flex-shrink: 0;
    }
    .activity-title {
        font-weight: 700;
        color: #0D2B6E;
        font-size: 0.95rem;
    }
    .activity-desc {
        color: #666;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }

    /* ── Status Badges ── */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .badge-completada { background: #d4edda; color: #155724; }
    .badge-activa, .badge-en-proceso { background: #cce5ff; color: #004085; }
    .badge-vencida { background: #f8d7da; color: #721c24; }
    .badge-en-riesgo { background: #fff3cd; color: #856404; }
    .badge-pendiente { background: #e9ecef; color: #495057; }
    .badge-vigente { background: #d4edda; color: #155724; }
    .badge-consumida { background: #cce5ff; color: #004085; }
    .badge-revocada { background: #f8d7da; color: #721c24; }
    .badge-borrador { background: #fff3cd; color: #856404; }

    /* ── Responsible Avatar ── */
    .avatar {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px; height: 32px;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.75rem;
        color: white;
        margin-right: 0.4rem;
        flex-shrink: 0;
    }

    /* ── Progress Bar ── */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #0D2B6E, #1a5cb5);
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
    }

    /* ── Phase Divider ── */
    .phase-header {
        background: linear-gradient(90deg, #0D2B6E, transparent);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 1rem 0 0.5rem 0;
    }

    /* ── Template Card ── */
    .template-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8edf5;
        transition: all 0.2s;
        margin-bottom: 1rem;
    }
    .template-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-color: #0D2B6E; }

    /* ── Instance Header ── */
    .instance-header {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8edf5;
        margin-bottom: 1.5rem;
    }
    .instance-folio {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0D2B6E;
    }

    /* ── Login ── */
    .login-container {
        max-width: 400px;
        margin: 4rem auto;
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 40px rgba(13,43,110,0.15);
        text-align: center;
    }
    .login-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0D2B6E;
        margin-bottom: 0.3rem;
    }
    .login-subtitle {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* ── Semaforo dots ── */
    .semaforo { display: inline-flex; gap: 0.4rem; align-items: center; }
    .dot {
        width: 12px; height: 12px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-green { background: #28a745; }
    .dot-yellow { background: #ffc107; }
    .dot-red { background: #C41E2E; }
    .dot-gray { background: #ccc; }

    /* ── Misc ── */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0D2B6E;
        border-bottom: 3px solid #C41E2E;
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem 0;
    }
    .info-box {
        background: #f0f4fa;
        border-left: 4px solid #0D2B6E;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    .error-box {
        background: #f8d7da;
        border-left: 4px solid #C41E2E;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    </style>
    """


def badge(text, tipo=None):
    if tipo is None:
        tipo = text.lower().replace(" ", "-")
    css_class = f"badge-{tipo}"
    return f'<span class="badge {css_class}">{text}</span>'


AVATAR_COLORS = [
    "#0D2B6E", "#C41E2E", "#1a5cb5", "#28a745", "#6f42c1",
    "#e83e8c", "#fd7e14", "#20c997", "#007bff", "#6610f2"
]


def avatar(name, size=32):
    initials = "".join([p[0].upper() for p in name.split()[:2]]) if name else "?"
    color_idx = sum(ord(c) for c in name) % len(AVATAR_COLORS) if name else 0
    color = AVATAR_COLORS[color_idx]
    return (
        f'<span class="avatar" style="width:{size}px;height:{size}px;'
        f'background:{color};font-size:{size*0.38}px;">{initials}</span>'
    )


def metric_card(value, label, color=""):
    cls = f"metric-card {color}" if color else "metric-card"
    return f"""
    <div class="{cls}">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
    </div>
    """


def progress_bar(pct):
    pct = max(0, min(100, pct))
    return f"""
    <div class="progress-container">
        <div class="progress-bar" style="width:{pct}%">{pct:.0f}%</div>
    </div>
    """
