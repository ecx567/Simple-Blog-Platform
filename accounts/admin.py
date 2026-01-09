"""
Configuración del panel de administración para el modelo de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Administración personalizada para el modelo CustomUser.
    """
    model = CustomUser
    list_display = ['email', 'username', 'role', 'is_active', 'is_email_verified', 'date_joined']
    list_filter = ['role', 'is_active', 'is_email_verified', 'is_staff', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Grupos y Permisos', {'fields': ('groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_active', 'is_email_verified'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']

