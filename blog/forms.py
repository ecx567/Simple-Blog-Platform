"""
Formularios para el sistema de blog.

Incluye formularios para crear y editar publicaciones, y comentarios.
"""

from django import forms
from .models import Post, Comment, Category, Tag


class PostForm(forms.ModelForm):
    """
    Formulario para crear y editar publicaciones.
    """
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'tags', 'featured_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la publicación'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Contenido de la publicación...'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resumen breve (opcional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'excerpt': 'Extracto',
            'category': 'Categoría',
            'tags': 'Etiquetas',
            'featured_image': 'Imagen destacada',
            'status': 'Estado',
        }
        help_texts = {
            'excerpt': 'Resumen breve que aparecerá en la lista de publicaciones',
            'tags': 'Mantén presionado Ctrl (Cmd en Mac) para seleccionar múltiples',
        }
    
    def clean_title(self):
        """Valida que el título no esté vacío y tenga longitud adecuada."""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        return title
    
    def clean_content(self):
        """Valida que el contenido tenga suficiente longitud."""
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError('El contenido debe tener al menos 50 caracteres.')
        return content


class CommentForm(forms.ModelForm):
    """
    Formulario para crear comentarios.
    """
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu comentario...'
            }),
        }
        labels = {
            'content': 'Comentario',
        }
    
    def clean_content(self):
        """Valida que el comentario no esté vacío."""
        content = self.cleaned_data.get('content')
        if len(content) < 3:
            raise forms.ValidationError('El comentario debe tener al menos 3 caracteres.')
        if len(content) > 1000:
            raise forms.ValidationError('El comentario no puede exceder 1000 caracteres.')
        return content


class PostSearchForm(forms.Form):
    """
    Formulario para búsqueda de publicaciones.
    """
    query = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar publicaciones...'
        })
    )
    
    category = forms.ModelChoiceField(
        label='Categoría',
        queryset=Category.objects.all(),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    tag = forms.ModelChoiceField(
        label='Etiqueta',
        queryset=Tag.objects.all(),
        required=False,
        empty_label='Todas las etiquetas',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
