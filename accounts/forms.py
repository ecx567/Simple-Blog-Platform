"""
Formularios para el sistema de autenticación.

Incluye formularios para registro, login, recuperación de contraseña
y perfil de usuario.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from .models import CustomUser
import re


class RegistrationForm(UserCreationForm):
    """
    Formulario de registro de nuevos usuarios.
    
    Incluye validación personalizada de contraseñas con política de seguridad.
    """
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email'
        })
    )
    
    username = forms.CharField(
        label='Nombre de usuario',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario123',
            'autocomplete': 'username'
        })
    )
    
    first_name = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Juan'
        })
    )
    
    last_name = forms.CharField(
        label='Apellido',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pérez'
        })
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña segura',
            'autocomplete': 'new-password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repetir contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        """Valida que el email no esté registrado."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email.lower()
    
    def clean_username(self):
        """Valida que el username no esté registrado y cumpla con el formato."""
        username = self.cleaned_data.get('username')
        
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        
        if len(username) < 3:
            raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('El nombre de usuario solo puede contener letras, números y guiones bajos.')
        
        return username
    
    def clean_password1(self):
        """
        Valida la contraseña con política de seguridad robusta.
        
        Requisitos:
        - Mínimo 8 caracteres
        - Al menos una mayúscula
        - Al menos una minúscula
        - Al menos un número
        - Al menos un carácter especial
        """
        password = self.cleaned_data.get('password1')
        
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        
        if not re.search(r'[0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un número.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (!@#$%^&*).')
        
        return password


class LoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesión.
    
    Permite login con email y contraseña, incluye opción "Recuérdame".
    """
    
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True,
            'autocomplete': 'email'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )
    
    remember_me = forms.BooleanField(
        label='Recuérdame',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulario de recuperación de contraseña.
    """
    
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Formulario para edición de perfil de usuario.
    """
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Email no se puede cambiar (requiere verificación)
        self.fields['email'].disabled = True
