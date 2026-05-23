"""
Gestión de datos en Google Sheets para la Plataforma de Procesos Transversales
Versión optimizada con caché agresivo para evitar rate limiting de Google API.
"""
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime, timedelta
import json
import time
import config as C

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource(ttl=600)
def get_client():
    raw = st.secrets["gcp_service_account"]
    if isinstance(raw, str):
        creds_dict = json.loads(raw)
    else:
        creds_dict = dict(raw)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_resource(ttl=600)
def _get_spreadsheet():
    client = get_client()
    return client.open_by_key(st.secrets["spreadsheet_id"])


@st.cache_resource(ttl=600)
def _get_ws(name):
    """Cache worksheet references to avoid repeated API calls."""
    ss = _get_spreadsheet()
    try:
        return ss.worksheet(name)
    except gspread.exceptions.WorksheetNotFound:
        ws = ss.add_worksheet(title=name, rows=1000, cols=20)
        headers = C.HEADERS.get(name, [])
        if headers:
            ws.update("A1", [headers])
        return ws


def _retry(func, max_retries=4, base_delay=3):
    """Execute with retry and exponential backoff for 429 errors."""
    for attempt in range(max_retries):
        try:
            return func()
        except gspread.exceptions.APIError as e:
            error_code = getattr(e, 'response', None)
            status = error_code.status_code if error_code else 0
            if attempt < max_retries - 1:
                wait = base_delay * (2 ** attempt)  # 3, 6, 12, 24 seconds
                time.sleep(wait)
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(base_delay)
            else:
                raise e


# ── In-memory cache for sheet data ──
if "_sheets_cache" not in st.session_state:
    st.session_state._sheets_cache = {}
if "_sheets_cache_time" not in st.session_state:
    st.session_state._sheets_cache_time = {}

CACHE_TTL = 30  # seconds


def get_all_records(sheet_name):
    """Read all records with in-memory session cache."""
    cache = st.session_state._sheets_cache
    cache_time = st.session_state._sheets_cache_time
    now = time.time()

    # Return cached if fresh
    if sheet_name in cache and sheet_name in cache_time:
        if now - cache_time[sheet_name] < CACHE_TTL:
            return cache[sheet_name]

    # Fetch from API with retry
    def _do():
        ws = _get_ws(sheet_name)
        return ws.get_all_records()

    data = _retry(_do)
    cache[sheet_name] = data
    cache_time[sheet_name] = now
    return data


def _invalidate(sheet_name):
    """Mark a specific sheet cache as stale."""
    if sheet_name in st.session_state._sheets_cache_time:
        st.session_state._sheets_cache_time[sheet_name] = 0


def _invalidate_all():
    """Mark all caches as stale."""
    st.session_state._sheets_cache_time = {}


def append_row(sheet_name, row_data):
    def _do():
        ws = _get_ws(sheet_name)
        ws.append_row(row_data, value_input_option="USER_ENTERED")
    _retry(_do)
    _invalidate(sheet_name)


def update_cell_by_id(sheet_name, id_column, id_value, target_column, new_value):
    def _do():
        ws = _get_ws(sheet_name)
        records = ws.get_all_values()
        if not records:
            return False
        headers = records[0]
        id_col_idx = headers.index(id_column) if id_column in headers else -1
        tgt_col_idx = headers.index(target_column) if target_column in headers else -1
        if id_col_idx < 0 or tgt_col_idx < 0:
            return False
        for i, row in enumerate(records[1:], start=2):
            if row[id_col_idx] == str(id_value):
                ws.update_cell(i, tgt_col_idx + 1, new_value)
                return True
        return False
    result = _retry(_do)
    _invalidate(sheet_name)
    return result


def update_row_by_id(sheet_name, id_column, id_value, updates_dict):
    def _do():
        ws = _get_ws(sheet_name)
        records = ws.get_all_values()
        if not records:
            return False
        headers = records[0]
        id_col_idx = headers.index(id_column) if id_column in headers else -1
        if id_col_idx < 0:
            return False
        for i, row in enumerate(records[1:], start=2):
            if row[id_col_idx] == str(id_value):
                # Batch update: build range and values
                for col_name, value in updates_dict.items():
                    if col_name in headers:
                        col_idx = headers.index(col_name)
                        ws.update_cell(i, col_idx + 1, str(value))
                return True
        return False
    result = _retry(_do)
    _invalidate(sheet_name)
    return result


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
        if aid.startswith(prefix):
            try:
                nums.append(int(aid.split("-")[-1]))
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
        if iid.startswith(prefix):
            try:
                nums.append(int(iid.split("-")[-1]))
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


# ── Initialize spreadsheet ──
def init_spreadsheet():
    for sheet_name in C.HEADERS:
        _get_ws(sheet_name)
        time.sleep(2)


# ── User management ──
def find_user_by_email(email):
    users = get_all_records(C.HOJA_USUARIOS)
    for u in users:
        if u.get("Correo", "").strip().lower() == email.strip().lower():
            return u
    return None


def validate_domain(email):
    return any(email.strip().lower().endswith(d) for d in C.DOMINIOS_PERMITIDOS)


def auto_register_users(activities_df):
    existing_users = get_all_records(C.HOJA_USUARIOS)
    existing_emails = {u["Correo"].strip().lower() for u in existing_users}
    new_users = []
    discrepancies = []

    for _, row in activities_df.iterrows():
        email = str(row.get("Correo", "")).strip().lower()
        if not email or email in [e.strip().lower() for e in [u["Correo"] for u in new_users if "Correo" in u]]:
            continue

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
                new_user = {
                    "ID_Usuario": uid,
                    "Nombre": str(row.get("Responsable", "")),
                    "Correo": email,
                    "Telefono": str(row.get("Telefono", "")),
                    "Area": "",
                    "Rol": "Responsable",
                    "Activo": "Sí"
                }
                append_row(C.HOJA_USUARIOS, list(new_user.values()))
                new_users.append(new_user)
                existing_emails.add(email)
                time.sleep(1)

    return new_users, discrepancies


# ── Log (non-blocking) ──
def log_action(usuario, accion, entidad, id_entidad, detalle=""):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_id = f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        append_row(C.HOJA_LOG, [log_id, now, usuario, accion, entidad, id_entidad, detalle])
    except Exception:
        pass  # Log errors should never break the app
