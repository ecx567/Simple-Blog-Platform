"""
Tests para el sistema de autenticación.

Tests de:
- Registro de usuarios
- Login y logout
- Verificación de email
- Roles y permisos
- Recuperación de contraseña
"""

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Tests para el registro de usuarios."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = Client()
        self.register_url = reverse('register')
        
    def test_registration_page_loads(self):
        """Test que la página de registro carga correctamente."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        
    def test_user_registration_success(self):
        """Test que un usuario puede registrarse exitosamente."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        response = self.client.post(self.register_url, data)
        
        # Verifica que se creó el usuario
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Verifica que el usuario está inactivo hasta verificar email
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_email_verified)


class UserLoginTestCase(TestCase):
    """Tests para el login de usuarios."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = Client()
        self.login_url = reverse('login')
        
        # Crear usuario de prueba activo
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            is_active=True,
            is_email_verified=True
        )
        
    def test_login_page_loads(self):
        """Test que la página de login carga correctamente."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_login_with_valid_credentials_success(self):
        """Test que un usuario puede iniciar sesión con credenciales válidas."""
        data = {
            'username': 'test@example.com',  # LoginForm usa 'username' como campo
            'password': 'TestPass123!',
        }
        response = self.client.post(self.login_url, data, follow=True)
        
        # Verifica que el usuario está autenticado después del redirect
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class UserRolesTestCase(TestCase):
    """Tests para roles y permisos de usuarios."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            role='admin',
            is_active=True,
            is_email_verified=True
        )
        
        self.author_user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='AuthorPass123!',
            role='author',
            is_active=True,
            is_email_verified=True
        )
        
        self.reader_user = User.objects.create_user(
            username='reader',
            email='reader@example.com',
            password='ReaderPass123!',
            role='reader',
            is_active=True,
            is_email_verified=True
        )
        
    def test_admin_has_admin_role(self):
        """Test que admin tiene rol de administrador."""
        self.assertTrue(self.admin_user.is_admin)
        self.assertEqual(self.admin_user.role, 'admin')
        
    def test_author_has_author_role(self):
        """Test que author tiene rol de autor."""
        self.assertTrue(self.author_user.is_author)
        self.assertEqual(self.author_user.role, 'author')
        
    def test_author_can_publish(self):
        """Test que autores tienen permiso para publicar."""
        self.assertTrue(self.author_user.can_publish)
        self.assertTrue(self.admin_user.can_publish)
        self.assertFalse(self.reader_user.can_publish)
