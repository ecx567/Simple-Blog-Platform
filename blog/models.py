"""
Modelos para el sistema de blog.

Este módulo contiene los modelos para publicaciones, categorías,
etiquetas y comentarios del blog.
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from accounts.models import CustomUser


class Category(models.Model):
    """
    Modelo de categorías para organizar publicaciones.
    """
    name = models.CharField('Nombre', max_length=100, unique=True)
    slug = models.SlugField('Slug', unique=True, db_index=True)
    description = models.TextField('Descripción', blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_list') + f'?category={self.slug}'


class Tag(models.Model):
    """
    Modelo de etiquetas para categorizar publicaciones.
    """
    name = models.CharField('Nombre', max_length=50, unique=True)
    slug = models.SlugField('Slug', unique=True, db_index=True)
    
    class Meta:
        db_table = 'tags'
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    """
    Manager personalizado para obtener solo publicaciones publicadas.
    """
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """
    Modelo de publicaciones del blog.
    """
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    ]
    
    # Relaciones
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='Autor'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Categoría'
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name='posts', 
        blank=True,
        verbose_name='Etiquetas'
    )
    
    # Contenido
    title = models.CharField('Título', max_length=200, db_index=True)
    slug = models.SlugField('Slug', unique=True, max_length=200, db_index=True)
    content = models.TextField('Contenido')
    excerpt = models.TextField('Extracto', max_length=300, blank=True, 
                               help_text='Resumen breve del post')
    featured_image = models.ImageField(
        'Imagen destacada',
        upload_to='posts/%Y/%m/%d/', 
        blank=True, 
        null=True
    )
    
    # Estado
    status = models.CharField(
        'Estado',
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft',
        db_index=True
    )
    
    # Estadísticas
    views_count = models.PositiveIntegerField('Vistas', default=0)
    
    # Metadatos temporales
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    published_at = models.DateTimeField('Fecha de publicación', null=True, blank=True)
    
    # Managers
    objects = models.Manager()  # Manager por defecto
    published = PublishedManager()  # Solo publicados
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generar slug si no existe
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        
        # Establecer fecha de publicación
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # Generar excerpt si está vacío
        if not self.excerpt and self.content:
            self.excerpt = self.content[:280] + '...' if len(self.content) > 280 else self.content
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    @property
    def reading_time(self):
        """Calcula el tiempo estimado de lectura en minutos."""
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count / words_per_minute
        return max(1, round(minutes))
    
    @property
    def comment_count(self):
        """Retorna el número de comentarios aprobados."""
        return self.comments.filter(is_approved=True).count()


class Comment(models.Model):
    """
    Modelo de comentarios en publicaciones.
    Soporta comentarios anidados (respuestas).
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Publicación'
    )
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Usuario'
    )
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Respuesta a'
    )
    
    content = models.TextField('Contenido')
    is_approved = models.BooleanField('Aprobado', default=True)
    
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f'Comentario de {self.user.username} en {self.post.title}'
    
    @property
    def is_reply(self):
        """Verifica si es una respuesta a otro comentario."""
        return self.parent is not None
