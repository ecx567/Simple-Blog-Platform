"""
Modelos personalizados de usuario para el sistema de autenticación.

Este módulo contiene el modelo de usuario personalizado que extiende 
AbstractBaseUser y PermissionsMixin de Django para implementar un sistema 
de autenticación basado en email con roles.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator


class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo CustomUser.
    
    Maneja la creación de usuarios regulares y superusuarios.
    """
    
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Crea y guarda un usuario regular.
        
        Args:
            email (str): Email del usuario (usado para login)
            username (str): Nombre de usuario único
            password (str): Contraseña en texto plano (se hasheará)
            **extra_fields: Campos adicionales del modelo
            
        Returns:
            CustomUser: Instancia del usuario creado
            
        Raises:
            ValueError: Si el email no es proporcionado
        """
        if not email:
            raise ValueError('El email es obligatorio')
        if not username:
            raise ValueError('El username es obligatorio')
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash automático de contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Crea y guarda un superusuario.
        
        Args:
            email (str): Email del superusuario
            username (str): Nombre de usuario
            password (str): Contraseña
            **extra_fields: Campos adicionales
            
        Returns:
            CustomUser: Instancia del superusuario creado
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado.
    
    Usa email como identificador único para autenticación.
    Incluye sistema de roles (admin, author, reader).
    """
    
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('author', 'Autor'),
        ('reader', 'Lector'),
    ]
    
    # Campos principales
    email = models.EmailField(
        'Email',
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': 'Ya existe un usuario con este email.',
        }
    )
    username = models.CharField(
        'Nombre de usuario',
        max_length=150,
        unique=True,
        db_index=True,
        error_messages={
            'unique': 'Ya existe un usuario con este nombre.',
        }
    )
    first_name = models.CharField('Nombre', max_length=150, blank=True)
    last_name = models.CharField('Apellido', max_length=150, blank=True)
    
    # Sistema de roles
    role = models.CharField(
        'Rol',
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader'
    )
    
    # Estados y permisos
    is_active = models.BooleanField(
        'Activo',
        default=False,
        help_text='Debe verificar su email para activar la cuenta.'
    )
    is_staff = models.BooleanField('Staff', default=False)
    is_email_verified = models.BooleanField('Email verificado', default=False)
    
    # Metadatos
    date_joined = models.DateTimeField('Fecha de registro', default=timezone.now)
    last_login = models.DateTimeField('Último login', null=True, blank=True)
    
    # Manager
    objects = CustomUserManager()
    
    # Configuración de autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['username']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        """Representación en string del usuario."""
        return self.email
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.username
    
    def get_short_name(self):
        """Retorna el nombre corto del usuario."""
        return self.first_name or self.username
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador."""
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_author(self):
        """Verifica si el usuario es autor."""
        return self.role == 'author' or self.is_admin
    
    @property
    def can_publish(self):
        """Verifica si el usuario puede publicar posts."""
        return self.is_author or self.is_admin

