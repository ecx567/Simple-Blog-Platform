"""
Decoradores personalizados para control de acceso basado en roles.
"""

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps


def role_required(allowed_roles):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    
    Args:
        allowed_roles (list): Lista de roles permitidos ('admin', 'author', 'reader')
    
    Usage:
        @role_required(['admin', 'author'])
        def my_view(request):
            pass
    
    Raises:
        PermissionDenied: Si el usuario no tiene un rol permitido
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied(
                    f'No tienes permiso para acceder a esta página. Requiere rol: {", ".join(allowed_roles)}'
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador que permite acceso solo a administradores.
    
    Usage:
        @admin_required
        def admin_view(request):
            pass
    """
    return role_required(['admin'])(view_func)


def author_required(view_func):
    """
    Decorador que permite acceso a autores y administradores.
    
    Usage:
        @author_required
        def create_post(request):
            pass
    """
    return role_required(['admin', 'author'])(view_func)


def email_verified_required(view_func):
    """
    Decorador que requiere que el email del usuario esté verificado.
    
    Usage:
        @email_verified_required
        def sensitive_action(request):
            pass
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_email_verified:
            raise PermissionDenied('Debes verificar tu email para acceder a esta función.')
        return view_func(request, *args, **kwargs)
    return wrapper
