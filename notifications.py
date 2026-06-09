"""
Motor de notificaciones por correo electrónico
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

APP_URL = "https://procesostransversales2026.streamlit.app"


def _get_smtp():
    email = st.secrets.get("smtp_email", "")
    password = st.secrets.get("smtp_password", "")
    return email, password


def _send_email(to_email, subject, html_body):
    sender, password = _get_smtp()
    if not sender or not password:
        st.warning("⚠️ Credenciales SMTP no configuradas en Secrets.")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"IMEMSA Procesos <{sender}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("❌ Error de autenticación SMTP. Verifica smtp_email y smtp_password.")
        return False
    except smtplib.SMTPRecipientsRefused:
        st.warning(f"⚠️ Correo rechazado para: {to_email}")
        return False
    except Exception as e:
        st.warning(f"⚠️ Error al enviar correo a {to_email}: {type(e).__name__}: {e}")
        return False


def test_email(to_email):
    subject = "✅ Prueba de correo — IMEMSA Procesos Transversales"
    body = _base_template("Prueba Exitosa", f"""
    <p>Este es un correo de prueba del sistema de notificaciones.</p>
    <p>Si recibes este mensaje, el motor de correos está funcionando correctamente.</p>
    <p><strong>Destinatario:</strong> {to_email}</p>
    """)
    return _send_email(to_email, subject, body)


def _base_template(title, body_html):
    return f"""
    <html>
    <body style="font-family:Arial,sans-serif;margin:0;padding:0;background:#f5f5f5;">
    <div style="max-width:600px;margin:20px auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <div style="background:linear-gradient(135deg,#0D2B6E,#1a3f8a);padding:20px 30px;">
            <h1 style="color:white;margin:0;font-size:20px;">IMEMSA</h1>
            <p style="color:rgba(255,255,255,0.8);margin:4px 0 0;font-size:13px;">Plataforma de Procesos Transversales</p>
        </div>
        <div style="padding:25px 30px;">
            <h2 style="color:#0D2B6E;margin-top:0;font-size:18px;">{title}</h2>
            {body_html}
        </div>
        <div style="background:#f0f4fa;padding:15px 30px;text-align:center;font-size:12px;color:#666;">
            <a href="{APP_URL}" style="color:#0D2B6E;font-weight:bold;">Acceder a la Plataforma</a>
            <p style="margin:8px 0 0;">Grupo IMEMSA &mdash; Este es un correo autom&aacute;tico, no responder.</p>
        </div>
    </div>
    </body></html>
    """


def notify_task_activated(email, nombre, proceso, actividad, plazo_dias, fecha_limite, **kwargs):
    subject = f"📋 Nueva tarea asignada: {actividad}"
    body = _base_template("Nueva Tarea Asignada", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>Se te ha asignado una nueva tarea en el proceso <strong>{proceso}</strong>:</p>
    <div style="background:#f0f4fa;padding:15px;border-radius:8px;border-left:4px solid #0D2B6E;margin:15px 0;">
        <p style="margin:0;"><strong>Actividad:</strong> {actividad}</p>
        <p style="margin:5px 0 0;"><strong>Plazo:</strong> {plazo_dias} días hábiles</p>
        <p style="margin:5px 0 0;"><strong>Fecha límite:</strong> {fecha_limite}</p>
    </div>
    <p>Por favor ingresa a la plataforma para dar seguimiento.</p>
    """)
    return _send_email(email, subject, body)


def notify_reminder(email, nombre, actividad, dias_restantes, proceso, **kwargs):
    subject = f"⚠️ Recordatorio: {actividad} - {dias_restantes} día(s) restante(s)"
    body = _base_template("Recordatorio de Actividad", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>Te recordamos que la actividad <strong>{actividad}</strong> del proceso
    <strong>{proceso}</strong> tiene <strong>{dias_restantes} día(s) hábil(es) restante(s)</strong>.</p>
    <p>Por favor complétala a la brevedad.</p>
    """)
    return _send_email(email, subject, body)


def notify_overdue(email, nombre, actividad, proceso, dias_vencidos, **kwargs):
    subject = f"🔴 Actividad vencida: {actividad}"
    body = _base_template("Actividad Vencida", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>La actividad <strong>{actividad}</strong> del proceso <strong>{proceso}</strong>
    tiene <strong style="color:#C41E2E;">{dias_vencidos} día(s) de retraso</strong>.</p>
    <p>Se requiere atención inmediata.</p>
    """)
    return _send_email(email, subject, body)


def notify_task_completed(email_gerente, gerente, actividad, responsable, proceso):
    subject = f"✅ Actividad completada: {actividad}"
    body = _base_template("Actividad Completada", f"""
    <p>Hola <strong>{gerente}</strong>,</p>
    <p>La actividad <strong>{actividad}</strong> del proceso <strong>{proceso}</strong>
    ha sido completada por <strong>{responsable}</strong>.</p>
    """)
    return _send_email(email_gerente, subject, body)


def notify_process_completed(email, nombre, proceso, folio):
    subject = f"🎉 Proceso completado: {proceso}"
    body = _base_template("Proceso Completado", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>El proceso <strong>{proceso}</strong> (Folio: <strong>{folio}</strong>)
    ha sido completado exitosamente.</p>
    <p>Todas las actividades han sido finalizadas.</p>
    """)
    return _send_email(email, subject, body)


def notify_confirmation_number(email, nombre, auth_id, proceso, vencimiento):
    subject = f"🔑 Número de confirmación: {auth_id}"
    body = _base_template("Número de Confirmación", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>Se ha generado tu número de confirmación para la plataforma:</p>
    <div style="background:#f0f4fa;padding:20px;border-radius:8px;text-align:center;margin:15px 0;">
        <p style="font-size:28px;font-weight:800;color:#0D2B6E;margin:0;">{auth_id}</p>
    </div>
    <p><strong>Proceso:</strong> {proceso}</p>
    <p><strong>Vigencia:</strong> Hasta el {vencimiento}</p>
    <p>Utiliza este número al crear tu plantilla o lanzar una instancia en la plataforma.</p>
    """)
    return _send_email(email, subject, body)


def notify_welcome(email, nombre, proceso, actividad, password=""):
    subject = "🎉 Bienvenido a la Plataforma de Procesos Transversales IMEMSA"
    pwd_section = ""
    if password:
        pwd_section = f"""
        <div style="background:#f0f4fa;padding:15px;border-radius:8px;text-align:center;margin:15px 0;">
            <p style="margin:0;font-size:12px;color:#666;">Tu contraseña de acceso:</p>
            <p style="font-size:22px;font-weight:800;color:#0D2B6E;margin:5px 0;">{password}</p>
        </div>
        """
    body = _base_template("Bienvenido a IMEMSA Procesos", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>Has sido registrado(a) en la Plataforma de Procesos Transversales del Grupo IMEMSA.</p>
    <p>Tu primera tarea asignada es:</p>
    <div style="background:#f0f4fa;padding:15px;border-radius:8px;border-left:4px solid #0D2B6E;margin:15px 0;">
        <p style="margin:0;"><strong>Proceso:</strong> {proceso}</p>
        <p style="margin:5px 0 0;"><strong>Actividad:</strong> {actividad}</p>
    </div>
    <p><strong>¿Cómo acceder?</strong></p>
    <p>Ingresa a <a href="{APP_URL}" style="color:#0D2B6E;font-weight:bold;">{APP_URL}</a>
    con tu correo institucional: <strong>{email}</strong></p>
    {pwd_section}
    <p style="font-size:12px;color:#888;">Te recomendamos cambiar tu contraseña después del primer ingreso.</p>
    """)
    return _send_email(email, subject, body)

def notify_new_user(email, nombre, password, admin_copy=False, user_email=""):
    """Notify new user registration with credentials."""
    if admin_copy:
        subject = f"📋 Alta de usuario: {nombre}"
        body = _base_template("Notificación de Alta de Usuario", f"""
        <p>Se ha registrado un nuevo usuario en la Plataforma de Procesos Transversales:</p>
        <div style="background:#f0f4fa;padding:15px;border-radius:8px;border-left:4px solid #0D2B6E;margin:15px 0;">
            <p style="margin:0;"><strong>Nombre:</strong> {nombre}</p>
            <p style="margin:5px 0 0;"><strong>Correo:</strong> {user_email}</p>
            <p style="margin:5px 0 0;"><strong>Contraseña:</strong> {password}</p>
        </div>
        """)
    else:
        subject = "🎉 Bienvenido a la Plataforma de Procesos Transversales IMEMSA"
        body = _base_template("Bienvenido a IMEMSA Procesos", f"""
        <p>Hola <strong>{nombre}</strong>,</p>
        <p>Has sido registrado(a) en la Plataforma de Procesos Transversales del Grupo IMEMSA.</p>
        <p>Tus credenciales de acceso son:</p>
        <div style="background:#f0f4fa;padding:15px;border-radius:8px;text-align:center;margin:15px 0;">
            <p style="margin:0;font-size:12px;color:#666;">Tu correo:</p>
            <p style="font-size:16px;font-weight:700;color:#0D2B6E;margin:5px 0;">{email}</p>
            <p style="margin:10px 0 0;font-size:12px;color:#666;">Tu contraseña:</p>
            <p style="font-size:22px;font-weight:800;color:#0D2B6E;margin:5px 0;">{password}</p>
        </div>
        <p>Ingresa a <a href="{APP_URL}" style="color:#0D2B6E;font-weight:bold;">{APP_URL}</a></p>
        <p style="font-size:12px;color:#888;">Te recomendamos cambiar tu contraseña después del primer ingreso.</p>
        """)
    return _send_email(email, subject, body)


def notify_password_recovery(email, nombre, password):
    """Send password recovery email."""
    subject = "🔑 Recuperación de contraseña — IMEMSA Procesos Transversales"
    body = _base_template("Recuperación de Contraseña", f"""
    <p>Hola <strong>{nombre}</strong>,</p>
    <p>Recibimos una solicitud de recuperación de contraseña para tu cuenta.</p>
    <div style="background:#f0f4fa;padding:20px;border-radius:8px;text-align:center;margin:15px 0;">
        <p style="margin:0;font-size:12px;color:#666;">Tu contraseña actual es:</p>
        <p style="font-size:28px;font-weight:800;color:#0D2B6E;margin:8px 0;">{password}</p>
    </div>
    <p>Ingresa a <a href="{APP_URL}" style="color:#0D2B6E;font-weight:bold;">{APP_URL}</a>
    con tu correo <strong>{email}</strong> y la contraseña de arriba.</p>
    <p style="font-size:12px;color:#888;">Te recomendamos cambiar tu contraseña después de ingresar.</p>
    """)
    return _send_email(email, subject, body)
