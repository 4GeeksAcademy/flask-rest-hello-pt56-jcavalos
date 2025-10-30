from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

db = SQLAlchemy()

# Enums


class PostStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

# Modelos principales


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), default=True, nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    posts = relationship('BlogPost', back_populates='author', lazy='dynamic')
    comments = relationship('Comment', back_populates='author', lazy='dynamic')
    favorite_characters = relationship(
        'FavoriteCharacter', back_populates='user', lazy='dynamic')
    favorite_planets = relationship(
        'FavoritePlanet', back_populates='user', lazy='dynamic')
    favorite_vehicles = relationship(
        'FavoriteVehicle', back_populates='user', lazy='dynamic')
    favorite_starships = relationship(
        'FavoriteStarship', back_populates='user', lazy='dynamic')
    favorite_films = relationship(
        'FavoriteFilm', back_populates='user', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None
        }

    def serialize_with_stats(self):
        return {
            **self.serialize(),
            "total_posts": self.posts.count(),
            "total_comments": self.comments.count(),
            "total_favorites": (
                self.favorite_characters.count() +
                self.favorite_planets.count() +
                self.favorite_vehicles.count() +
                self.favorite_starships.count() +
                self.favorite_films.count()
            )
        }


class Character(db.Model):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    mass: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    favorites = relationship(
        'FavoriteCharacter', back_populates='character', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "url": self.url
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(50), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(50), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(50), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    favorites = relationship(
        'FavoritePlanet', back_populates='planet', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "url": self.url
        }


class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=True)
    cost_in_credits: Mapped[str] = mapped_column(String(50), nullable=True)
    length: Mapped[str] = mapped_column(String(50), nullable=True)
    max_atmosphering_speed: Mapped[str] = mapped_column(
        String(50), nullable=True)
    crew: Mapped[str] = mapped_column(String(50), nullable=True)
    passengers: Mapped[str] = mapped_column(String(50), nullable=True)
    cargo_capacity: Mapped[str] = mapped_column(String(50), nullable=True)
    consumables: Mapped[str] = mapped_column(String(50), nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    favorites = relationship(
        'FavoriteVehicle', back_populates='vehicle', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class,
            "url": self.url
        }


class Starship(db.Model):
    __tablename__ = 'starship'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=True)
    cost_in_credits: Mapped[str] = mapped_column(String(50), nullable=True)
    length: Mapped[str] = mapped_column(String(50), nullable=True)
    max_atmosphering_speed: Mapped[str] = mapped_column(
        String(50), nullable=True)
    crew: Mapped[str] = mapped_column(String(50), nullable=True)
    passengers: Mapped[str] = mapped_column(String(50), nullable=True)
    cargo_capacity: Mapped[str] = mapped_column(String(50), nullable=True)
    consumables: Mapped[str] = mapped_column(String(50), nullable=True)
    hyperdrive_rating: Mapped[str] = mapped_column(String(50), nullable=True)
    MGLT: Mapped[str] = mapped_column(String(50), nullable=True)
    starship_class: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    favorites = relationship(
        'FavoriteStarship', back_populates='starship', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class,
            "url": self.url
        }


class Film(db.Model):
    __tablename__ = 'film'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    episode_id: Mapped[int] = mapped_column(Integer, nullable=True)
    opening_crawl: Mapped[str] = mapped_column(Text, nullable=True)
    director: Mapped[str] = mapped_column(String(100), nullable=True)
    producer: Mapped[str] = mapped_column(String(100), nullable=True)
    release_date: Mapped[str] = mapped_column(String(50), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    favorites = relationship(
        'FavoriteFilm', back_populates='film', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date,
            "url": self.url
        }


class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default='draft', nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Foreign Keys
    author_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)

    # Relaciones
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post',
                            lazy='dynamic', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "excerpt": self.excerpt,
            "status": self.status,
            "views": self.views,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "author_id": self.author_id,
            "author": self.author.serialize() if self.author else None
        }

    def serialize_summary(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "excerpt": self.excerpt,
            "status": self.status,
            "views": self.views,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "author": {
                "id": self.author.id,
                "username": self.author.username
            } if self.author else None
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Foreign Keys
    author_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('blog_post.id'), nullable=False)

    # Relaciones
    author = relationship('User', back_populates='comments')
    post = relationship('BlogPost', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "author": {
                "id": self.author.id,
                "username": self.author.username
            } if self.author else None
        }

# Tablas de Favoritos


class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship('User', back_populates='favorite_characters')
    character = relationship('Character', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "character": self.character.serialize() if self.character else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship('User', back_populates='favorite_planets')
    planet = relationship('Planet', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize() if self.planet else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite_vehicle'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey('vehicle.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship('User', back_populates='favorite_vehicles')
    vehicle = relationship('Vehicle', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "vehicle": self.vehicle.serialize() if self.vehicle else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FavoriteStarship(db.Model):
    __tablename__ = 'favorite_starship'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    starship_id: Mapped[int] = mapped_column(
        ForeignKey('starship.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship('User', back_populates='favorite_starships')
    starship = relationship('Starship', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
            "starship": self.starship.serialize() if self.starship else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FavoriteFilm(db.Model):
    __tablename__ = 'favorite_film'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    film_id: Mapped[int] = mapped_column(ForeignKey('film.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship('User', back_populates='favorite_films')
    film = relationship('Film', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "film_id": self.film_id,
            "film": self.film.serialize() if self.film else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
