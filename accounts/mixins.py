"""
Mixins personalizados para Class-Based Views con control de acceso basado en roles.
"""

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que verifica si el usuario tiene uno de los roles permitidos.
    
    Usage:
        class MyView(RoleRequiredMixin, ListView):
            allowed_roles = ['admin', 'author']
            model = Post
    """
    allowed_roles = []
    
    def test_func(self):
        """Verifica si el usuario tiene un rol permitido."""
        return self.request.user.role in self.allowed_roles
    
    def handle_no_permission(self):
        """Maneja el caso cuando el usuario no tiene permiso."""
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                f'No tienes permiso para acceder a esta página. Requiere rol: {", ".join(self.allowed_roles)}'
            )
        return super().handle_no_permission()


class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin que permite acceso solo a administradores.
    
    Usage:
        class AdminPanelView(AdminRequiredMixin, TemplateView):
            template_name = 'admin_panel.html'
    """
    allowed_roles = ['admin']


class AuthorRequiredMixin(RoleRequiredMixin):
    """
    Mixin que permite acceso a autores y administradores.
    
    Usage:
        class CreatePostView(AuthorRequiredMixin, CreateView):
            model = Post
            fields = ['title', 'content']
    """
    allowed_roles = ['admin', 'author']


class EmailVerifiedRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que requiere que el email del usuario esté verificado.
    
    Usage:
        class SensitiveView(EmailVerifiedRequiredMixin, View):
            pass
    """
    
    def test_func(self):
        """Verifica si el email del usuario está verificado."""
        return self.request.user.is_email_verified
    
    def handle_no_permission(self):
        """Maneja el caso cuando el email no está verificado."""
        if self.request.user.is_authenticated:
            raise PermissionDenied('Debes verificar tu email para acceder a esta función.')
        return super().handle_no_permission()


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que verifica si el usuario es el propietario del objeto.
    
    El modelo debe tener un campo 'author' o 'user' que apunte al usuario.
    
    Usage:
        class UpdatePostView(OwnerRequiredMixin, UpdateView):
            model = Post
            owner_field = 'author'  # Campo que apunta al usuario
    """
    owner_field = 'author'  # Por defecto busca el campo 'author'
    
    def test_func(self):
        """Verifica si el usuario es el propietario o es admin."""
        obj = self.get_object()
        user = self.request.user
        
        # Admin siempre tiene permiso
        if user.is_admin:
            return True
        
        # Verificar si el usuario es el propietario
        owner = getattr(obj, self.owner_field, None)
        return owner == user
    
    def handle_no_permission(self):
        """Maneja el caso cuando el usuario no es el propietario."""
        if self.request.user.is_authenticated:
            raise PermissionDenied('No tienes permiso para modificar este recurso.')
        return super().handle_no_permission()
