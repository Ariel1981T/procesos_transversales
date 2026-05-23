# 📋 Plataforma de Procesos Transversales — Grupo IMEMSA

Sistema configurable para la creación, gestión y seguimiento de procesos transversales del Grupo IMEMSA.

## 🏗️ Arquitectura

| Componente | Tecnología |
|------------|------------|
| Frontend | Streamlit |
| Backend | Google Sheets (gspread) |
| Archivos | Cloudinary |
| Notificaciones | Gmail SMTP |
| Deploy | Streamlit Cloud |

## 📁 Estructura del Proyecto

```
imemsa-procesos/
├── app.py                  # Aplicación principal
├── config.py               # Constantes y configuración
├── sheets_manager.py       # Operaciones con Google Sheets
├── notifications.py        # Motor de notificaciones por correo
├── styles.py               # CSS personalizado y componentes visuales
├── requirements.txt        # Dependencias Python
├── secrets_template.toml   # Plantilla de secrets
└── .streamlit/
    └── config.toml         # Configuración de Streamlit
```

## 🚀 Despliegue

### 1. Crear Google Spreadsheet
- Crear un nuevo Google Spreadsheet vacío
- Compartirlo con el correo de la Service Account (permisos de Editor)
- Copiar el ID del spreadsheet (de la URL)

### 2. Subir a GitHub
```bash
git init
git add .
git commit -m "Plataforma de Procesos Transversales v1.0"
git remote add origin https://github.com/TU-USUARIO/imemsa-procesos.git
git push -u origin main
```

### 3. Configurar Streamlit Cloud
- Conectar el repositorio en [share.streamlit.io](https://share.streamlit.io)
- En Settings > Secrets, pegar el contenido de `secrets_template.toml` con valores reales
- Deploy

### 4. Inicializar Base de Datos
- Ingresar a la app como Admin
- Ir a ⚙️ Admin > Inicializar BD
- Esto crea las 9 hojas con sus encabezados

### 5. Crear Primer Usuario
- En Google Sheets, agregar manualmente el primer usuario Admin en la hoja `Usuarios`:
  ```
  USR-001 | Tu Nombre | tucorreo@imemsa.com.mx | 5500000000 | TI | Admin | Sí
  ```

## 👥 Roles

| Rol | Permisos |
|-----|----------|
| **Admin** | Acceso total, inicializar BD, gestionar usuarios |
| **PM** | Generar autorizaciones, dashboard global, ver todos los procesos |
| **Gerente** | Crear plantillas, lanzar instancias, ver sus procesos |
| **Responsable** | Ver y completar sus tareas, subir evidencias |

## 📋 Flujo de Uso

1. **PM** genera un número de confirmación para el gerente
2. **Gerente** sube su Excel con las actividades del proceso
3. El sistema crea la plantilla y registra nuevos usuarios automáticamente
4. **Gerente** lanza una instancia desde la plantilla
5. **Responsables** reciben notificaciones y completan sus tareas
6. El sistema avanza secuencialmente y notifica en cada paso

## 🔧 Dominios Permitidos

- @imemsa.com.mx
- @equipodelmar.com.mx
- @imeembarcaciones.com.mx
- @equiposeamex.com.mx
