"""
Vistas personalizadas para manejar errores HTTP.
"""

from django.shortcuts import render


def ratelimit_error(request, exception=None):
    """
    Vista personalizada para el error 429 (Too Many Requests).
    Se muestra cuando se excede el límite de intentos.
    """
    return render(request, '403.html', status=429)


def handler404(request, exception=None):
    """
    Vista personalizada para el error 404 (Not Found).
    """
    return render(request, '404.html', status=404)


def handler500(request, exception=None):
    """
    Vista personalizada para el error 500 (Internal Server Error).
    """
    return render(request, '500.html', status=500)
