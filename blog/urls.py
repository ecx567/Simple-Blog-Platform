"""
URLs para el sistema de blog.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Lista de posts
    path('', views.post_list, name='post_list'),
    
    # CRUD de posts (orden importante: específico antes que genérico)
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Mis posts
    path('my-posts/', views.my_posts, name='my_posts'),
    
    # Comentarios
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    
    # Categorías y etiquetas
    path('categories/', views.category_list, name='category_list'),
    path('tags/', views.tag_list, name='tag_list'),
]
