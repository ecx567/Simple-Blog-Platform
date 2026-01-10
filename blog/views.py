"""
Vistas para el sistema de blog.

Incluye vistas para listar, crear, editar y eliminar publicaciones,
así como para gestionar comentarios.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from accounts.decorators import author_required
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, PostSearchForm


def post_list(request):
    """
    Lista de publicaciones públicas con búsqueda y filtrado.
    """
    posts = Post.published.all().select_related('author', 'category').prefetch_related('tags')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    # Filtro por categoría
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Filtro por etiqueta
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Ordenamiento
    order = request.GET.get('order', '-created_at')
    valid_orders = ['-created_at', 'created_at', '-views_count', 'title']
    if order in valid_orders:
        posts = posts.order_by(order)
    
    # Paginación
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    
    # Datos para el sidebar
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:10]
    recent_posts = Post.published.all()[:5]
    
    context = {
        'posts': posts_page,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'query': query,
        'current_category': category_slug,
        'current_tag': tag_slug,
    }
    
    return render(request, 'blog/post_list.html', context)


@ratelimit(key='user_or_ip', rate='10/h', method='POST', block=True)
def post_detail(request, slug):
    """
    Detalle de una publicación con comentarios.
    Rate limit: 10 comentarios por hora por usuario o IP.
    """
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published'
    )
    
    # Incrementar contador de vistas
    Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
    post.refresh_from_db()
    
    # Comentarios (solo los principales, sin respuestas)
    comments = post.comments.filter(
        is_approved=True, 
        parent=None
    ).select_related('user').prefetch_related('replies')
    
    # Formulario de comentarios
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                
                # Si es una respuesta
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    parent_comment = get_object_or_404(Comment, id=parent_id)
                    comment.parent = parent_comment
                
                comment.save()
                messages.success(request, 'Comentario publicado exitosamente.')
                return redirect('post_detail', slug=post.slug)
        else:
            comment_form = CommentForm()
    
    # Posts relacionados (misma categoría)
    related_posts = Post.published.filter(
        category=post.category
    ).exclude(pk=post.pk)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)


@login_required
@author_required
def post_create(request):
    """
    Crear una nueva publicación.
    Solo autores y admins.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Guardar las relaciones ManyToMany (tags)
            
            messages.success(
                request, 
                f'Publicación "{post.title}" creada exitosamente como {post.get_status_display()}.'
            )
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Nueva Publicación'
    })


@login_required
def post_edit(request, slug):
    """
    Editar una publicación existente.
    Solo el autor o admin puede editar.
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Verificar permisos: debe ser el autor o admin
    if post.author != request.user and not request.user.is_admin:
        messages.error(request, 'No tienes permiso para editar esta publicación.')
        return HttpResponseForbidden('No tienes permiso para editar esta publicación.')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Publicación "{post.title}" actualizada exitosamente.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'title': f'Editar: {post.title}'
    })


@login_required
def post_delete(request, slug):
    """
    Eliminar una publicación.
    Solo el autor o admin puede eliminar.
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Verificar permisos
    if post.author != request.user and not request.user.is_admin:
        messages.error(request, 'No tienes permiso para eliminar esta publicación.')
        return HttpResponseForbidden('No tienes permiso para eliminar esta publicación.')
    
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Publicación "{title}" eliminada exitosamente.')
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def my_posts(request):
    """
    Lista de publicaciones del usuario actual.
    """
    posts = Post.objects.filter(author=request.user).select_related('category')
    
    # Estadísticas
    total_count = posts.count()
    published_count = posts.filter(status='published').count()
    draft_count = posts.filter(status='draft').count()
    total_views = sum(post.views_count for post in posts)
    
    # Filtro por estado
    status_filter = request.GET.get('status')
    if status_filter in ['draft', 'published']:
        posts = posts.filter(status=status_filter)
    
    # Paginación
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    
    context = {
        'posts': posts_page,
        'status_filter': status_filter,
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'total_views': total_views,
    }
    
    return render(request, 'blog/my_posts.html', context)


@login_required
def comment_delete(request, comment_id):
    """
    Eliminar un comentario.
    Solo el autor del comentario o admin pueden eliminar.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Verificar permisos
    if comment.user != request.user and not request.user.is_admin:
        messages.error(request, 'No tienes permiso para eliminar este comentario.')
        return HttpResponseForbidden('No tienes permiso para eliminar este comentario.')
    
    post_slug = comment.post.slug
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comentario eliminado exitosamente.')
        return redirect('post_detail', slug=post_slug)
    
    return render(request, 'blog/comment_confirm_delete.html', {
        'comment': comment
    })


def category_list(request):
    """
    Lista de todas las categorías con conteo de posts.
    """
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)
    
    popular_categories = categories.order_by('-post_count')[:4]
    
    return render(request, 'blog/category_list.html', {
        'categories': categories,
        'popular_categories': popular_categories,
    })


def tag_list(request):
    """
    Lista de todas las etiquetas con conteo de posts.
    """
    tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0).order_by('-post_count')
    
    max_count = tags.first().post_count if tags.exists() else 1
    popular_tags = tags[:10]
    
    return render(request, 'blog/tag_list.html', {
        'tags': tags,
        'popular_tags': popular_tags,
        'max_count': max_count,
    })
