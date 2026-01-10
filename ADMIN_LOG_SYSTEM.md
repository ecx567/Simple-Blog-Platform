# Sistema de Monitoreo de Logs para Administradores

## 📋 Descripción General

Este sistema proporciona un panel de administración completo para monitorear, analizar y gestionar los logs del sistema Blog Platform. **Solo usuarios con rol de Administrador** tienen acceso a estas funcionalidades.

## 🔐 Control de Acceso

### Seguridad Implementada

- **Decorador `@admin_required`**: Todas las vistas del admin panel están protegidas
- **Verificación a nivel de template**: Los enlaces solo aparecen para administradores
- **Protección CSRF**: Todas las operaciones destructivas requieren token CSRF
- **Rate Limiting**: Las operaciones de logs están limitadas para prevenir abuso

### Roles y Permisos

| Rol | Acceso al Admin Panel | Ver Logs | Descargar Logs | Limpiar Logs |
|-----|----------------------|----------|----------------|--------------|
| **Admin** | ✅ | ✅ | ✅ | ✅ |
| **Autor** | ❌ | ❌ | ❌ | ❌ |
| **Lector** | ❌ | ❌ | ❌ | ❌ |

## 📁 Estructura del Sistema de Logs

### Archivos de Log Configurados

```
logs/
├── general.log          # Logs generales de la aplicación
├── general.log.1        # Rotación automática (backup 1)
├── general.log.2        # Rotación automática (backup 2)
├── error.log            # Errores y excepciones
├── error.log.1-5        # Hasta 5 backups
├── security.log         # Eventos de seguridad
├── security.log.1-5     # Hasta 5 backups
└── database.log         # Queries y operaciones de BD
    └── database.log.1-3 # Hasta 3 backups
```

### Configuración de Rotación

- **Tamaño máximo por archivo**: 10 MB (database.log: 10 MB)
- **Número de backups**: 
  - general.log: 5 backups
  - error.log: 5 backups
  - security.log: 5 backups
  - database.log: 3 backups
- **Rotación automática**: Cuando se alcanza el tamaño máximo

## 🎯 Funcionalidades del Admin Panel

### 1. Dashboard Principal (`/admin-panel/`)

**Características:**

- **Estadísticas de Usuarios**:
  - Total de usuarios registrados
  - Usuarios activos (últimos 7 días)
  - Conteo por roles (Admin, Autores, Lectores)

- **Estadísticas de Contenido**:
  - Total de posts (publicados vs borradores)
  - Total de comentarios (aprobados vs pendientes)
  - Número de categorías y tags

- **Top 5 Posts Más Vistos**:
  - Título del post
  - Autor
  - Número de vistas
  - Fecha de publicación

- **Información de Logs**:
  - Lista de archivos de log
  - Tamaño de cada archivo
  - Última modificación
  - Acceso directo a visualización

- **Actividad Reciente**:
  - Nuevos usuarios (últimos 7 días)
  - Posts recientes

### 2. Visor de Logs (`/admin-panel/logs/`)

**Características Avanzadas:**

#### Filtrado Múltiple

1. **Por Tipo de Log**:
   - General (todos los eventos)
   - Error (solo errores)
   - Security (eventos de seguridad)
   - Database (operaciones de BD)

2. **Por Nivel de Severidad**:
   - 🔴 **CRITICAL**: Errores críticos del sistema
   - 🟠 **ERROR**: Errores que requieren atención
   - 🟡 **WARNING**: Advertencias importantes
   - 🔵 **INFO**: Información general
   - ⚪ **DEBUG**: Información de depuración

3. **Búsqueda de Texto**:
   - Buscar en todo el contenido del log
   - Búsqueda en módulo, mensaje y timestamp
   - Búsqueda case-insensitive

#### Visualización

- **Color-Coded**: Cada nivel tiene su color distintivo
- **Paginación**: 50 entradas por página
- **Detalles Expandibles**: Click para ver el log completo
- **Estadísticas en Tiempo Real**: Contadores por nivel de severidad

#### Tabla de Información

| Columna | Descripción |
|---------|-------------|
| **Timestamp** | Fecha y hora exacta del evento |
| **Nivel** | Severidad con badge de color |
| **Módulo** | Origen del log (view, model, etc.) |
| **Mensaje** | Descripción del evento |
| **Detalles** | Botón para expandir información completa |

### 3. Descarga de Logs (`/admin-panel/logs/download/<type>/`)

**Funcionalidad:**

- Descargar logs completos en formato `.log`
- Mantiene el formato original
- Útil para análisis offline
- Tipos disponibles: general, error, security, database

**Ejemplo de Uso:**
```
GET /admin-panel/logs/download/error/
→ Descarga: error.log
```

### 4. Limpieza de Logs (`/admin-panel/logs/clear/<type>/`)

**Características de Seguridad:**

1. **Backup Automático**: Antes de limpiar, se crea `<log_type>.log.backup`
2. **Confirmación Requerida**: Modal de JavaScript con confirmación doble
3. **Protección CSRF**: Token obligatorio para la operación
4. **Log del Evento**: Se registra quién limpió los logs y cuándo

**Proceso de Limpieza:**
```
1. Usuario hace click en "Limpiar Logs"
2. Modal de confirmación: "¿Estás seguro?"
3. Si confirma:
   - Crear backup: error.log → error.log.backup
   - Vaciar archivo error.log
   - Registrar evento en security.log
   - Mostrar mensaje de éxito
```

### 5. Estado del Sistema (`/admin-panel/system/`)

**Información Mostrada:**

#### Información del Sistema
- Versión de Python
- Versión de Django
- Tipo de base de datos
- Estado del modo DEBUG

#### Estado de la Base de Datos
- Conexión activa/inactiva
- Mensaje de error si hay problemas

#### Espacio de Logs
- Tamaño total de logs en MB
- Barra de progreso visual
- Alertas si excede límites:
  - Verde: < 10 MB
  - Amarillo: 10-50 MB
  - Rojo: > 50 MB
  - Alerta: > 100 MB

#### Estado de Servicios
- ✅ Servidor Web
- ✅ Base de Datos
- ✅ Sistema de Seguridad
- ✅ Sistema de Logs

#### Configuraciones de Seguridad
- Protecciones activas (CSRF, XSS, SQL Injection, Argon2)
- Rate Limiting configurado

## 🔍 Tipos de Eventos Registrados

### General Log
```python
- Inicio de sesión exitoso
- Acceso a páginas
- Operaciones CRUD de posts
- Creación de comentarios
- Cambios en perfiles
```

### Error Log
```python
- Excepciones no controladas
- Errores 500
- Errores de validación de formularios
- Timeouts de operaciones
- Fallos de conexión a BD
```

### Security Log
```python
- Intentos de login fallidos
- Violaciones de rate limiting
- Accesos no autorizados
- Cambios de contraseña
- Limpieza de logs
- Creación/eliminación de usuarios admin
```

### Database Log
```python
- Queries SQL ejecutadas
- Tiempo de ejecución de queries
- Errores de integridad
- Migraciones aplicadas
```

## 🛠️ Configuración Técnica

### Settings.py - LOGGING

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} - {module} (Process: {process:d} Thread: {thread:d}) - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_general': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'general.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        # ... más handlers
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        # ... más loggers
    }
}
```

### Uso en Código

```python
import logging

logger = logging.getLogger('accounts')  # Para app accounts
logger_blog = logging.getLogger('blog')  # Para app blog
logger_security = logging.getLogger('django.security')  # Para seguridad

# Ejemplos de uso
logger.info(f'Usuario {username} inició sesión correctamente')
logger_blog.warning(f'Intento de acceso a post borrador por usuario no autor')
logger_security.error(f'Intento de acceso no autorizado al admin panel por {user.username}')
```

## 📊 Casos de Uso

### Caso 1: Detectar Intentos de Acceso No Autorizado

1. Usuario no-admin intenta acceder a `/admin-panel/`
2. Decorador `@admin_required` bloquea el acceso
3. Se registra en `security.log`:
   ```
   [WARNING] 2024-01-15 10:30:45 - decorators - Intento de acceso no autorizado al admin panel por usuario_normal
   ```
4. Admin revisa logs y ve el patrón de intentos
5. Puede tomar acción (bloquear usuario, investigar, etc.)

### Caso 2: Monitorear Errores de Aplicación

1. Ocurre error 500 en producción
2. Se registra en `error.log` con stack trace completo
3. Admin accede a `/admin-panel/logs/`
4. Filtra por nivel ERROR
5. Ve el error específico con contexto
6. Descarga el log para análisis detallado
7. Implementa fix y monitorea que no se repita

### Caso 3: Análisis de Rendimiento

1. Admin nota lentitud en la aplicación
2. Accede a `/admin-panel/logs/?type=database`
3. Filtra logs de base de datos
4. Identifica queries lentas
5. Optimiza índices o queries problemáticas
6. Monitorea mejora en performance

### Caso 4: Auditoría de Seguridad

1. Se requiere auditoría de seguridad mensual
2. Admin descarga `security.log`
3. Analiza:
   - Intentos de login fallidos
   - Cambios de contraseña
   - Accesos a áreas restringidas
   - Rate limiting activado
4. Genera reporte de seguridad
5. Implementa medidas adicionales si es necesario

## 🚀 Acceso al Sistema

### URLs del Admin Panel

| URL | Descripción | Método |
|-----|-------------|--------|
| `/admin-panel/` | Dashboard principal | GET |
| `/admin-panel/logs/` | Visor de logs | GET |
| `/admin-panel/logs/?type=error` | Logs filtrados por tipo | GET |
| `/admin-panel/logs/?level=ERROR` | Logs filtrados por nivel | GET |
| `/admin-panel/logs/?search=login` | Buscar en logs | GET |
| `/admin-panel/logs/download/<type>/` | Descargar log | GET |
| `/admin-panel/logs/clear/<type>/` | Limpiar log | POST |
| `/admin-panel/system/` | Estado del sistema | GET |

### Navegación

1. **Desde Navbar**: 
   - Solo aparece para admins
   - Link "Admin Panel" con icono 🔒

2. **Desde Dashboard Personal**:
   - Botón "Administración" si es admin

3. **URL Directa**:
   - Ir a `http://localhost:8000/admin-panel/`

## 🛡️ Seguridad y Mejores Prácticas

### Recomendaciones

1. **Revisar logs regularmente**: Al menos semanalmente
2. **Limpiar logs antiguos**: Cuando excedan 100 MB
3. **Descargar backups**: Antes de limpiar logs importantes
4. **Monitorear intentos de acceso**: Revisar `security.log` diariamente
5. **Alertas automáticas**: Configurar para errores CRITICAL
6. **Rotación automática**: Ya configurada, no requiere intervención

### Protecciones Implementadas

- ✅ Solo administradores pueden acceder
- ✅ Protección CSRF en operaciones destructivas
- ✅ Backup automático antes de limpiar
- ✅ Logs de auditoría para todas las acciones
- ✅ Rate limiting para prevenir abuso
- ✅ Sanitización de paths para prevenir directory traversal

## 📝 Mantenimiento

### Tareas Periódicas

| Frecuencia | Tarea | Acción |
|------------|-------|--------|
| Diaria | Revisar errores críticos | Filtrar por CRITICAL/ERROR |
| Semanal | Revisar seguridad | Analizar security.log |
| Mensual | Limpieza de logs | Descargar y limpiar logs antiguos |
| Trimestral | Auditoría completa | Análisis profundo de todos los logs |

### Comandos Útiles

```bash
# Ver tamaño de logs
ls -lh logs/

# Contar errores en el último día
grep ERROR logs/error.log | grep "2024-01-15"

# Buscar intentos de login fallidos
grep "Login failed" logs/security.log

# Ver últimas 100 líneas de logs generales
tail -n 100 logs/general.log
```

## 📞 Soporte

Para problemas con el sistema de logs:

1. Verificar permisos del directorio `logs/`
2. Verificar configuración en `settings.py`
3. Revisar que el usuario sea admin en la base de datos
4. Verificar logs de error del servidor

---

**Última actualización**: Enero 2024  
**Versión del sistema**: 1.0  
**Compatible con**: Django 5.0.1+
