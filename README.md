# Simple Blog Platform

Sistema de blog completo con autenticación de usuarios, sistema de roles y funcionalidades avanzadas desarrollado con Django.

## 📋 Características

### Autenticación y Roles
- ✅ Sistema de autenticación completo (registro, login, logout)
- ✅ Verificación de email
- ✅ Recuperación de contraseña
- ✅ Sistema de roles (Admin, Autor, Lector)
- ✅ Contraseñas hasheadas con Argon2

### Blog y Contenido
- ✅ CRUD de publicaciones con editor rico
- ✅ Sistema de comentarios anidados
- ✅ Categorías y etiquetas
- ✅ Búsqueda y filtrado avanzado

### Panel de Administración
- ✅ **Dashboard de administración** con estadísticas del sistema
- ✅ **Sistema de monitoreo de logs** exclusivo para administradores
- ✅ **Visor de logs** con filtros avanzados (tipo, nivel, búsqueda)
- ✅ **4 tipos de logs** (general, error, security, database)
- ✅ **Rotación automática** de logs (10MB, hasta 5 backups)
- ✅ **Descarga y limpieza** de logs con backup automático
- ✅ **Estado del sistema** (versiones, BD, servicios, espacio)

### Seguridad
- ✅ Seguridad robusta (protección XSS, CSRF, SQL Injection)
- ✅ Rate limiting para prevenir ataques de fuerza bruta
- ✅ Control de acceso basado en roles
- ✅ Logs de auditoría para eventos de seguridad

## 🛠️ Tecnologías

- **Backend:** Python 3.11+, Django 5.0
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Seguridad:** Argon2, Django Security Middleware, CSP Headers
- **Logging:** RotatingFileHandler con rotación automática
- **Testing:** pytest, coverage

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd Simple_Blog_Platform
```

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones.

### 5. Crear base de datos y migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Visita: http://127.0.0.1:8000/

## 📚 Documentación

La documentación completa del proyecto incluye:

### Documentación Principal
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Documentación completa del sistema:
  1. Definición de requisitos (funcionales y no funcionales)
  2. Arquitectura del sistema (MTV/MVC)
  3. Tecnologías y justificación
  4. Diseño del sistema de autenticación paso a paso
  5. Reglas de seguridad
  6. Modelo de base de datos
  7. Flujo de desarrollo
  8. Buenas prácticas
  9. Pruebas y validación

### Documentación del Admin Panel
- **[ADMIN_LOG_SYSTEM.md](ADMIN_LOG_SYSTEM.md)** - Sistema de monitoreo de logs:
  - Descripción general y control de acceso
  - Estructura del sistema de logs
  - Funcionalidades del admin panel
  - Tipos de eventos registrados
  - Configuración técnica
  - Casos de uso y mejores prácticas
  - Mantenimiento y soporte

- **[TESTING_ADMIN_LOGS.md](TESTING_ADMIN_LOGS.md)** - Guía de prueba del sistema de logs:
  - Pre-requisitos y configuración
  - Pruebas paso a paso de todas las funcionalidades
  - Verificación de seguridad y control de acceso
  - Checklist completo de verificación
  - Troubleshooting común

## 🚀 Uso Rápido

### Crear un post

1. Inicia sesión como usuario con rol "Autor" o "Admin"
2. Ve a "Crear Publicación"
3. Completa el formulario
4. Publica o guarda como borrador

### Sistema de Roles

- **Admin:** Acceso total al sistema + Panel de administración con monitoreo de logs
- **Autor:** Puede crear, editar y eliminar sus propias publicaciones
- **Lector:** Puede ver publicaciones y comentar

### Acceder al Admin Panel (Solo Administradores)

1. Inicia sesión como usuario con rol "Admin"
2. Click en el enlace "🔒 Admin Panel" en la navbar
3. O navega directamente a: http://127.0.0.1:8000/admin-panel/

**Funcionalidades disponibles:**
- **Dashboard:** Estadísticas de usuarios, contenido, top posts, actividad reciente
- **Logs:** Visor con filtros por tipo, nivel de severidad y búsqueda de texto
- **Descargas:** Descargar logs completos para análisis offline
- **Limpieza:** Limpiar logs con backup automático
- **Sistema:** Estado del sistema, base de datos, servicios y espacio de logs

### Generar Logs de Prueba

```bash
python generate_test_logs.py
```

Esto crea logs de ejemplo en 4 categorías: general, error, security y database.

## 🧪 Testing

Ejecutar todos los tests:

```bash
python manage.py test
```

Con coverage:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML en htmlcov/
```

## 🔒 Seguridad

El proyecto implementa múltiples capas de seguridad:

- **Contraseñas:** Hasheadas con Argon2 (resistente a GPU cracking)
- **CSRF Protection:** Tokens en todos los formularios
- **XSS Protection:** Auto-escape en templates + CSP headers
- **SQL Injection:** ORM de Django (sin SQL crudo)
- **Rate Limiting:** Máximo 5 intentos de login por minuto
- **Sesiones Seguras:** HttpOnly, Secure, SameSite cookies
- **HTTPS:** Obligatorio en producción

## 📁 Estructura del Proyecto

```
Simple_Blog_Platform/
├── accounts/                    # App de autenticación
│   ├── models.py               # Modelo de usuario personalizado
│   ├── views.py                # Vistas de auth
│   ├── forms.py                # Formularios de registro/login
│   ├── urls.py                 # Rutas de autenticación
│   └── templates/              # Templates de auth
├── blog/                       # App del blog
│   ├── models.py               # Posts, Comments, Categories, Tags
│   ├── views.py                # Vistas CRUD
│   ├── forms.py                # Formularios del blog
│   └── templates/              # Templates del blog
├── admin_panel/                # App de administración (NUEVO)
│   ├── views.py                # Vistas de monitoreo y logs
│   ├── urls.py                 # Rutas del admin panel
│   └── templates/
│       └── admin_panel/
│           ├── dashboard.html  # Dashboard de administración
│           ├── logs.html       # Visor de logs
│           └── system_status.html  # Estado del sistema
├── blog_platform/              # Configuración del proyecto
│   ├── settings.py             # Configuración principal + LOGGING
│   ├── urls.py                 # Rutas principales
│   └── wsgi.py                 # WSGI config
├── logs/                       # Sistema de logs (NUEVO)
│   ├── general.log             # Logs generales (10MB, 5 backups)
│   ├── error.log               # Logs de errores
│   ├── security.log            # Logs de seguridad
│   └── database.log            # Logs de base de datos
├── static/                     # Archivos estáticos
├── media/                      # Uploads de usuarios
├── templates/                  # Templates base
├── manage.py                   # CLI de Django
├── requirements.txt            # Dependencias
├── generate_test_logs.py       # Script para generar logs de prueba (NUEVO)
├── .env.example                # Variables de entorno ejemplo
├── .gitignore                  # Git ignore
├── README.md                   # Este archivo
├── DOCUMENTATION.md            # Documentación completa
├── ADMIN_LOG_SYSTEM.md         # Documentación del sistema de logs (NUEVO)
└── TESTING_ADMIN_LOGS.md       # Guía de prueba de logs (NUEVO)
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Usar **black** para formateo: `black .`
- Pasar **flake8** linting: `flake8 .`
- Tests con cobertura > 80%
- Docstrings en funciones y clases

## 📝 Changelog

### [1.1.0] - 2026-01-09

#### Añadido
- ✨ **Sistema de monitoreo de logs exclusivo para administradores**
- 📊 Dashboard de administración con estadísticas en tiempo real
- 📝 Visor de logs con filtros avanzados (tipo, nivel, búsqueda)
- 📁 4 tipos de logs: general, error, security, database
- 🔄 Rotación automática de logs (10MB, hasta 5 backups)
- ⬇️ Funcionalidad de descarga de logs
- 🧹 Limpieza de logs con backup automático
- 🖥️ Página de estado del sistema (versiones, BD, servicios)
- 🔒 Control de acceso basado en roles para admin panel
- 📚 Documentación completa del sistema de logs
- 🧪 Guía de prueba paso a paso
- 🛠️ Script para generar logs de prueba

### [1.0.0] - 2026-01-09

#### Añadido
- Sistema de autenticación completo
- Modelos de blog (Post, Comment, Category, Tag)
- Sistema de roles y permisos
- Verificación de email
- Recuperación de contraseña
- Rate limiting
- Tests unitarios y de seguridad
- Documentación completa
