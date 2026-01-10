"""
URL configuration for blog_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
from . import views

# Handlers para errores HTTP
handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Admin Panel Personalizado (solo para administradores)
    path('admin-panel/', include('admin_panel.urls')),
    
    # Home
    path('', account_views.home, name='home'),
    
    # Accounts (Autenticación)
    path('accounts/', include('accounts.urls')),
    
    # Blog
    path('blog/', include('blog.urls')),
]

# Servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
