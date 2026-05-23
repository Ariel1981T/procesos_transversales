"""
Configuración global de la Plataforma de Procesos Transversales IMEMSA
"""

# ── Branding ──
NAVY = "#0D2B6E"
RED = "#C41E2E"
GREEN = "#28a745"
YELLOW = "#ffc107"
LIGHT_BG = "#F0F4FA"
WHITE = "#FFFFFF"

# ── Dominios permitidos del Grupo IMEMSA ──
DOMINIOS_PERMITIDOS = [
    "@imemsa.com.mx",
    "@equipodelmar.com.mx",
    "@imeembarcaciones.com.mx",
    "@equiposeamex.com.mx",
]

# ── Roles del sistema ──
ROLES = ["PM", "Gerente", "Responsable", "Admin"]

# ── Estatus de autorizaciones ──
ESTATUS_AUTORIZACION = ["Vigente", "Consumida", "Vencida", "Revocada"]
TIPOS_AUTORIZACION = ["Nueva Plantilla", "Nueva Instancia"]

# ── Estatus de plantillas ──
ESTATUS_PLANTILLA = ["Borrador", "Activa", "Archivada"]

# ── Estatus de instancias ──
ESTATUS_INSTANCIA = ["En Proceso", "Completado", "Cancelado"]

# ── Estatus de actividades ──
ESTATUS_ACTIVIDAD = ["Pendiente", "Activa", "Completada", "Vencida"]

# ── Vigencia por defecto de autorizaciones (días) ──
VIGENCIA_AUTORIZACION_DIAS = 30

# ── Días de anticipación para alerta amarilla ──
DIAS_ALERTA_AMARILLA = 2

# ── Columnas esperadas en el Excel de carga ──
COLUMNAS_EXCEL_OBLIGATORIAS = ["No.", "Fase", "Actividad", "Responsable", "Correo", "Telefono", "Días teoricos"]
COLUMNAS_EXCEL_OPCIONALES = ["Descripción", "Evidencia requerida"]

# ── Nombres de hojas en Google Sheets ──
HOJA_USUARIOS = "Usuarios"
HOJA_AUTORIZACIONES = "Autorizaciones"
HOJA_PLANTILLAS = "Plantillas"
HOJA_ACTIVIDADES_PLANTILLA = "Actividades_Plantilla"
HOJA_INSTANCIAS = "Instancias"
HOJA_AVANCE = "Avance_Instancia"
HOJA_EVIDENCIAS = "Evidencias"
HOJA_COMENTARIOS = "Comentarios"
HOJA_LOG = "Log_Sistema"

# ── Headers de cada hoja ──
HEADERS = {
    HOJA_USUARIOS: ["ID_Usuario", "Nombre", "Correo", "Telefono", "Area", "Rol", "Activo"],
    HOJA_AUTORIZACIONES: ["ID_Autorizacion", "Tipo", "Solicitante", "Area", "Nombre_Proceso",
                          "PM_Emisor", "Fecha_Emision", "Fecha_Vencimiento", "Estatus",
                          "ID_Vinculado", "Fecha_Consumo"],
    HOJA_PLANTILLAS: ["ID_Plantilla", "Nombre", "Descripcion", "Area_Origen", "Gerente_Creador",
                      "Fecha_Creacion", "Version", "Estatus", "Num_Actividades", "Num_Fases",
                      "Veces_Utilizada", "ID_Autorizacion", "Dias_Teoricos_Total"],
    HOJA_ACTIVIDADES_PLANTILLA: ["ID_Actividad_TPL", "ID_Plantilla", "Numero", "Fase", "Actividad",
                                  "Descripcion", "Responsable", "Correo", "Telefono",
                                  "Dias_Teoricos", "Evidencia_Requerida"],
    HOJA_INSTANCIAS: ["ID_Instancia", "ID_Plantilla", "Nombre_Instancia", "Descripcion",
                      "Gerente_Responsable", "Fecha_Creacion", "Fecha_Estimada_Fin",
                      "Fecha_Real_Fin", "Estatus", "Porcentaje_Avance", "ID_Autorizacion",
                      "Unidades", "Importe"],
    HOJA_AVANCE: ["ID_Avance", "ID_Instancia", "Numero_Actividad", "Actividad", "Fase",
                  "Responsable", "Correo", "Dias_Teoricos", "Fecha_Inicio", "Fecha_Limite",
                  "Fecha_Cierre", "Estatus", "Dias_Reales", "Desviacion",
                  "Evidencia_Requerida", "Tiene_Evidencia"],
    HOJA_EVIDENCIAS: ["ID_Evidencia", "ID_Instancia", "Numero_Actividad", "Nombre_Archivo",
                      "URL_Cloudinary", "Public_ID", "Fecha_Subida", "Subido_Por"],
    HOJA_COMENTARIOS: ["ID_Comentario", "ID_Instancia", "Numero_Actividad", "Autor",
                       "Fecha", "Texto"],
    HOJA_LOG: ["ID_Log", "Fecha_Hora", "Usuario", "Accion", "Entidad", "ID_Entidad", "Detalle"],
}
