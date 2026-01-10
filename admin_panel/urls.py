"""
URLs para el panel de administración personalizado.
Solo accesible para administradores.
"""

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard principal
    path('', views.admin_dashboard, name='dashboard'),
    
    # Visualización de logs
    path('logs/', views.view_logs, name='logs'),
    path('logs/download/<str:log_type>/', views.download_log, name='download_log'),
    path('logs/clear/<str:log_type>/', views.clear_log, name='clear_log'),
    
    # Estado del sistema
    path('system/', views.system_status, name='system_status'),
]
