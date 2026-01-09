"""
URL configuration for blog_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', account_views.home, name='home'),
    
    # Accounts (Autenticación)
    path('accounts/', include('accounts.urls')),
    
    # Blog (se agregará después)
    # path('blog/', include('blog.urls')),
]

# Servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
