"""
Vistas para el sistema de autenticación.

Incluye vistas para registro, login, logout, verificación de email,
y recuperación de contraseña.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

from .forms import RegistrationForm, LoginForm
from .models import CustomUser


def register(request):
    """
    Vista de registro de nuevos usuarios.
    
    Proceso:
    1. Usuario completa formulario
    2. Se crea usuario inactivo
    3. Se envía email de verificación
    4. Usuario debe verificar email para activar cuenta
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Crear usuario inactivo
            user = form.save(commit=False)
            user.is_active = False  # Requiere verificación de email
            user.is_email_verified = False
            user.save()
            
            # Enviar email de verificación
            send_verification_email(request, user)
            
            messages.success(
                request,
                'Registro exitoso. Por favor verifica tu email para activar tu cuenta.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def send_verification_email(request, user):
    """
    Envía email de verificación al usuario.
    
    Args:
        request: HttpRequest object
        user: Instancia de CustomUser
    """
    # Generar token de verificación
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Construir URL de verificación
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    # Preparar email
    subject = 'Verifica tu cuenta - Blog Platform'
    message = f'''
    Hola {user.username},
    
    Gracias por registrarte en Blog Platform.
    
    Por favor verifica tu cuenta haciendo clic en el siguiente enlace:
    {verification_link}
    
    Este enlace expirará en 24 horas.
    
    Si no solicitaste esta cuenta, ignora este email.
    
    Saludos,
    El equipo de Blog Platform
    '''
    
    # Enviar email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER or 'noreply@blogplatform.com',
        [user.email],
        fail_silently=False,
    )


def verify_email(request, uidb64, token):
    """
    Vista de verificación de email.
    
    Valida el token y activa la cuenta del usuario.
    """
    try:
        # Decodificar user id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        # Activar usuario
        user.is_active = True
        user.is_email_verified = True
        user.save()
        
        messages.success(
            request,
            '¡Email verificado exitosamente! Ahora puedes iniciar sesión.'
        )
        return redirect('login')
    else:
        messages.error(
            request,
            'El enlace de verificación es inválido o ha expirado.'
        )
        return redirect('register')


def login_view(request):
    """
    Vista de inicio de sesión.
    
    Proceso:
    1. Validar credenciales
    2. Verificar que la cuenta esté activa
    3. Crear sesión
    4. Redirigir a dashboard
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username es email en nuestro caso
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Autenticar usuario
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    # Login exitoso
                    auth_login(request, user)
                    
                    # Actualizar last_login
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    
                    # Configurar duración de sesión
                    if not remember_me:
                        # Sesión expira al cerrar navegador
                        request.session.set_expiry(0)
                    else:
                        # Sesión dura 2 semanas
                        request.session.set_expiry(1209600)
                    
                    messages.success(request, f'¡Bienvenido, {user.username}!')
                    
                    # Redirigir a página solicitada o dashboard
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(
                        request,
                        'Tu cuenta no está activa. Por favor verifica tu email.'
                    )
            else:
                messages.error(request, 'Email o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Vista de cierre de sesión.
    
    POST request: Cierra la sesión
    GET request: Muestra confirmación
    """
    if request.method == 'POST':
        username = request.user.username
        auth_logout(request)
        messages.info(request, f'Has cerrado sesión exitosamente, {username}.')
        return redirect('home')
    
    return render(request, 'accounts/logout_confirm.html')


@login_required
def dashboard(request):
    """
    Vista del dashboard del usuario autenticado.
    
    Muestra información personalizada según el rol del usuario.
    """
    context = {
        'user': request.user,
        'total_posts': 0,  # Se actualizará cuando tengamos el modelo Post
        'total_comments': 0,  # Se actualizará cuando tengamos el modelo Comment
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """
    Vista de perfil de usuario.
    
    Permite ver y editar información del perfil.
    """
    context = {
        'user': request.user,
    }
    
    return render(request, 'accounts/profile.html', context)


def home(request):
    """
    Vista de la página de inicio.
    """
    return render(request, 'home.html')

