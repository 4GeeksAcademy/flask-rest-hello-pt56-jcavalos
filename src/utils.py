"""
Funciones de utilidad para el proyecto Star Wars Blog
"""
from datetime import datetime
from sqlalchemy import func
from slugify import slugify as make_slug

class DatabaseHelper:
    """
    Clase con métodos auxiliares para operaciones de base de datos
    """
    
    @staticmethod
    def get_or_create(session, model, **kwargs):
        """
        Obtiene una instancia o la crea si no existe
        
        Args:
            session: Sesión de SQLAlchemy
            model: Clase del modelo
            **kwargs: Campos para buscar/crear
        
        Returns:
            tuple: (instance, created)
        """
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            instance = model(**kwargs)
            session.add(instance)
            return instance, True
    
    @staticmethod
    def bulk_create(session, model, data_list):
        """
        Crea múltiples registros en bulk
        
        Args:
            session: Sesión de SQLAlchemy
            model: Clase del modelo
            data_list: Lista de diccionarios con datos
        
        Returns:
            list: Lista de instancias creadas
        """
        instances = [model(**data) for data in data_list]
        session.bulk_save_objects(instances)
        return instances
    
    @staticmethod
    def paginate(query, page=1, per_page=10):
        """
        Pagina una consulta
        
        Args:
            query: Query de SQLAlchemy
            page: Número de página
            per_page: Elementos por página
        
        Returns:
            dict: Datos de paginación
        """
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }

class SlugHelper:
    """
    Ayudantes para generar y manejar slugs
    """
    
    @staticmethod
    def generate_slug(text, max_length=50):
        """
        Genera un slug a partir de texto
        
        Args:
            text: Texto a convertir
            max_length: Longitud máxima del slug
        
        Returns:
            str: Slug generado
        """
        slug = make_slug(text, max_length=max_length)
        return slug
    
    @staticmethod
    def ensure_unique_slug(session, model, slug, slug_field='slug'):
        """
        Asegura que el slug sea único añadiendo un número si es necesario
        
        Args:
            session: Sesión de SQLAlchemy
            model: Clase del modelo
            slug: Slug base
            slug_field: Nombre del campo slug
        
        Returns:
            str: Slug único
        """
        original_slug = slug
        counter = 1
        
        while session.query(model).filter(
            getattr(model, slug_field) == slug
        ).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug

class StatisticsHelper:
    """
    Funciones para calcular estadísticas
    """
    
    @staticmethod
    def get_popular_posts(session, blog_post_model, limit=10):
        """
        Obtiene los posts más populares por vistas
        
        Args:
            session: Sesión de SQLAlchemy
            blog_post_model: Modelo de BlogPost
            limit: Número de posts a retornar
        
        Returns:
            list: Lista de posts populares
        """
        return session.query(blog_post_model)\
            .filter(blog_post_model.status == 'published')\
            .order_by(blog_post_model.views.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_most_favorited_characters(session, favorite_model, character_model, limit=10):
        """
        Obtiene los personajes más guardados como favoritos
        
        Args:
            session: Sesión de SQLAlchemy
            favorite_model: Modelo de FavoriteCharacter
            character_model: Modelo de Character
            limit: Número de personajes a retornar
        
        Returns:
            list: Lista de (character, count)
        """
        return session.query(
            character_model,
            func.count(favorite_model.id).label('favorite_count')
        )\
        .join(favorite_model)\
        .group_by(character_model.id)\
        .order_by(func.count(favorite_model.id).desc())\
        .limit(limit)\
        .all()
    
    @staticmethod
    def get_user_statistics(session, user):
        """
        Obtiene estadísticas completas de un usuario
        
        Args:
            session: Sesión de SQLAlchemy
            user: Instancia de User
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            'total_posts': user.posts.count(),
            'total_comments': user.comments.count(),
            'favorite_characters': user.favorite_characters.count(),
            'favorite_planets': user.favorite_planets.count(),
            'favorite_vehicles': user.favorite_vehicles.count(),
            'favorite_starships': user.favorite_starships.count(),
            'favorite_films': user.favorite_films.count(),
            'member_since': user.subscription_date,
            'days_active': (datetime.utcnow() - user.subscription_date).days
        }

class ValidationHelper:
    """
    Funciones de validación
    """
    
    @staticmethod
    def validate_email(email):
        """
        Valida formato de email
        
        Args:
            email: Email a validar
        
        Returns:
            bool: True si es válido
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password):
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
        
        Returns:
            tuple: (is_valid, messages)
        """
        messages = []
        
        if len(password) < 8:
            messages.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            messages.append("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            messages.append("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            messages.append("Password must contain at least one number")
        
        return len(messages) == 0, messages
    
    @staticmethod
    def sanitize_html(text):
        """
        Limpia HTML peligroso de texto
        
        Args:
            text: Texto a limpiar
        
        Returns:
            str: Texto limpio
        """
        # En producción, usar bleach o html.escape
        import html
        return html.escape(text)

class SearchHelper:
    """
    Funciones de búsqueda
    """
    
    @staticmethod
    def search_characters(session, character_model, query_string):
        """
        Busca personajes por nombre
        
        Args:
            session: Sesión de SQLAlchemy
            character_model: Modelo de Character
            query_string: Texto a buscar
        
        Returns:
            list: Lista de personajes encontrados
        """
        return session.query(character_model)\
            .filter(character_model.name.ilike(f"%{query_string}%"))\
            .all()
    
    @staticmethod
    def search_posts(session, blog_post_model, query_string):
        """
        Busca posts por título o contenido
        
        Args:
            session: Sesión de SQLAlchemy
            blog_post_model: Modelo de BlogPost
            query_string: Texto a buscar
        
        Returns:
            list: Lista de posts encontrados
        """
        return session.query(blog_post_model)\
            .filter(
                (blog_post_model.title.ilike(f"%{query_string}%")) |
                (blog_post_model.content.ilike(f"%{query_string}%"))
            )\
            .filter(blog_post_model.status == 'published')\
            .all()

# Funciones de formateo
def format_datetime(dt, format_string='%Y-%m-%d %H:%M:%S'):
    """Formatea un datetime"""
    if dt:
        return dt.strftime(format_string)
    return None

def calculate_reading_time(content):
    """
    Calcula el tiempo estimado de lectura
    
    Args:
        content: Contenido del post
    
    Returns:
        int: Minutos de lectura estimados
    """
    words = len(content.split())
    # Promedio de 200 palabras por minuto
    minutes = max(1, round(words / 200))
    return minutes

def truncate_text(text, length=100, suffix='...'):
    """
    Trunca texto a cierta longitud
    
    Args:
        text: Texto a truncar
        length: Longitud máxima
        suffix: Sufijo a añadir
    
    Returns:
        str: Texto truncado
    """
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix