"""
Gestión de datos con Supabase para la Plataforma de Procesos Transversales.
Reemplaza Google Sheets con PostgreSQL via Supabase REST API.
"""
import streamlit as st
from datetime import datetime, timedelta
from supabase import create_client
import config as C
import random
import string

# ── Table name mapping ──
TABLE_MAP = {
    C.HOJA_USUARIOS: "usuarios",
    C.HOJA_AUTORIZACIONES: "autorizaciones",
    C.HOJA_PLANTILLAS: "plantillas",
    C.HOJA_ACTIVIDADES_PLANTILLA: "actividades_plantilla",
    C.HOJA_INSTANCIAS: "instancias",
    C.HOJA_AVANCE: "avance_instancia",
    C.HOJA_EVIDENCIAS: "evidencias",
    C.HOJA_COMENTARIOS: "comentarios",
    C.HOJA_LOG: "log_sistema",
}

# ── Column name mapping (Google Sheets names -> Supabase column names) ──
COL_MAP = {
    "ID_Usuario": "id_usuario", "Nombre": "nombre", "Correo": "correo",
    "Telefono": "telefono", "Area": "area", "Rol": "rol", "Activo": "activo",
    "ID_Autorizacion": "id_autorizacion", "Tipo": "tipo", "Solicitante": "solicitante",
    "Nombre_Proceso": "nombre_proceso", "PM_Emisor": "pm_emisor",
    "Fecha_Emision": "fecha_emision", "Fecha_Vencimiento": "fecha_vencimiento",
    "Estatus": "estatus", "ID_Vinculado": "id_vinculado", "Fecha_Consumo": "fecha_consumo",
    "ID_Plantilla": "id_plantilla", "Descripcion": "descripcion",
    "Area_Origen": "area_origen", "Gerente_Creador": "gerente_creador",
    "Fecha_Creacion": "fecha_creacion", "Version": "version",
    "Num_Actividades": "num_actividades", "Num_Fases": "num_fases",
    "Veces_Utilizada": "veces_utilizada", "Dias_Teoricos_Total": "dias_teoricos_total",
    "ID_Actividad_TPL": "id_actividad_tpl", "Numero": "numero", "Fase": "fase",
    "Actividad": "actividad", "Responsable": "responsable",
    "Dias_Teoricos": "dias_teoricos", "Evidencia_Requerida": "evidencia_requerida",
    "ID_Instancia": "id_instancia", "Nombre_Instancia": "nombre_instancia",
    "Gerente_Responsable": "gerente_responsable", "Fecha_Estimada_Fin": "fecha_estimada_fin",
    "Fecha_Real_Fin": "fecha_real_fin", "Porcentaje_Avance": "porcentaje_avance",
    "Unidades": "unidades", "Importe": "importe",
    "ID_Avance": "id_avance", "Numero_Actividad": "numero_actividad",
    "Fecha_Inicio": "fecha_inicio", "Fecha_Limite": "fecha_limite",
    "Fecha_Cierre": "fecha_cierre", "Dias_Reales": "dias_reales",
    "Desviacion": "desviacion", "Tiene_Evidencia": "tiene_evidencia",
    "ID_Evidencia": "id_evidencia", "Nombre_Archivo": "nombre_archivo",
    "URL_Cloudinary": "url_cloudinary", "Public_ID": "public_id",
    "Fecha_Subida": "fecha_subida", "Subido_Por": "subido_por",
    "ID_Comentario": "id_comentario", "Autor": "autor", "Fecha": "fecha", "Texto": "texto",
    "ID_Log": "id_log", "Fecha_Hora": "fecha_hora", "Usuario": "usuario",
    "Accion": "accion", "Entidad": "entidad", "ID_Entidad": "id_entidad",
    "Detalle": "detalle",
    "Password": "password",
}

# Reverse mapping: supabase column -> Google Sheets name
REV_COL_MAP = {v: k for k, v in COL_MAP.items()}


@st.cache_resource(ttl=600)
def get_client():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)


def _table(sheet_name):
    return TABLE_MAP.get(sheet_name, sheet_name)


def _to_db_cols(data_dict):
    """Convert app-level column names to database column names."""
    return {COL_MAP.get(k, k.lower()): v for k, v in data_dict.items()}


def _to_app_cols(row):
    """Convert database column names back to app-level names."""
    return {REV_COL_MAP.get(k, k): v for k, v in row.items()}


def get_all_records(sheet_name):
    """Fetch all records from a table."""
    client = get_client()
    table = _table(sheet_name)
    response = client.table(table).select("*").execute()
    return [_to_app_cols(row) for row in response.data]


def append_row(sheet_name, row_data):
    """Insert a new row into a table."""
    client = get_client()
    table = _table(sheet_name)
    headers = C.HEADERS.get(sheet_name, [])
    if not headers or len(row_data) != len(headers):
        return
    record = {}
    for i, header in enumerate(headers):
        col = COL_MAP.get(header, header.lower())
        val = row_data[i] if i < len(row_data) else ""
        record[col] = val
    client.table(table).insert(record).execute()


def update_cell_by_id(sheet_name, id_column, id_value, target_column, new_value):
    """Update a single cell identified by ID."""
    client = get_client()
    table = _table(sheet_name)
    db_id_col = COL_MAP.get(id_column, id_column.lower())
    db_tgt_col = COL_MAP.get(target_column, target_column.lower())
    client.table(table).update({db_tgt_col: new_value}).eq(db_id_col, str(id_value)).execute()
    return True


def update_row_by_id(sheet_name, id_column, id_value, updates_dict):
    """Update multiple fields in a row identified by ID."""
    client = get_client()
    table = _table(sheet_name)
    db_id_col = COL_MAP.get(id_column, id_column.lower())
    db_updates = _to_db_cols(updates_dict)
    client.table(table).update(db_updates).eq(db_id_col, str(id_value)).execute()
    return True


def get_next_id(prefix, sheet_name, id_column):
    records = get_all_records(sheet_name)
    if not records:
        return f"{prefix}001"
    existing = [r.get(id_column, "") for r in records]
    nums = []
    for eid in existing:
        parts = str(eid).split("-")
        try:
            nums.append(int(parts[-1]))
        except (ValueError, IndexError):
            continue
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}{next_num:03d}"


def get_next_auth_id():
    year = datetime.now().strftime("%Y")
    records = get_all_records(C.HOJA_AUTORIZACIONES)
    prefix = f"PT-{year}-"
    nums = []
    for r in records:
        aid = r.get("ID_Autorizacion", "")
        if str(aid).startswith(prefix):
            try:
                nums.append(int(str(aid).split("-")[-1]))
            except ValueError:
                continue
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}{next_num:03d}"


def get_next_instance_id():
    year = datetime.now().strftime("%Y")
    records = get_all_records(C.HOJA_INSTANCIAS)
    prefix = f"IMEMSA-{year}-"
    nums = []
    for r in records:
        iid = r.get("ID_Instancia", "")
        if str(iid).startswith(prefix):
            try:
                nums.append(int(str(iid).split("-")[-1]))
            except ValueError:
                continue
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}{next_num:03d}"


# ── Business day calculations ──
def add_business_days(start_date, days):
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current


def business_days_between(d1, d2):
    count = 0
    current = d1
    while current < d2:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return count


def remaining_business_days(deadline):
    today = datetime.now().date()
    if isinstance(deadline, str):
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            return 0
    if today >= deadline:
        return -business_days_between(deadline, today)
    return business_days_between(today, deadline)


# ── Initialize (no-op for Supabase, tables created via SQL) ──
def init_spreadsheet():
    pass


# ── User management ──
def generate_password(length=8):
    """Generate a random password like: IMEMSA-Xx9y"""
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"IM-{random_part}"


def find_user_by_email(email):
    client = get_client()
    response = client.table("usuarios").select("*").eq("correo", email.strip().lower()).execute()
    if response.data:
        return _to_app_cols(response.data[0])
    # Try case-insensitive search
    users = get_all_records(C.HOJA_USUARIOS)
    for u in users:
        if u.get("Correo", "").strip().lower() == email.strip().lower():
            return u
    return None


def get_user_phone(email):
    """Get phone number for a user by email."""
    user = find_user_by_email(email)
    return str(user.get("Telefono", "")) if user else ""


def validate_domain(email):
    return any(email.strip().lower().endswith(d) for d in C.DOMINIOS_PERMITIDOS)


def auto_register_users(activities_df):
    existing_users = get_all_records(C.HOJA_USUARIOS)
    existing_emails = {u["Correo"].strip().lower() for u in existing_users}
    new_users = []
    discrepancies = []
    seen_emails = set()

    for _, row in activities_df.iterrows():
        email = str(row.get("Correo", "")).strip().lower()
        if not email or email in seen_emails:
            continue
        seen_emails.add(email)

        if email in existing_emails:
            existing = next(u for u in existing_users if u["Correo"].strip().lower() == email)
            if str(existing.get("Telefono", "")) != str(row.get("Telefono", "")):
                discrepancies.append({
                    "email": email,
                    "campo": "Teléfono",
                    "existente": existing.get("Telefono", ""),
                    "nuevo": row.get("Telefono", "")
                })
        else:
            if validate_domain(email):
                uid = get_next_id("USR-", C.HOJA_USUARIOS, "ID_Usuario")
                pwd = generate_password()
                new_user = {
                    "ID_Usuario": uid,
                    "Nombre": str(row.get("Responsable", "")),
                    "Correo": email,
                    "Telefono": str(row.get("Telefono", "")),
                    "Area": "",
                    "Rol": "Responsable",
                    "Activo": "Sí",
                    "Password": pwd
                }
                append_row(C.HOJA_USUARIOS, list(new_user.values()))
                new_users.append(new_user)
                existing_emails.add(email)

    return new_users, discrepancies


# ── Log ──
def log_action(usuario, accion, entidad, id_entidad, detalle=""):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_id = f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        append_row(C.HOJA_LOG, [log_id, now, usuario, accion, entidad, id_entidad, detalle])
    except Exception:
        pass
