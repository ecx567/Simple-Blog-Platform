# 📰 Simple Blog Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Sistema de blog profesional con autenticación avanzada, roles de usuario y panel de administración con monitoreo en tiempo real**

[Características](#-características-principales) • [Instalación](#-guía-de-instalación) • [Uso](#-guía-de-uso) • [Arquitectura](#-arquitectura-del-sistema) • [Documentación](#-documentación-completa)

</div>

---

## 📋 Características Principales

### 🔐 Autenticación y Seguridad
- **Sistema de autenticación completo** con email y contraseña
- **Verificación de email** mediante tokens de seguridad
- **Recuperación de contraseña** con enlaces temporales
- **Sistema de roles** jerárquico (Administrador, Autor, Lector)
- **Argon2 Password Hashing** resistente a ataques de fuerza bruta
- **Rate Limiting** configurable por endpoint
- **CSRF Protection** en todos los formularios
- **XSS Protection** con auto-escape de templates
- **SQL Injection Prevention** mediante ORM de Django
- **Content Security Policy (CSP)** headers configurados

### 📝 Gestión de Contenido
- **CRUD completo** de publicaciones con interfaz intuitiva
- **Sistema de comentarios anidados** (respuestas a comentarios)
- **Categorías y etiquetas** para organización
- **Búsqueda full-text** con filtros avanzados
- **Paginación automática** de resultados
- **Contador de vistas** por publicación
- **Sistema de borradores** y publicaciones
- **Slugs automáticos** para URLs amigables
- **Imágenes destacadas** con gestión de archivos
- **Tiempo de lectura estimado** calculado automáticamente

### 👨‍💼 Panel de Administración
- **Dashboard con estadísticas** en tiempo real del sistema
- **Sistema de monitoreo de logs** con 4 categorías independientes
- **Visor de logs interactivo** con filtros por tipo, nivel y búsqueda
- **Rotación automática** de logs (10MB por archivo, hasta 5 backups)
- **Descarga de logs** para análisis offline
- **Limpieza de logs** con backup automático de seguridad
- **Estado del sistema** mostrando versiones, BD, servicios y espacio
- **Gráficas de actividad** de usuarios y contenido
- **Control total** exclusivo para administradores

### 🎨 Interfaz de Usuario
- **Diseño responsive** con Bootstrap 5
- **Iconos de Bootstrap Icons** para mejor UX
- **Tema moderno y limpio** con paleta de colores profesional
- **Navegación intuitiva** con menús contextuales
- **Mensajes flash** para feedback del usuario
- **Formularios validados** en cliente y servidor
- **Carga de imágenes** con preview
- **Modo de lectura** optimizado para posts

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Python** | 3.11+ | Lenguaje base del proyecto |
| **Django** | 5.0.1 | Framework web MTV/MVC |
| **Argon2** | Latest | Hashing de contraseñas seguro |
| **django-ratelimit** | Latest | Protección contra fuerza bruta |

### Frontend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Bootstrap** | 5.3 | Framework CSS responsive |
| **Bootstrap Icons** | 1.11 | Iconografía moderna |
| **JavaScript** | ES6+ | Interactividad del cliente |
| **HTML5/CSS3** | Latest | Estructura y estilos |

### Base de Datos
| Tecnología | Uso | Propósito |
|-----------|-----|-----------|
| **SQLite** | Desarrollo | BD ligera para desarrollo local |
| **PostgreSQL** | Producción | BD robusta para producción |

### Seguridad y Monitoreo
- **CSRF Middleware** - Protección contra ataques CSRF
- **XSS Protection** - Auto-escape de templates
- **CSP Headers** - Content Security Policy
- **RotatingFileHandler** - Sistema de logs con rotación
- **Secure Sessions** - Cookies HttpOnly y Secure

---

## 📊 Arquitectura del Sistema

### Patrón MTV (Model-Template-View)

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTE                             │
│                    (Navegador Web)                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO MIDDLEWARE                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Security │  │   CSRF   │  │   Auth   │  │ Sessions │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      URL ROUTER                             │
│              blog_platform/urls.py                          │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ accounts │  │   blog   │  │  admin   │  │  static  │   │
│  │  /urls   │  │  /urls   │  │  /urls   │  │  files   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   VIEWS     │  │   VIEWS     │  │   VIEWS     │
│  accounts   │  │    blog     │  │admin_panel  │
│             │  │             │  │             │
│ • register  │  │ • post_list │  │ • dashboard │
│ • login     │  │ • post_crud │  │ • view_logs │
│ • logout    │  │ • comments  │  │ • sys_status│
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      MODELS (ORM)                            │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   User   │  │   Post   │  │ Comment  │  │ Category │   │
│  │          │  │          │  │          │  │          │   │
│  │ • email  │  │ • title  │  │ • user   │  │ • name   │   │
│  │ • role   │  │ • content│  │ • post   │  │ • slug   │   │
│  │ • active │  │ • author │  │ • parent │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS                             │
│            SQLite (Dev) / PostgreSQL (Prod)                  │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Autenticación

```
Usuario Visita /accounts/login/
         │
         ▼
┌────────────────────┐
│  LoginView         │
│  (accounts/views)  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐      ┌─────────────┐
│  LoginForm         │◄─────┤ POST Data   │
│  (accounts/forms)  │      └─────────────┘
└────────┬───────────┘
         │ Validación
         ▼
┌────────────────────┐
│  authenticate()    │
│  (Django Auth)     │
└────────┬───────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────────┐
│ FAIL  │ │  SUCCESS  │
└───┬───┘ └─────┬─────┘
    │           │
    │           ▼
    │     ┌──────────────┐
    │     │  auth_login()│
    │     └──────┬───────┘
    │            │
    │            ▼
    │     ┌──────────────┐
    │     │ Crear Sesión │
    │     └──────┬───────┘
    │            │
    │            ▼
    │     ┌──────────────┐
    │     │  Rate Limit  │
    │     │   Check      │
    │     └──────┬───────┘
    │            │
    ▼            ▼
┌────────────────────────┐
│  Mensaje de Error      │
│  Redirigir a Login     │
└────────────────────────┘
         │
         ▼
┌────────────────────────┐
│  Actualizar last_login │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│  Redirigir a Dashboard │
└────────────────────────┘
```

### Flujo de Creación de Post

```
Autor hace click en "Nueva Publicación"
         │
         ▼
┌────────────────────┐
│ @login_required    │◄── Si no auth → Login
│ @author_required   │◄── Si no autor → 403
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  post_create()     │
│  GET Request       │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  PostForm()        │
│  Formulario vacío  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Renderizar         │
│ post_form.html     │
└────────────────────┘
         │
         │ Usuario llena formulario
         │ y hace submit
         ▼
┌────────────────────┐
│  post_create()     │
│  POST Request      │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  PostForm(POST)    │
│  + FILES           │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  form.is_valid()   │
└────────┬───────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌─────────────┐
│ FAIL  │ │   SUCCESS   │
└───┬───┘ └──────┬──────┘
    │            │
    │            ▼
    │     ┌─────────────┐
    │     │ save(commit │
    │     │   =False)   │
    │     └──────┬──────┘
    │            │
    │            ▼
    │     ┌─────────────┐
    │     │ Set author  │
    │     │ = req.user  │
    │     └──────┬──────┘
    │            │
    │            ▼
    │     ┌─────────────┐
    │     │ Auto-genera │
    │     │    slug     │
    │     └──────┬──────┘
    │            │
    │            ▼
    │     ┌─────────────┐
    │     │ save() en BD│
    │     └──────┬──────┘
    │            │
    │            ▼
    │     ┌─────────────┐
    │     │ save_m2m()  │
    │     │   (tags)    │
    │     └──────┬──────┘
    │            │
    ▼            ▼
┌────────────────────────┐
│ Mostrar errores        │
│ Re-renderizar form     │
└────────────────────────┘
         │
         ▼
┌────────────────────────┐
│ Log evento en          │
│ general.log            │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Mensaje success        │
│ Redirect post_detail   │
└────────────────────────┘
```

### Flujo del Sistema de Logs

```
┌─────────────────────────────────────────────────────────┐
│                    EVENTO DEL SISTEMA                    │
│   (Login, Error, Query BD, Acceso no autorizado)       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  LOGGER (logging module)                 │
│                                                          │
│  logger.info()  │  logger.error()  │  logger.warning() │
│  logger.debug() │  logger.critical()                    │
└────────────────────────┬────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Formatter  │ │   Formatter  │ │   Formatter  │
│   (verbose)  │ │   (simple)   │ │   (verbose)  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Handler    │ │   Handler    │ │   Handler    │
│ file_general │ │   console    │ │ file_security│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│              ROTATING FILE HANDLERS                      │
│                                                          │
│  general.log    error.log    security.log   database.log│
│  (10MB/5)       (10MB/5)     (10MB/5)       (10MB/3)    │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Cuando archivo > 10MB
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  ROTACIÓN AUTOMÁTICA                     │
│                                                          │
│  general.log  →  general.log.1                          │
│  general.log.1  →  general.log.2                        │
│  general.log.4  →  general.log.5                        │
│  general.log.5  →  ELIMINADO                            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              ADMIN ACCEDE A /admin-panel/logs/           │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 @admin_required decorator                │
│             Verificar user.is_admin == True              │
└────────────────────────┬────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │         │
                    ▼         ▼
            ┌──────────┐ ┌────────────┐
            │   DENY   │ │   ALLOW    │
            │   403    │ └─────┬──────┘
            └──────────┘       │
                               ▼
                    ┌────────────────────┐
                    │   view_logs()      │
                    │   Lee archivo log  │
                    └─────┬──────────────┘
                          │
                          ▼
                    ┌────────────────────┐
                    │  parse_log_line()  │
                    │  Extrae:           │
                    │  • Nivel           │
                    │  • Timestamp       │
                    │  • Módulo          │
                    │  • Mensaje         │
                    └─────┬──────────────┘
                          │
                          ▼
                    ┌────────────────────┐
                    │  Aplicar Filtros:  │
                    │  • Tipo (general)  │
                    │  • Nivel (ERROR)   │
                    │  • Búsqueda (text) │
                    └─────┬──────────────┘
                          │
                          ▼
                    ┌────────────────────┐
                    │  Paginar (50/pag)  │
                    └─────┬──────────────┘
                          │
                          ▼
                    ┌────────────────────┐
                    │ Renderizar logs.html│
                    │ con logs filtrados │
                    └────────────────────┘
```

---

## 📦 Guía de Instalación

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.11 o superior** - [Descargar Python](https://www.python.org/downloads/)
- **pip** (gestor de paquetes de Python)
- **Git** - [Descargar Git](https://git-scm.com/downloads)
- **(Opcional) PostgreSQL** - Para producción

### Paso 1: Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/tu-usuario/Simple_Blog_Platform.git

# Entrar al directorio
cd Simple_Blog_Platform
```

### Paso 2: Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de política de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

**Lista de paquetes principales:**
```
Django==5.0.1
argon2-cffi==23.1.0
django-crispy-forms==2.1
crispy-bootstrap5==2.0.0
django-ratelimit==4.1.0
python-dotenv==1.0.0
Pillow==10.2.0
```

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu editor preferido
nano .env  # o vim, code, notepad, etc.
```

**Configuración básica (.env):**
```env
# Django Settings
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (opcional - usa SQLite por defecto)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=blog_platform
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_app
```

### Paso 5: Configurar Base de Datos

```bash
# Crear directorios necesarios
mkdir logs
mkdir media
mkdir static

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (administrador)
python manage.py createsuperuser
```

**Datos del superusuario:**
```
Email: admin@example.com
Username: admin
Password: (mínimo 8 caracteres, mayúscula, minúscula, número, especial)
```

### Paso 6: Cargar Datos de Ejemplo (Opcional)

```bash
# Crear categorías de ejemplo
python manage.py shell
```

```python
from blog.models import Category, Tag

# Crear categorías
Category.objects.create(name='Python', description='Tutoriales de Python')
Category.objects.create(name='Django', description='Framework Django')
Category.objects.create(name='JavaScript', description='JS y frameworks')

# Crear tags
Tag.objects.create(name='tutorial')
Tag.objects.create(name='intermedio')
Tag.objects.create(name='avanzado')

exit()
```

### Paso 7: Generar Logs de Prueba

```bash
# Generar logs de ejemplo para el admin panel
python generate_test_logs.py
```

### Paso 8: Ejecutar Servidor de Desarrollo

```bash
# Iniciar servidor
python manage.py runserver

# O especificar puerto personalizado
python manage.py runserver 8080
```

**Acceder a la aplicación:**
- **Frontend:** http://127.0.0.1:8000/
- **Admin Django:** http://127.0.0.1:8000/admin/
- **Admin Panel Custom:** http://127.0.0.1:8000/admin-panel/

### Paso 9: Verificar Instalación

```bash
# Ejecutar tests
python manage.py test

# Verificar cobertura
coverage run --source='.' manage.py test
coverage report
coverage html

# Abrir reporte de cobertura
# El archivo estará en htmlcov/index.html
```

### Paso 10: Crear Usuarios de Prueba

```bash
python manage.py shell
```

```python
from accounts.models import CustomUser

# Crear autor
autor = CustomUser.objects.create_user(
    email='autor@example.com',
    username='autor1',
    password='Password123!',
    role='author',
    is_active=True,
    is_email_verified=True
)

# Crear lector
lector = CustomUser.objects.create_user(
    email='lector@example.com',
    username='lector1',
    password='Password123!',
    role='reader',
    is_active=True,
    is_email_verified=True
)

print("✅ Usuarios de prueba creados")
exit()
```

---

## 🚀 Guía de Uso

### Para Usuarios Lectores

#### 1. Registro de Cuenta

```
1. Navegar a http://127.0.0.1:8000/accounts/register/
2. Completar el formulario:
   - Email: tu_email@example.com
   - Username: tu_usuario
   - Contraseña: Mínimo 8 caracteres, incluir mayúscula, minúscula, número y especial
3. Click en "Registrarse"
4. Verificar email (modo desarrollo: ver consola del servidor)
5. Click en el enlace de verificación
6. ¡Cuenta activada!
```

#### 2. Inicio de Sesión

```
1. Ir a http://127.0.0.1:8000/accounts/login/
2. Ingresar email y contraseña
3. (Opcional) Marcar "Recuérdame" para mantener sesión 2 semanas
4. Click en "Iniciar Sesión"
5. Redirigido a Dashboard personalizado
```

#### 3. Explorar Publicaciones

```
1. Click en "Blog" en la navbar
2. Usar filtros disponibles:
   - Búsqueda por texto
   - Filtrar por categoría
   - Filtrar por etiqueta
   - Ordenar por fecha o vistas
3. Click en una publicación para ver detalles
4. Leer contenido completo
5. Ver comentarios de otros usuarios
```

#### 4. Comentar en Posts

```
1. Abrir una publicación
2. Scroll hasta la sección de comentarios
3. Escribir comentario en el formulario
4. Click en "Publicar Comentario"
5. Para responder a un comentario:
   - Click en "Responder"
   - Escribir respuesta
   - Click en "Publicar Respuesta"
```

#### 5. Gestionar Perfil

```
1. Click en tu nombre de usuario (navbar)
2. Seleccionar "Perfil"
3. Ver información personal
4. Editar nombre, apellido (email no editable)
5. Ver estadísticas personales
```

### Para Autores

#### 1. Crear Nueva Publicación

```
1. Login como autor o admin
2. Click en "Nueva Publicación" en navbar
3. Completar formulario:
   
   Título: *
   ├─ Mínimo 5 caracteres
   └─ Se genera slug automático
   
   Contenido: *
   ├─ Mínimo 50 caracteres
   ├─ Soporta markdown
   └─ Editor de texto enriquecido
   
   Extracto:
   ├─ Opcional (se auto-genera si vacío)
   └─ Máximo 300 caracteres
   
   Categoría:
   └─ Seleccionar de lista desplegable
   
   Etiquetas:
   └─ Seleccionar múltiples (Ctrl + Click)
   
   Imagen Destacada:
   ├─ Formatos: JPG, PNG, GIF
   └─ Máximo 5MB
   
   Estado:
   ├─ Borrador: Solo visible para ti
   └─ Publicado: Visible para todos

4. Click en "Guardar"
5. Post creado exitosamente
```

**Ejemplo de Post:**
```markdown
Título: Introducción a Django 5.0

Contenido:
Django 5.0 trae nuevas características importantes...

[IMAGEN]

## Características Principales

1. **Async Views Mejoradas**
   Las vistas asíncronas ahora soportan...

2. **ORM Optimizado**
   Mejoras en rendimiento de queries...

## Instalación

pip install Django==5.0.1

## Conclusión

Django 5.0 es una actualización sólida...

Categoría: Django
Tags: tutorial, django, python
Estado: Publicado
```

#### 2. Editar Publicación

```
1. Ir a "Mis Posts"
2. Localizar el post a editar
3. Click en "Editar"
4. Modificar campos necesarios
5. Click en "Actualizar"
6. Cambios guardados
```

#### 3. Eliminar Publicación

```
1. Ir a "Mis Posts"
2. Localizar el post a eliminar
3. Click en "Eliminar"
4. Confirmar eliminación en el modal
5. Post eliminado permanentemente
```

#### 4. Gestionar Mis Posts

```
Vista "Mis Posts" muestra:

Estadísticas:
├─ Total de posts: 15
├─ Publicados: 12
├─ Borradores: 3
└─ Total de vistas: 1,234

Tabla de Posts:
├─ Título
├─ Estado (Publicado/Borrador)
├─ Fecha de creación
├─ Vistas
├─ Comentarios
└─ Acciones (Ver, Editar, Eliminar)

Filtros:
├─ Todos
├─ Solo publicados
└─ Solo borradores
```

### Para Administradores

#### 1. Acceder al Panel de Administración

```
1. Login como admin
2. Click en "🔒 Admin Panel" (navbar - texto amarillo)
3. Dashboard principal se carga

O directamente:
http://127.0.0.1:8000/admin-panel/
```

#### 2. Dashboard de Administración

**Vista Principal muestra:**

```
┌─────────────────────────────────────────────┐
│           ESTADÍSTICAS DE USUARIOS           │
├──────────────┬──────────────┬───────────────┤
│ Total: 156   │ Activos: 142 │ Admins: 3     │
├──────────────┼──────────────┼───────────────┤
│ Autores: 24  │ Lectores: 129│ Nuevos(7d): 12│
└──────────────┴──────────────┴───────────────┘

┌─────────────────────────────────────────────┐
│         ESTADÍSTICAS DE CONTENIDO            │
├──────────────┬──────────────┬───────────────┤
│ Total: 89    │ Publicados:78│ Borradores: 11│
├──────────────┼──────────────┼───────────────┤
│ Comentarios: │ Aprobados:   │ Pendientes:   │
│ 234          │ 230          │ 4             │
├──────────────┼──────────────┼───────────────┤
│ Categorías:8 │ Tags: 24     │               │
└──────────────┴──────────────┴───────────────┘

┌─────────────────────────────────────────────┐
│          TOP 5 POSTS MÁS VISTOS              │
├─────────────────────────┬──────────┬────────┤
│ Título                  │ Autor    │ Vistas │
├─────────────────────────┼──────────┼────────┤
│ Guía Django Avanzada    │ admin    │ 1,234  │
│ Python Tips & Tricks    │ autor1   │ 987    │
│ REST API con Django     │ admin    │ 856    │
│ Testing en Python       │ autor2   │ 743    │
│ Deploy en Producción    │ admin    │ 621    │
└─────────────────────────┴──────────┴────────┘

┌─────────────────────────────────────────────┐
│            ARCHIVOS DE LOG                   │
├─────────────┬───────────┬───────────────────┤
│ Archivo     │ Tamaño    │ Última Modificación│
├─────────────┼───────────┼───────────────────┤
│ general.log │ 2.4 MB    │ 2026-01-18 10:30  │
│ error.log   │ 0.5 MB    │ 2026-01-18 09:15  │
│ security.log│ 1.2 MB    │ 2026-01-18 10:28  │
│ database.log│ 3.1 MB    │ 2026-01-18 10:29  │
└─────────────┴───────────┴───────────────────┘
```

#### 3. Monitorear Logs del Sistema

**Acceder al visor:**
```
1. En Admin Panel, click en "Ver Logs"
2. O navegar a: /admin-panel/logs/
```

**Interfaz del Visor:**

```
┌─────────────────────────────────────────────────────┐
│  VISOR DE LOGS DEL SISTEMA                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Tipo: [General ▼]  Nivel: [Todos ▼]  Buscar: [....]│
│                                                      │
│  Estadísticas:  ERROR: 12  WARNING: 45  INFO: 234   │
│                                                      │
├──────┬─────────────────┬───────┬──────────────────┤
│Nivel │ Timestamp        │Módulo │ Mensaje          │
├──────┼─────────────────┼───────┼──────────────────┤
│🔴ERROR│2026-01-18 10:30│views  │Connection timeout│
│       │[Ver detalles ▼]                           │
├──────┼─────────────────┼───────┼──────────────────┤
│🟡WARN │2026-01-18 10:25│auth   │Failed login:user1│
├──────┼─────────────────┼───────┼──────────────────┤
│🔵INFO │2026-01-18 10:20│blog   │New post created  │
├──────┼─────────────────┼───────┼──────────────────┤
│      │         ... más logs ...                    │
└──────┴─────────────────┴───────┴──────────────────┘

 Página 1 de 10     [< Anterior]  [Siguiente >]
 
 [⬇️ Descargar Log]  [🗑️ Limpiar Logs]
```

**Filtros Disponibles:**

1. **Por Tipo:**
   - General - Todos los eventos del sistema
   - Error - Solo errores y excepciones
   - Security - Eventos de seguridad (logins, accesos)
   - Database - Queries y operaciones de BD

2. **Por Nivel:**
   - CRITICAL - Errores críticos del sistema
   - ERROR - Errores que requieren atención
   - WARNING - Advertencias importantes
   - INFO - Información general
   - DEBUG - Información de depuración

3. **Por Búsqueda:**
   - Buscar texto en timestamp, módulo o mensaje
   - Case-insensitive
   - Filtra en tiempo real

**Ejemplo de Uso:**
```
Escenario: Investigar intentos de login fallidos

1. Seleccionar tipo: "Security"
2. Seleccionar nivel: "WARNING"
3. Buscar: "login"
4. Revisar resultados:
   
   [WARNING] 2026-01-18 10:15 - auth - Login failed: usuario@email.com
   [WARNING] 2026-01-18 10:16 - auth - Login failed: usuario@email.com
   [WARNING] 2026-01-18 10:17 - auth - Login failed: usuario@email.com
   [WARNING] 2026-01-18 10:18 - auth - Rate limit reached for IP 192.168.1.100

Conclusión: Usuario bloqueado por múltiples intentos
Acción: Verificar si es ataque o usuario olvidó contraseña
```

#### 4. Descargar Logs

```
1. En visor de logs, seleccionar tipo
2. Click en "⬇️ Descargar Log"
3. Archivo se descarga al navegador
4. Nombre del archivo: [tipo].log
5. Abrir con editor de texto para análisis detallado
```

#### 5. Limpiar Logs

```
⚠️ PRECAUCIÓN: Esta acción limpia el log seleccionado

1. Seleccionar tipo de log
2. Click en "🗑️ Limpiar Logs"
3. Confirmar en modal:
   "¿Estás seguro de limpiar general.log?"
   "Se creará un backup automático"
4. Click en "Sí, limpiar"
5. Proceso:
   ├─ Crear backup: general.log.backup
   ├─ Vaciar archivo general.log
   └─ Registrar evento en security.log
6. Mensaje de éxito mostrado
```

#### 6. Ver Estado del Sistema

```
1. En Admin Panel, click en "Estado del Sistema"
2. Vista completa muestra:

┌─────────────────────────────────────────┐
│       INFORMACIÓN DEL SISTEMA           │
├─────────────────────────────────────────┤
│ Python Version: 3.11.9                  │
│ Django Version: 5.0.1                   │
│ Database: sqlite3                       │
│ Debug Mode: ⚠️ Activado (desarrollo)    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     ESTADO DE LA BASE DE DATOS          │
├─────────────────────────────────────────┤
│ ✅ Conexión OK                           
│ Base de datos funcionando correctamente │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         ESPACIO DE LOGS                 │
├─────────────────────────────────────────┤
│ 7.2 MB usado                            │
│ [████████░░░░░░░░░░] 7.2%               │
│                                         │
│ ✅ Espacio normal (< 10 MB)            
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       ESTADO DE SERVICIOS               │
├────────────┬────────────────────────────┤
│ 🌐 Web     │ ✅ Activo                 │
│ 🗄️ BD      │ ✅ Activo                 │
│ 🔒 Segur   │ ✅ Activo                 │
│ 📁 Logs    │ ✅ Activo                 │
└────────────┴────────────────────────────┘

┌─────────────────────────────────────────┐
│    CONFIGURACIONES DE SEGURIDAD         │
├──────────────────────────────────────── ┤
│ Protecciones Activas:                   │
| ✅ CSRF Protection                    
│ ✅ XSS Protection                      
│ ✅ SQL Injection Prevention             
│ ✅ Argon2 Password Hashing              
│                                         
│ Rate Limiting:                          
│ ✅ Login: 10/min por IP                 
│ ✅ Registro: 5/min por IP               
│ ✅ Comentarios: 10/hora por usuario     
└─────────────────────────────────────────
```

---

## 📁 Estructura Detallada del Proyecto

```
Simple_Blog_Platform/
│
├── 📁 accounts/                    # App de Autenticación y Usuarios
│   ├── __init__.py                # Inicialización del paquete
│   ├── admin.py                   # Configuración del admin de Django
│   ├── apps.py                    # Configuración de la app
│   ├── decorators.py              # Decoradores personalizados (@admin_required, etc.)
│   ├── forms.py                   # Formularios (Registro, Login, Perfil)
│   ├── mixins.py                  # Mixins para vistas basadas en clases
│   ├── models.py                  # Modelo CustomUser con roles
│   ├── tests.py                   # Tests unitarios de autenticación
│   ├── urls.py                    # Rutas de accounts/
│   ├── views.py                   # Vistas (register, login, logout, etc.)
│   ├── 📁 migrations/             # Migraciones de base de datos
│   │   ├── 0001_initial.py       # Migración inicial
│   │   └── __init__.py
│   └── 📁 templates/accounts/     # Templates de autenticación
│       ├── dashboard.html        # Dashboard del usuario
│       ├── login.html            # Formulario de login
│       ├── register.html         # Formulario de registro
│       ├── profile.html          # Perfil de usuario
│       ├── logout_confirm.html   # Confirmación de logout
│       └── password_reset_*.html # Templates de recuperación
│
├── 📁 blog/                       # App del Blog (Posts y Comentarios)
│   ├── __init__.py
│   ├── admin.py                  # Admin de Posts, Categories, Tags, Comments
│   ├── apps.py
│   ├── forms.py                  # Formularios (PostForm, CommentForm, etc.)
│   ├── models.py                 # Modelos (Post, Category, Tag, Comment)
│   ├── tests.py                  # Tests del blog
│   ├── urls.py                   # Rutas de blog/
│   ├── views.py                  # Vistas CRUD y listados
│   ├── 📁 migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   └── 📁 templates/blog/
│       ├── post_list.html        # Lista de publicaciones
│       ├── post_detail.html      # Detalle con comentarios
│       ├── post_form.html        # Crear/Editar post
│       ├── post_confirm_delete.html  # Confirmar eliminación
│       ├── my_posts.html         # Posts del autor
│       ├── category_list.html    # Lista de categorías
│       └── tag_list.html         # Lista de tags
│
├── 📁 admin_panel/                # App del Panel de Administración
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py                   # Rutas de admin-panel/
│   ├── views.py                  # Vistas (dashboard, logs, system_status)
│   └── 📁 templates/admin_panel/
│       ├── dashboard.html        # Dashboard con estadísticas
│       ├── logs.html             # Visor de logs con filtros
│       └── system_status.html    # Estado del sistema
│
├── 📁 blog_platform/              # Configuración Principal del Proyecto
│   ├── __init__.py
│   ├── asgi.py                   # Configuración ASGI (async)
│   ├── settings.py               # ⚙️ CONFIGURACIÓN PRINCIPAL
│   │                             # • INSTALLED_APPS
│   │                             # • MIDDLEWARE
│   │                             # • DATABASES
│   │                             # • AUTH_USER_MODEL
│   │                             # • PASSWORD_HASHERS (Argon2)
│   │                             # • SECURITY SETTINGS
│   │                             # • LOGGING CONFIGURATION
│   ├── urls.py                   # 🔗 ENRUTAMIENTO PRINCIPAL
│   │                             # • admin/
│   │                             # • admin-panel/
│   │                             # • accounts/
│   │                             # • blog/
│   ├── views.py                  # Handlers de errores (404, 500)
│   └── wsgi.py                   # Configuración WSGI (sync)
│
├── 📁 templates/                  # Templates Base y Globales
│   ├── base.html                 # 🎨 TEMPLATE BASE
│   │                             # • Navbar con roles
│   │                             # • Mensajes flash
│   │                             # • Footer
│   │                             # • Bloques {% block %}
│   ├── home.html                 # Página de inicio
│   ├── 403.html                  # Error de permisos
│   ├── 404.html                  # Página no encontrada
│   └── 500.html                  # Error del servidor
│
├── 📁 static/                     # Archivos Estáticos
│   ├── 📁 css/                   # Estilos personalizados
│   ├── 📁 js/                    # JavaScript personalizado
│   └── 📁 images/                # Imágenes del sitio
│
├── 📁 media/                      # Archivos Subidos por Usuarios
│   └── 📁 posts/                 # Imágenes de posts
│       └── 📁 YYYY/MM/DD/        # Organizado por fecha
│
├── 📁 logs/                       # 📊 SISTEMA DE LOGS
│   ├── general.log               # Logs generales (INFO+)
│   ├── general.log.1-5           # Backups rotados
│   ├── error.log                 # Solo errores (ERROR+)
│   ├── error.log.1-5             # Backups rotados
│   ├── security.log              # Eventos de seguridad (WARNING+)
│   ├── security.log.1-5          # Backups rotados
│   ├── database.log              # Queries de BD (DEBUG+)
│   └── database.log.1-3          # Backups rotados
│
├── 📄 manage.py                   # CLI de Django
├── 📄 requirements.txt            # Dependencias del proyecto
├── 📄 .env.example                # Plantilla de variables de entorno
├── 📄 .gitignore                  # Archivos ignorados por Git
│
├── 📄 README.md                   # 📖 ESTE ARCHIVO
├── 📄 generate_test_logs.py       # Script para generar logs de prueba
│
└── 📁 venv/                       # Entorno virtual (no en Git)
    └── ...
```

### Descripción de Componentes Clave

#### 🔐 accounts/models.py
```python
CustomUserManager:
  • create_user()      - Crea usuarios regulares
  • create_superuser() - Crea administradores

CustomUser (extends AbstractBaseUser, PermissionsMixin):
  Campos:
    • email (unique)          - Campo de login
    • username (unique)       - Nombre de usuario
    • role                    - 'admin', 'author', 'reader'
    • is_active               - Requiere verificación de email
    • is_email_verified       - Email confirmado
    • date_joined, last_login - Metadatos
  
  Properties:
    • is_admin     - Verifica si es admin
    • is_author    - Verifica si puede publicar
    • can_publish  - Alias de is_author
  
  Métodos:
    • get_full_name()  - Nombre completo
    • get_short_name() - Nombre corto
```

#### 📝 blog/models.py
```python
Category:
  • name (unique)     - Nombre de la categoría
  • slug (unique)     - URL amigable
  • description       - Descripción opcional
  • Auto-genera slug  - slugify(name)

Tag:
  • name (unique)     - Nombre del tag
  • slug (unique)     - URL amigable
  • Relación M2M      - con Post

Post:
  Campos:
    • author (FK)         - Relación con CustomUser
    • category (FK)       - Relación con Category
    • tags (M2M)          - Relación con Tag
    • title               - Título del post
    • slug (unique)       - URL amigable
    • content (Text)      - Contenido completo
    • excerpt             - Resumen corto
    • featured_image      - Imagen principal
    • status              - 'draft' o 'published'
    • views_count         - Contador de vistas
    • created_at          - Fecha de creación
    • updated_at          - Última actualización
    • published_at        - Fecha de publicación
  
  Managers:
    • objects     - Manager por defecto (todos)
    • published   - Solo publicados
  
  Properties:
    • reading_time    - Calcula minutos de lectura
    • comment_count   - Cuenta comentarios aprobados
  
  Métodos:
    • save()            - Auto-genera slug y excerpt
    • get_absolute_url()- URL del post

Comment:
  • post (FK)         - Post al que pertenece
  • user (FK)         - Usuario que comentó
  • parent (FK self)  - Comentario padre (anidado)
  • content           - Texto del comentario
  • is_approved       - Moderación
  • created_at        - Fecha de creación
  
  Properties:
    • is_reply  - Verifica si es respuesta
```

#### 🛡️ accounts/decorators.py
```python
@role_required(['admin', 'author']):
  • Verifica rol del usuario
  • Requiere login previo
  • Levanta PermissionDenied si no cumple

@admin_required:
  • Solo permite admins
  • Wrapper de role_required(['admin'])

@author_required:
  • Permite admins y autores
  • Wrapper de role_required(['admin', 'author'])

@email_verified_required:
  • Requiere email verificado
  • Para acciones sensibles
```

#### 📋 accounts/forms.py
```python
RegistrationForm:
  Validaciones:
    • Email único
    • Username único (3+ chars, alfanumérico + _)
    • Password seguro:
      - 8+ caracteres
      - Al menos 1 mayúscula
      - Al menos 1 minúscula
      - Al menos 1 número
      - Al menos 1 carácter especial

LoginForm:
  • Email como username
  • Campo remember_me para sesión persistente
  • Widgets Bootstrap 5

PostForm:
  • Todos los campos de Post
  • Validación de título (5+ chars)
  • Validación de contenido (50+ chars)
  • Upload de imagen
  • Selección múltiple de tags

CommentForm:
  • Solo campo content
  • Validación (3-1000 chars)
```

#### 🌐 Rutas (URLs)

```
blog_platform/urls.py (Principal):
  /                           → home
  /admin/                     → Django admin
  /admin-panel/               → Admin panel custom
  /accounts/                  → accounts.urls
  /blog/                      → blog.urls

accounts/urls.py:
  /accounts/register/         → register
  /accounts/login/            → login_view
  /accounts/logout/           → logout_view
  /accounts/dashboard/        → dashboard
  /accounts/profile/          → profile
  /accounts/verify/<uid>/<token>/ → verify_email
  /accounts/password-reset/   → PasswordResetView

blog/urls.py:
  /blog/                      → post_list
  /blog/post/new/             → post_create
  /blog/post/<slug>/          → post_detail
  /blog/post/<slug>/edit/     → post_edit
  /blog/post/<slug>/delete/   → post_delete
  /blog/my-posts/             → my_posts
  /blog/categories/           → category_list
  /blog/tags/                 → tag_list

admin_panel/urls.py (app_name='admin_panel'):
  /admin-panel/               → admin_dashboard
  /admin-panel/logs/          → view_logs
  /admin-panel/logs/download/<type>/ → download_log
  /admin-panel/logs/clear/<type>/    → clear_log
  /admin-panel/system/        → system_status
```

#### ⚙️ Configuración de Seguridad (settings.py)

```python
# Password Hashing (Más seguro a menos seguro)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Recomendado
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Protecciones de Producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True           # Forzar HTTPS
    SESSION_COOKIE_SECURE = True          # Cookies solo HTTPS
    CSRF_COOKIE_SECURE = True             # CSRF solo HTTPS
    SECURE_HSTS_SECONDS = 31536000        # HSTS 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # HSTS subdominios
    SECURE_HSTS_PRELOAD = True            # HSTS preload
    X_FRAME_OPTIONS = 'DENY'              # No iframes
    SECURE_BROWSER_XSS_FILTER = True      # XSS filter
    SECURE_CONTENT_TYPE_NOSNIFF = True    # No MIME sniffing

# Cookies Seguras
CSRF_COOKIE_HTTPONLY = True     # No accesible por JS
CSRF_COOKIE_SAMESITE = 'Strict' # Solo mismo sitio
SESSION_COOKIE_HTTPONLY = True  # No accesible por JS
SESSION_COOKIE_SAMESITE = 'Lax' # Permite navegación normal
SESSION_COOKIE_AGE = 1209600    # 2 semanas

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FRAME_ANCESTORS = ("'none'",)

# Rate Limiting
RATELIMIT_ENABLE = True
Implementado en vistas:
  • register: 5 intentos/minuto por IP
  • login: 10 intentos/minuto por IP
  • post_detail (comentarios): 10/hora por usuario o IP
```

#### 📊 Sistema de Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
        },
    },
    
    'handlers': {
        'file_general': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/general.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_database': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/database.log',
            'maxBytes': 10485760,
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    
    'loggers': {
        'django.request': {
            'handlers': ['file_error'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'WARNING',
        },
        'django.db.backends': {
            'handlers': ['file_database'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'accounts': {
            'handlers': ['file_general', 'file_security'],
            'level': 'INFO',
        },
        'blog': {
            'handlers': ['file_general'],
            'level': 'INFO',
        },
    },
}
```

**Uso en código:**
```python
import logging
logger = logging.getLogger('accounts')

# En las vistas
logger.info(f'Usuario {username} inició sesión')
logger.warning(f'Intento de login fallido: {email}')
logger.error(f'Error al procesar formulario: {error}')
```

---

## 🧪 Testing y Calidad de Código

### Ejecutar Tests

```bash
# Tests completos
python manage.py test

# Tests de una app específica
python manage.py test accounts
python manage.py test blog
python manage.py test admin_panel

# Tests con verbose
python manage.py test --verbosity=2

# Tests en paralelo (más rápido)
python manage.py test --parallel
```

### Cobertura de Código

```bash
# Instalar coverage (si no está)
pip install coverage

# Ejecutar tests con cobertura
coverage run --source='.' manage.py test

# Ver reporte en terminal
coverage report

# Ver líneas no cubiertas
coverage report -m

# Generar reporte HTML
coverage html

# Abrir reporte en navegador
# Windows
start htmlcov/index.html
# Linux/Mac
open htmlcov/index.html
```

**Objetivo de Cobertura:**
- **Global:** > 80%
- **Funciones core:** 100%
- **Infraestructura:** > 0% (no requerido)

### Linting y Formateo

```bash
# Instalar herramientas
pip install black flake8 isort

# Formatear código con black
black .

# Verificar estilo con flake8
flake8 .

# Ordenar imports con isort
isort .

# Verificar tipos con mypy (opcional)
pip install mypy
mypy .
```

### Tests Manuales

#### Test de Seguridad

**1. Test de SQL Injection:**
```bash
# Intentar inyección en búsqueda
/blog/?q=' OR '1'='1

# Resultado esperado:
✅ No devuelve todos los posts
✅ Query es sanitizada por ORM
```

**2. Test de XSS:**
```bash
# Intentar script en comentario
<script>alert('XSS')</script>

# Resultado esperado:
✅ El script se escapa automáticamente
✅ Se muestra como texto plano
```

**3. Test de CSRF:**
```bash
# Intentar POST sin token
curl -X POST http://localhost:8000/accounts/login/ -d "email=test@test.com"

# Resultado esperado:
✅ 403 Forbidden
✅ "CSRF verification failed"
```

**4. Test de Rate Limiting:**
```bash
# 6 intentos de login en 1 minuto
for i in {1..6}; do
  curl -X POST http://localhost:8000/accounts/login/ \
    -d "email=test@test.com&password=wrong"
done

# Resultado esperado:
✅ Primeros 5: Login fallido
✅ Sexto: 429 Too Many Requests
✅ "Rate limit exceeded"
```

**5. Test de Permisos:**
```bash
# Como lector, intentar crear post
# Login como lector → Ir a /blog/post/new/

# Resultado esperado:
✅ 403 Forbidden
✅ Mensaje: "Requiere rol: admin, author"
```

#### Test de Funcionalidad

**Checklist de Registro:**
```
[ ] Formulario muestra todos los campos
[ ] Validación de email duplicado funciona
[ ] Validación de username duplicado funciona
[ ] Validación de contraseña segura funciona
[ ] Email de verificación se envía
[ ] Link de verificación funciona
[ ] Usuario puede iniciar sesión después
[ ] Rate limiting (5/min) funciona
```

**Checklist de Posts:**
```
[ ] Solo autores/admins pueden crear
[ ] Slug se genera automáticamente
[ ] Excerpt se genera si está vacío
[ ] Imagen se sube correctamente
[ ] Tags se guardan (ManyToMany)
[ ] Borrador no es visible públicamente
[ ] Publicado es visible en lista
[ ] Contador de vistas incrementa
[ ] Tiempo de lectura se calcula
[ ] Solo autor/admin puede editar
[ ] Solo autor/admin puede eliminar
```

**Checklist de Comentarios:**
```
[ ] Solo usuarios autenticados pueden comentar
[ ] Comentario aparece inmediatamente (is_approved=True)
[ ] Respuestas anidadas funcionan (parent)
[ ] Solo autor/admin puede eliminar comentario
[ ] Rate limiting (10/hora) funciona
```

**Checklist de Admin Panel:**
```
[ ] Solo admins pueden acceder
[ ] Dashboard muestra estadísticas correctas
[ ] Logs se cargan correctamente
[ ] Filtros de logs funcionan:
    [ ] Por tipo (general, error, security, database)
    [ ] Por nivel (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    [ ] Por búsqueda de texto
[ ] Paginación de logs funciona (50/página)
[ ] Descarga de logs funciona
[ ] Limpieza de logs crea backup
[ ] Estado del sistema muestra info correcta
```

---

## 🔒 Políticas de Seguridad

### Prácticas de Seguridad

#### ✅ Implementadas

- **Autenticación:** Argon2 password hashing
- **Autorización:** Decoradores basados en roles
- **CSRF:** Tokens en todos los formularios POST
- **XSS:** Auto-escape de templates + CSP headers
- **SQL Injection:** ORM (sin SQL crudo)
- **Rate Limiting:** Endpoints críticos limitados
- **Sesiones:** HttpOnly, Secure, SameSite cookies
- **HTTPS:** Forzado en producción
- **HSTS:** Headers configurados
- **Logs:** Auditoría de eventos de seguridad

#### ⚠️ Recomendaciones para Producción

```python
# En .env de producción
DEBUG=False
SECRET_KEY=<generar-clave-fuerte-aleatoria>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de datos
# Usar PostgreSQL, no SQLite
DB_ENGINE=django.db.backends.postgresql

# Email
# Configurar SMTP real, no console backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Servidor
# Usar gunicorn/uwsgi, no runserver
# Usar nginx como reverse proxy
# Configurar SSL/TLS (Let's Encrypt)

# Monitoreo
# Implementar Sentry para tracking de errores
# Configurar alertas de logs críticos
# Monitorear espacio en disco de logs
```

### Checklist de Deployment

```
Antes de deploy a producción:

[ ] DEBUG = False
[ ] SECRET_KEY única y segura
[ ] ALLOWED_HOSTS configurado
[ ] Base de datos PostgreSQL
[ ] Email SMTP configurado
[ ] Archivos estáticos colectados (collectstatic)
[ ] Gunicorn/uWSGI configurado
[ ] Nginx como reverse proxy
[ ] SSL/TLS habilitado
[ ] Firewall configurado
[ ] Backups automáticos de BD
[ ] Monitoreo de logs configurado
[ ] Sentry o similar para errores
[ ] Variables de entorno en servidor
[ ] Permisos de archivos correctos
[ ] Logs directory con permisos de escritura
```

---

## 🚢 Deployment en Producción

### Opción 1: Deploy con Gunicorn + Nginx

#### 1. Instalar dependencias de producción

```bash
pip install gunicorn psycopg2-binary
```

#### 2. Configurar Gunicorn

```bash
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

#### 3. Crear servicio systemd

```bash
# /etc/systemd/system/blogplatform.service
[Unit]
Description=Blog Platform Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Simple_Blog_Platform
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn \
          --config gunicorn.conf.py \
          blog_platform.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 4. Configurar Nginx

```nginx
# /etc/nginx/sites-available/blogplatform
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tudominio.com www.tudominio.com;
    
    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /path/to/Simple_Blog_Platform/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /path/to/Simple_Blog_Platform/media/;
        expires 30d;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. Habilitar y iniciar servicios

```bash
# Habilitar sitio Nginx
sudo ln -s /etc/nginx/sites-available/blogplatform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Habilitar servicio de app
sudo systemctl enable blogplatform
sudo systemctl start blogplatform
sudo systemctl status blogplatform
```

### Opción 2: Deploy con Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "blog_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: blog_platform
      POSTGRES_USER: bloguser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    
  web:
    build: .
    command: gunicorn blog_platform.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
  
  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

```bash
# Comandos Docker
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### Opción 3: Deploy en Heroku

```bash
# Procfile
web: gunicorn blog_platform.wsgi

# runtime.txt
python-3.11.9

# Comandos
heroku create tu-blog-platform
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=tu-clave-secreta
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 📝 Changelog

### [1.1.0] - 2026-01-18

#### ✨ Añadido
- Sistema completo de monitoreo de logs para administradores
- Dashboard de administración con estadísticas en tiempo real
- Visor de logs interactivo con filtros avanzados
- 4 tipos de logs categorizados (general, error, security, database)
- Rotación automática de logs con backups (10MB por archivo)
- Funcionalidad de descarga y limpieza de logs
- Vista de estado del sistema con información de versiones y servicios
- Script generador de logs de prueba
- Documentación completa del sistema de logs
- Guía de prueba paso a paso para administradores

#### 🔒 Seguridad
- Control de acceso basado en roles para admin panel
- Decorador @admin_required para protección de rutas
- Logs de auditoría para eventos de seguridad
- Backup automático antes de limpiar logs

#### 📚 Documentación
- ADMIN_LOG_SYSTEM.md - Documentación técnica completa
- TESTING_ADMIN_LOGS.md - Guía de prueba detallada
- README.md mejorado con diagramas y ejemplos
- Diagramas de flujo del sistema

### [1.0.0] - 2026-01-09

#### ✨ Añadido
- Sistema de autenticación completo con verificación de email
- Modelo de usuario personalizado con roles (Admin, Autor, Lector)
- CRUD completo de publicaciones
- Sistema de comentarios anidados
- Categorías y etiquetas para organización
- Búsqueda y filtrado avanzado de posts
- Panel de administración base de Django
- Rate limiting en endpoints críticos
- 17 tests unitarios con ~85% de cobertura

#### 🔒 Seguridad
- Argon2 password hashing
- CSRF protection
- XSS prevention con auto-escape
- SQL injection prevention con ORM
- Secure sessions con HttpOnly cookies
- CSP headers configurados

---

## 📜 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.
