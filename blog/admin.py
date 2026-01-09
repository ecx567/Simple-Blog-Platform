"""
Configuración del panel de administración para los modelos del blog.
"""

from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administración de categorías."""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def post_count(self, obj):
        """Muestra el número de posts en la categoría."""
        return obj.posts.count()
    post_count.short_description = 'Publicaciones'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Administración de etiquetas."""
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']
    
    def post_count(self, obj):
        """Muestra el número de posts con esta etiqueta."""
        return obj.posts.count()
    post_count.short_description = 'Publicaciones'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Administración de publicaciones."""
    list_display = ['title', 'author', 'category', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'created_at', 'category', 'author']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    raw_id_fields = ['author']
    filter_horizontal = ['tags']
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Clasificación', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Publicación', {
            'fields': ('status', 'published_at')
        }),
        ('Estadísticas', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['views_count']
    
    def save_model(self, request, obj, form, change):
        """Establece el autor automáticamente si es nuevo post."""
        if not change:  # Si es un post nuevo
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Administración de comentarios."""
    list_display = ['user', 'post', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'user__username', 'post__title']
    raw_id_fields = ['user', 'post', 'parent']
    actions = ['approve_comments', 'disapprove_comments']
    
    def content_preview(self, obj):
        """Muestra un preview del contenido."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'
    
    def approve_comments(self, request, queryset):
        """Acción para aprobar comentarios."""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comentario(s) aprobado(s).')
    approve_comments.short_description = 'Aprobar comentarios seleccionados'
    
    def disapprove_comments(self, request, queryset):
        """Acción para desaprobar comentarios."""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comentario(s) desaprobado(s).')
    disapprove_comments.short_description = 'Desaprobar comentarios seleccionados'
