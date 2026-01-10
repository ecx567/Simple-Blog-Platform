"""
Tests para el sistema de blog.

Tests de:
- Modelos (Category, Tag, Post, Comment)
- Vistas CRUD de posts
- Permisos y autorización
- Comentarios
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment

User = get_user_model()


class CategoryModelTestCase(TestCase):
    """Tests para el modelo Category."""
    
    def setUp(self):
        """Configuración inicial."""
        self.category = Category.objects.create(
            name='Tecnología',
            description='Artículos sobre tecnología'
        )
        
    def test_category_creation(self):
        """Test que una categoría se crea correctamente."""
        self.assertEqual(self.category.name, 'Tecnología')
        self.assertTrue(self.category.slug)
        
    def test_category_slug_auto_generation(self):
        """Test que el slug se genera automáticamente."""
        self.assertEqual(self.category.slug, 'tecnologia')


class PostModelTestCase(TestCase):
    """Tests para el modelo Post."""
    
    def setUp(self):
        """Configuración inicial."""
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='AuthorPass123!',
            role='author',
            is_active=True
        )
        
        self.category = Category.objects.create(name='Tecnología')
        
        self.post = Post.objects.create(
            title='Mi Primer Post',
            slug='mi-primer-post',
            content='Este es el contenido de mi primer post. ' * 10,
            excerpt='Este es un extracto del post',
            author=self.author,
            category=self.category,
            status='published'
        )
        
    def test_post_creation(self):
        """Test que un post se crea correctamente."""
        self.assertEqual(self.post.title, 'Mi Primer Post')
        self.assertEqual(self.post.author, self.author)
        self.assertEqual(self.post.status, 'published')
        
    def test_post_reading_time_calculation(self):
        """Test que el tiempo de lectura se calcula correctamente."""
        # El post tiene aproximadamente 10 palabras * 10 = 100 palabras
        # 100 palabras / 200 palabras por minuto = 0.5 minutos = 1 minuto (mínimo)
        self.assertGreaterEqual(self.post.reading_time, 1)
        
    def test_published_posts_manager(self):
        """Test que el manager 'published' solo devuelve posts publicados."""
        # Crear un borrador
        draft_post = Post.objects.create(
            title='Post Borrador',
            slug='post-borrador',
            content='Contenido del borrador',
            author=self.author,
            category=self.category,
            status='draft'
        )
        
        # Solo debe haber 1 post publicado
        self.assertEqual(Post.published.count(), 1)
        self.assertEqual(Post.objects.count(), 2)


class PostViewsTestCase(TestCase):
    """Tests para las vistas de posts."""
    
    def setUp(self):
        """Configuración inicial."""
        self.client = Client()
        
        # Crear autores
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='AuthorPass123!',
            role='author',
            is_active=True
        )
        
        self.reader = User.objects.create_user(
            username='reader',
            email='reader@example.com',
            password='ReaderPass123!',
            role='reader',
            is_active=True
        )
        
        # Crear categoría y post
        self.category = Category.objects.create(name='Tecnología')
        
        self.post = Post.objects.create(
            title='Mi Primer Post',
            slug='mi-primer-post',
            content='Contenido del post',
            author=self.author,
            category=self.category,
            status='published'
        )
        
    def test_post_list_view(self):
        """Test que la lista de posts carga correctamente."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Primer Post')
        
    def test_post_detail_view(self):
        """Test que el detalle de un post carga correctamente."""
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Primer Post')
        
    def test_post_create_requires_author_role(self):
        """Test que solo autores pueden crear posts."""
        # Intento sin autenticación
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
        
        # Intento con lector (no autor)
        self.client.login(email='reader@example.com', password='ReaderPass123!')
        response = self.client.get(reverse('post_create'))
        self.assertNotEqual(response.status_code, 200)
        
        # Intento con autor
        self.client.logout()
        self.client.login(email='author@example.com', password='AuthorPass123!')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)


class CommentModelTestCase(TestCase):
    """Tests para el modelo Comment."""
    
    def setUp(self):
        """Configuración inicial."""
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='UserPass123!',
            is_active=True
        )
        
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='AuthorPass123!',
            role='author',
            is_active=True
        )
        
        self.category = Category.objects.create(name='Tecnología')
        
        self.post = Post.objects.create(
            title='Post con Comentarios',
            slug='post-con-comentarios',
            content='Contenido del post',
            author=self.author,
            category=self.category,
            status='published'
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Este es un comentario de prueba',
            is_approved=True
        )
        
    def test_comment_creation(self):
        """Test que un comentario se crea correctamente."""
        self.assertEqual(self.comment.content, 'Este es un comentario de prueba')
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.user, self.user)
        
    def test_comment_with_parent(self):
        """Test que las respuestas a comentarios funcionan correctamente."""
        reply = Comment.objects.create(
            post=self.post,
            user=self.author,
            content='Esta es una respuesta al comentario',
            parent=self.comment,
            is_approved=True
        )
        
        self.assertEqual(reply.parent, self.comment)
        self.assertIn(reply, self.comment.replies.all())
