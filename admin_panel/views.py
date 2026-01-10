"""
Vistas para el sistema de administración y monitoreo.

Solo accesible para usuarios administradores.
"""

import os
import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from accounts.decorators import admin_required

logger = logging.getLogger(__name__)


@login_required
@admin_required
def admin_dashboard(request):
    """
    Dashboard principal para administradores con estadísticas del sistema.
    """
    from accounts.models import CustomUser
    from blog.models import Post, Comment, Category, Tag
    
    # Estadísticas de usuarios
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    admins = CustomUser.objects.filter(role='admin').count()
    authors = CustomUser.objects.filter(role='author').count()
    readers = CustomUser.objects.filter(role='reader').count()
    
    # Estadísticas de contenido
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    total_comments = Comment.objects.count()
    approved_comments = Comment.objects.filter(is_approved=True).count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    
    # Categorías y Tags
    total_categories = Category.objects.count()
    total_tags = Tag.objects.count()
    
    # Posts más vistos (top 5)
    top_posts = Post.published.all().order_by('-views_count')[:5]
    
    # Usuarios registrados recientemente (últimos 7 días)
    week_ago = datetime.now() - timedelta(days=7)
    recent_users = CustomUser.objects.filter(date_joined__gte=week_ago).count()
    
    # Logs disponibles
    logs_dir = settings.BASE_DIR / 'logs'
    log_files = []
    if logs_dir.exists():
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                file_path = logs_dir / file
                file_size = os.path.getsize(file_path)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                log_files.append({
                    'name': file,
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'modified': file_modified,
                })
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'admins': admins,
        'authors': authors,
        'readers': readers,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_comments': total_comments,
        'approved_comments': approved_comments,
        'pending_comments': pending_comments,
        'total_categories': total_categories,
        'total_tags': total_tags,
        'top_posts': top_posts,
        'recent_users': recent_users,
        'log_files': log_files,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@admin_required
def view_logs(request):
    """
    Vista para visualizar logs del sistema.
    """
    log_type = request.GET.get('type', 'general')
    search_query = request.GET.get('q', '')
    level_filter = request.GET.get('level', '')
    
    # Mapeo de tipos de log a archivos
    log_files = {
        'general': 'general.log',
        'error': 'error.log',
        'security': 'security.log',
        'database': 'database.log',
    }
    
    log_filename = log_files.get(log_type, 'general.log')
    log_path = settings.BASE_DIR / 'logs' / log_filename
    
    log_entries = []
    
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Procesar últimas 500 líneas (más recientes)
                lines = lines[-500:]
                
                for line in reversed(lines):  # Más recientes primero
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Filtrar por búsqueda
                    if search_query and search_query.lower() not in line.lower():
                        continue
                    
                    # Filtrar por nivel
                    if level_filter:
                        if f'[{level_filter}]' not in line:
                            continue
                    
                    # Parsear línea de log
                    entry = parse_log_line(line)
                    log_entries.append(entry)
        
        except Exception as e:
            logger.error(f"Error al leer archivo de log {log_filename}: {e}")
            log_entries.append({
                'level': 'ERROR',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'message': f'Error al leer el archivo de log: {str(e)}',
                'raw': str(e),
            })
    else:
        log_entries.append({
            'level': 'INFO',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'No se encontró el archivo de log. Se creará cuando ocurra el primer evento.',
            'raw': '',
        })
    
    # Paginación
    paginator = Paginator(log_entries, 50)
    page = request.GET.get('page')
    log_entries_page = paginator.get_page(page)
    
    # Estadísticas de logs
    log_stats = {
        'total': len(log_entries),
        'error': sum(1 for e in log_entries if e['level'] == 'ERROR'),
        'warning': sum(1 for e in log_entries if e['level'] == 'WARNING'),
        'info': sum(1 for e in log_entries if e['level'] == 'INFO'),
        'debug': sum(1 for e in log_entries if e['level'] == 'DEBUG'),
    }
    
    context = {
        'log_type': log_type,
        'log_entries': log_entries_page,
        'search_query': search_query,
        'level_filter': level_filter,
        'log_stats': log_stats,
        'log_types': log_files.keys(),
    }
    
    return render(request, 'admin_panel/logs.html', context)


@login_required
@admin_required
def download_log(request, log_type):
    """
    Descargar archivo de log completo.
    """
    log_files = {
        'general': 'general.log',
        'error': 'error.log',
        'security': 'security.log',
        'database': 'database.log',
    }
    
    log_filename = log_files.get(log_type)
    if not log_filename:
        return HttpResponse("Log no encontrado", status=404)
    
    log_path = settings.BASE_DIR / 'logs' / log_filename
    
    if not log_path.exists():
        return HttpResponse("Archivo de log no existe", status=404)
    
    try:
        with open(log_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{log_filename}"'
            return response
    except Exception as e:
        logger.error(f"Error al descargar log {log_filename}: {e}")
        return HttpResponse(f"Error al descargar log: {str(e)}", status=500)


@login_required
@admin_required
def clear_log(request, log_type):
    """
    Limpiar un archivo de log específico (requiere confirmación POST).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    log_files = {
        'general': 'general.log',
        'error': 'error.log',
        'security': 'security.log',
        'database': 'database.log',
    }
    
    log_filename = log_files.get(log_type)
    if not log_filename:
        return JsonResponse({'error': 'Log no encontrado'}, status=404)
    
    log_path = settings.BASE_DIR / 'logs' / log_filename
    
    try:
        if log_path.exists():
            # Hacer backup antes de limpiar
            backup_path = settings.BASE_DIR / 'logs' / f'{log_filename}.backup'
            with open(log_path, 'r') as f_in:
                with open(backup_path, 'w') as f_out:
                    f_out.write(f_in.read())
            
            # Limpiar el archivo
            with open(log_path, 'w') as f:
                f.write('')
            
            logger.info(f"Log {log_filename} limpiado por usuario {request.user.username}")
            
            return JsonResponse({
                'success': True,
                'message': f'Log {log_type} limpiado exitosamente. Se creó un backup.'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Archivo de log no existe'
            })
    
    except Exception as e:
        logger.error(f"Error al limpiar log {log_filename}: {e}")
        return JsonResponse({
            'error': f'Error al limpiar log: {str(e)}'
        }, status=500)


def parse_log_line(line):
    """
    Parsear una línea de log y extraer información relevante.
    """
    import re
    
    # Formato: [LEVEL] timestamp module message
    # Ejemplo: [INFO] 2026-01-09 20:00:00,123 module 12345 67890 message
    
    entry = {
        'level': 'UNKNOWN',
        'timestamp': '',
        'module': '',
        'message': '',
        'raw': line,
    }
    
    # Extraer nivel
    level_match = re.search(r'\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]', line)
    if level_match:
        entry['level'] = level_match.group(1)
    
    # Extraer timestamp (formato: YYYY-MM-DD HH:MM:SS,mmm)
    timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})?', line)
    if timestamp_match:
        entry['timestamp'] = timestamp_match.group(0)
    
    # Extraer módulo
    module_match = re.search(r'\] \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})? (\w+)', line)
    if module_match:
        entry['module'] = module_match.group(1)
    
    # Extraer mensaje (después del último número de proceso/thread)
    message_match = re.search(r'\d+ \d+ (.+)$', line)
    if message_match:
        entry['message'] = message_match.group(1)
    else:
        # Si no hay proceso/thread, tomar todo después del timestamp
        parts = line.split('] ', 1)
        if len(parts) > 1:
            remaining = parts[1]
            # Saltar timestamp y módulo
            message_parts = remaining.split(None, 3)
            if len(message_parts) > 2:
                entry['message'] = message_parts[-1]
            else:
                entry['message'] = remaining
    
    return entry


@login_required
@admin_required
def system_status(request):
    """
    Vista para ver el estado del sistema en tiempo real.
    """
    import sys
    import django
    from django.db import connection
    
    # Información del sistema
    system_info = {
        'python_version': sys.version,
        'django_version': django.get_version(),
        'database': connection.settings_dict['ENGINE'].split('.')[-1],
        'debug_mode': settings.DEBUG,
    }
    
    # Información de la base de datos
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = 'Conectada'
    except Exception as e:
        db_status = f'Error: {str(e)}'
    
    # Espacio en disco de logs
    logs_dir = settings.BASE_DIR / 'logs'
    total_log_size = 0
    if logs_dir.exists():
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                total_log_size += os.path.getsize(logs_dir / file)
    
    context = {
        'system_info': system_info,
        'db_status': db_status,
        'total_log_size': round(total_log_size / (1024 * 1024), 2),  # MB
    }
    
    return render(request, 'admin_panel/system_status.html', context)
