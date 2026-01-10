"""
Script para generar logs de prueba en el sistema
Ejecutar con: python generate_test_logs.py
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Asegurar que el directorio logs existe
os.makedirs('logs', exist_ok=True)

# Configurar formatters
verbose_formatter = logging.Formatter(
    '[{levelname}] {asctime} - {module} (Process: {process:d} Thread: {thread:d}) - {message}',
    style='{'
)

simple_formatter = logging.Formatter(
    '[{levelname}] {asctime} - {message}',
    style='{'
)

# Función para configurar logger
def setup_logger(name, log_file, level=logging.INFO):
    handler = RotatingFileHandler(
        f'logs/{log_file}',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    handler.setFormatter(verbose_formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Crear loggers para diferentes tipos
general_logger = setup_logger('general', 'general.log', logging.DEBUG)
error_logger = setup_logger('error', 'error.log', logging.ERROR)
security_logger = setup_logger('security', 'security.log', logging.INFO)
database_logger = setup_logger('database', 'database.log', logging.DEBUG)

print("Generando logs de prueba...")
print("=" * 60)

# GENERAL LOGS
print("\n📝 Generando logs generales...")
general_logger.debug("Modo de depuración activado")
general_logger.info("Aplicación iniciada correctamente")
general_logger.info("Usuario 'admin' inició sesión desde IP 192.168.1.100")
general_logger.info("Nuevo post creado: 'Mi primer artículo' por usuario 'autor1'")
general_logger.info("Comentario aprobado en post 'Django Tutorial'")
general_logger.warning("Cache de la aplicación está lleno, considere limpiar")
general_logger.info("Usuario 'lector1' visualizó el post 'Python Avanzado'")

# ERROR LOGS
print("❌ Generando logs de error...")
error_logger.error("Error al conectar con la base de datos: Connection timeout")
error_logger.error("Formulario de registro inválido: Email ya existe")
error_logger.critical("Memoria del servidor casi agotada: 95% usado")
error_logger.error("Error 404: Página no encontrada '/blog/post/999'")
error_logger.error("Error al procesar imagen: Formato no soportado")
error_logger.critical("Error crítico: No se puede escribir en disco")

# SECURITY LOGS
print("🔒 Generando logs de seguridad...")
security_logger.info("Inicio de sesión exitoso: usuario 'admin' desde 192.168.1.100")
security_logger.warning("Intento de login fallido: usuario 'hacker' - contraseña incorrecta")
security_logger.warning("Rate limit alcanzado para IP 203.0.113.0 en endpoint /login/")
security_logger.error("Intento de acceso no autorizado: usuario 'lector1' intentó acceder a /admin-panel/")
security_logger.info("Contraseña cambiada exitosamente para usuario 'autor2'")
security_logger.warning("Usuario 'guest' intentó acceder a post borrador sin permisos")
security_logger.critical("Múltiples intentos de login fallidos detectados desde IP 203.0.113.5")
security_logger.info("Token CSRF validado correctamente para formulario de post")
security_logger.error("Intento de SQL injection detectado y bloqueado")
security_logger.info("Sesión cerrada para usuario 'admin'")

# DATABASE LOGS
print("🗄️ Generando logs de base de datos...")
database_logger.debug("Query ejecutada: SELECT * FROM blog_post WHERE status='published' [Tiempo: 0.023s]")
database_logger.debug("Query ejecutada: SELECT COUNT(*) FROM accounts_user [Tiempo: 0.005s]")
database_logger.info("Migración aplicada: 0001_initial")
database_logger.warning("Query lenta detectada: SELECT * FROM blog_comment JOIN blog_post [Tiempo: 2.345s]")
database_logger.debug("Conexión establecida con PostgreSQL en localhost:5432")
database_logger.error("Error de integridad: Violación de clave única en tabla accounts_user")
database_logger.debug("Transaction committed exitosamente")
database_logger.info("Índice creado en tabla blog_post para campo 'created_at'")

print("\n" + "=" * 60)
print("✅ Logs de prueba generados exitosamente!")
print("\nArchivos creados:")
print("  - logs/general.log")
print("  - logs/error.log")
print("  - logs/security.log")
print("  - logs/database.log")
print("\nPuedes ver estos logs en: http://localhost:8000/admin-panel/logs/")
print("=" * 60)
