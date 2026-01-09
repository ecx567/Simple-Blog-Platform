# Simple Blog Platform

Sistema de blog completo con autenticación de usuarios, sistema de roles y funcionalidades avanzadas desarrollado con Django.

## 📋 Características

- ✅ Sistema de autenticación completo (registro, login, logout)
- ✅ Verificación de email
- ✅ Recuperación de contraseña
- ✅ Sistema de roles (Admin, Autor, Lector)
- ✅ CRUD de publicaciones con editor rico
- ✅ Sistema de comentarios anidados
- ✅ Categorías y etiquetas
- ✅ Búsqueda y filtrado avanzado
- ✅ Panel de administración
- ✅ Seguridad robusta (protección XSS, CSRF, SQL Injection)
- ✅ Rate limiting para prevenir ataques de fuerza bruta
- ✅ Contraseñas hasheadas con Argon2

## 🛠️ Tecnologías

- **Backend:** Python 3.11+, Django 5.0
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Seguridad:** Argon2, Django Security Middleware
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

La documentación completa del proyecto se encuentra en [DOCUMENTATION.md](DOCUMENTATION.md) e incluye:

1. Definición de requisitos (funcionales y no funcionales)
2. Arquitectura del sistema (MTV/MVC)
3. Tecnologías y justificación
4. Diseño del sistema de autenticación paso a paso
5. Reglas de seguridad
6. Modelo de base de datos
7. Flujo de desarrollo
8. Buenas prácticas
9. Pruebas y validación

## 🚀 Uso Rápido

### Crear un post

1. Inicia sesión como usuario con rol "Autor" o "Admin"
2. Ve a "Crear Publicación"
3. Completa el formulario
4. Publica o guarda como borrador

### Sistema de Roles

- **Admin:** Acceso total al sistema
- **Autor:** Puede crear, editar y eliminar sus propias publicaciones
- **Lector:** Puede ver publicaciones y comentar

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
├── accounts/              # App de autenticación
│   ├── models.py         # Modelo de usuario personalizado
│   ├── views.py          # Vistas de auth
│   ├── forms.py          # Formularios de registro/login
│   ├── urls.py           # Rutas de autenticación
│   └── templates/        # Templates de auth
├── blog/                 # App del blog
│   ├── models.py         # Posts, Comments, Categories, Tags
│   ├── views.py          # Vistas CRUD
│   ├── forms.py          # Formularios del blog
│   └── templates/        # Templates del blog
├── blog_platform/        # Configuración del proyecto
│   ├── settings.py       # Configuración principal
│   ├── urls.py           # Rutas principales
│   └── wsgi.py           # WSGI config
├── static/               # Archivos estáticos
├── media/                # Uploads de usuarios
├── templates/            # Templates base
├── manage.py             # CLI de Django
├── requirements.txt      # Dependencias
├── .env.example          # Variables de entorno ejemplo
├── .gitignore           # Git ignore
├── README.md            # Este archivo
└── DOCUMENTATION.md     # Documentación completa
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

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👤 Autor

Desarrollado como proyecto educativo para demostrar buenas prácticas en desarrollo web con Django.

## 📧 Soporte

Para preguntas o issues, por favor abre un issue en el repositorio.

---

**Nota:** Este proyecto está diseñado con fines educativos siguiendo las mejores prácticas de la industria.
