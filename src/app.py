"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import (
    db, User, Character, Planet, Vehicle, Starship, Film,
    BlogPost, Comment, FavoriteCharacter, FavoritePlanet,
    FavoriteVehicle, FavoriteStarship, FavoriteFilm
)
from datetime import datetime

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ============================================================================
# USER ENDPOINTS
# ============================================================================


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize_with_stats()), 200


@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()

    if not body:
        raise APIException('Request body is required', status_code=400)
    if 'email' not in body:
        raise APIException('Email is required', status_code=400)
    if 'password' not in body:
        raise APIException('Password is required', status_code=400)
    if 'username' not in body:
        raise APIException('Username is required', status_code=400)

    # Check if user already exists
    if User.query.filter_by(email=body['email']).first():
        raise APIException('Email already exists', status_code=400)
    if User.query.filter_by(username=body['username']).first():
        raise APIException('Username already exists', status_code=400)

    user = User(
        email=body['email'],
        password=body['password'],  # In production, hash this!
        username=body['username'],
        first_name=body.get('first_name'),
        last_name=body.get('last_name')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201

# ============================================================================
# CHARACTER ENDPOINTS
# ============================================================================


@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Character.query.get(people_id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    return jsonify(character.serialize()), 200


@app.route('/people', methods=['POST'])
def create_character():
    body = request.get_json()

    if not body or 'name' not in body:
        raise APIException('Name is required', status_code=400)

    character = Character(
        name=body['name'],
        height=body.get('height'),
        mass=body.get('mass'),
        hair_color=body.get('hair_color'),
        skin_color=body.get('skin_color'),
        eye_color=body.get('eye_color'),
        birth_year=body.get('birth_year'),
        gender=body.get('gender'),
        homeworld=body.get('homeworld'),
        url=body.get('url')
    )

    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201

# ============================================================================
# PLANET ENDPOINTS
# ============================================================================


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()

    if not body or 'name' not in body:
        raise APIException('Name is required', status_code=400)

    planet = Planet(
        name=body['name'],
        diameter=body.get('diameter'),
        rotation_period=body.get('rotation_period'),
        orbital_period=body.get('orbital_period'),
        gravity=body.get('gravity'),
        population=body.get('population'),
        climate=body.get('climate'),
        terrain=body.get('terrain'),
        surface_water=body.get('surface_water'),
        url=body.get('url')
    )

    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize()), 201

# ============================================================================
# VEHICLE ENDPOINTS
# ============================================================================


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        raise APIException('Vehicle not found', status_code=404)
    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = request.get_json()

    if not body or 'name' not in body:
        raise APIException('Name is required', status_code=400)

    vehicle = Vehicle(
        name=body['name'],
        model=body.get('model'),
        manufacturer=body.get('manufacturer'),
        cost_in_credits=body.get('cost_in_credits'),
        length=body.get('length'),
        max_atmosphering_speed=body.get('max_atmosphering_speed'),
        crew=body.get('crew'),
        passengers=body.get('passengers'),
        cargo_capacity=body.get('cargo_capacity'),
        consumables=body.get('consumables'),
        vehicle_class=body.get('vehicle_class'),
        url=body.get('url')
    )

    db.session.add(vehicle)
    db.session.commit()

    return jsonify(vehicle.serialize()), 201

# ============================================================================
# STARSHIP ENDPOINTS
# ============================================================================


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([starship.serialize() for starship in starships]), 200


@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=404)
    return jsonify(starship.serialize()), 200


@app.route('/starships', methods=['POST'])
def create_starship():
    body = request.get_json()

    if not body or 'name' not in body:
        raise APIException('Name is required', status_code=400)

    starship = Starship(
        name=body['name'],
        model=body.get('model'),
        manufacturer=body.get('manufacturer'),
        cost_in_credits=body.get('cost_in_credits'),
        length=body.get('length'),
        max_atmosphering_speed=body.get('max_atmosphering_speed'),
        crew=body.get('crew'),
        passengers=body.get('passengers'),
        cargo_capacity=body.get('cargo_capacity'),
        consumables=body.get('consumables'),
        hyperdrive_rating=body.get('hyperdrive_rating'),
        MGLT=body.get('MGLT'),
        starship_class=body.get('starship_class'),
        url=body.get('url')
    )

    db.session.add(starship)
    db.session.commit()

    return jsonify(starship.serialize()), 201

# ============================================================================
# FILM ENDPOINTS
# ============================================================================


@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    return jsonify([film.serialize() for film in films]), 200


@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    if film is None:
        raise APIException('Film not found', status_code=404)
    return jsonify(film.serialize()), 200


@app.route('/films', methods=['POST'])
def create_film():
    body = request.get_json()

    if not body or 'title' not in body:
        raise APIException('Title is required', status_code=400)

    film = Film(
        title=body['title'],
        episode_id=body.get('episode_id'),
        opening_crawl=body.get('opening_crawl'),
        director=body.get('director'),
        producer=body.get('producer'),
        release_date=body.get('release_date'),
        url=body.get('url')
    )

    db.session.add(film)
    db.session.commit()

    return jsonify(film.serialize()), 201

# ============================================================================
# BLOG POST ENDPOINTS
# ============================================================================


@app.route('/posts', methods=['GET'])
def get_posts():
    status = request.args.get('status', 'published')
    posts = BlogPost.query.filter_by(status=status).order_by(
        BlogPost.created_at.desc()).all()
    return jsonify([post.serialize_summary() for post in posts]), 200


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    # Increment view count
    post.views += 1
    db.session.commit()

    return jsonify(post.serialize()), 200


@app.route('/posts', methods=['POST'])
def create_post():
    body = request.get_json()

    if not body:
        raise APIException('Request body is required', status_code=400)
    if 'title' not in body:
        raise APIException('Title is required', status_code=400)
    if 'content' not in body:
        raise APIException('Content is required', status_code=400)
    if 'author_id' not in body:
        raise APIException('Author ID is required', status_code=400)

    # Generate slug from title
    from slugify import slugify
    slug = slugify(body['title'])

    # Ensure unique slug
    base_slug = slug
    counter = 1
    while BlogPost.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    post = BlogPost(
        title=body['title'],
        slug=slug,
        content=body['content'],
        excerpt=body.get('excerpt'),
        status=body.get('status', 'draft'),
        author_id=body['author_id']
    )

    if post.status == 'published':
        post.published_at = datetime.utcnow()

    db.session.add(post)
    db.session.commit()

    return jsonify(post.serialize()), 201


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    body = request.get_json()

    if 'title' in body:
        post.title = body['title']
    if 'content' in body:
        post.content = body['content']
    if 'excerpt' in body:
        post.excerpt = body['excerpt']
    if 'status' in body:
        if body['status'] == 'published' and post.status != 'published':
            post.published_at = datetime.utcnow()
        post.status = body['status']

    post.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(post.serialize()), 200


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200

# ============================================================================
# COMMENT ENDPOINTS
# ============================================================================


@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    comments = Comment.query.filter_by(post_id=post_id).order_by(
        Comment.created_at.desc()).all()
    return jsonify([comment.serialize() for comment in comments]), 200


@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    body = request.get_json()

    if not body or 'content' not in body:
        raise APIException('Content is required', status_code=400)
    if 'author_id' not in body:
        raise APIException('Author ID is required', status_code=400)

    comment = Comment(
        content=body['content'],
        author_id=body['author_id'],
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.serialize()), 201

# ============================================================================
# FAVORITES ENDPOINTS
# ============================================================================


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    return jsonify({
        "characters": [fav.serialize() for fav in user.favorite_characters.all()],
        "planets": [fav.serialize() for fav in user.favorite_planets.all()],
        "vehicles": [fav.serialize() for fav in user.favorite_vehicles.all()],
        "starships": [fav.serialize() for fav in user.favorite_starships.all()],
        "films": [fav.serialize() for fav in user.favorite_films.all()]
    }), 200


@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_character(user_id, people_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    character = Character.query.get(people_id)
    if character is None:
        raise APIException('Character not found', status_code=404)

    # Check if already exists
    existing = FavoriteCharacter.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if existing:
        raise APIException('Character already in favorites', status_code=400)

    favorite = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_character(user_id, people_id):
    favorite = FavoriteCharacter.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)

    existing = FavoritePlanet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if existing:
        raise APIException('Planet already in favorites', status_code=400)

    favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    favorite = FavoritePlanet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        raise APIException('Vehicle not found', status_code=404)

    existing = FavoriteVehicle.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()
    if existing:
        raise APIException('Vehicle already in favorites', status_code=400)

    favorite = FavoriteVehicle(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def remove_favorite_vehicle(user_id, vehicle_id):
    favorite = FavoriteVehicle.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


@app.route('/users/<int:user_id>/favorites/starships/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException('Starship not found', status_code=404)

    existing = FavoriteStarship.query.filter_by(
        user_id=user_id, starship_id=starship_id).first()
    if existing:
        raise APIException('Starship already in favorites', status_code=400)

    favorite = FavoriteStarship(user_id=user_id, starship_id=starship_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/users/<int:user_id>/favorites/starships/<int:starship_id>', methods=['DELETE'])
def remove_favorite_starship(user_id, starship_id):
    favorite = FavoriteStarship.query.filter_by(
        user_id=user_id, starship_id=starship_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


@app.route('/users/<int:user_id>/favorites/films/<int:film_id>', methods=['POST'])
def add_favorite_film(user_id, film_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    film = Film.query.get(film_id)
    if film is None:
        raise APIException('Film not found', status_code=404)

    existing = FavoriteFilm.query.filter_by(
        user_id=user_id, film_id=film_id).first()
    if existing:
        raise APIException('Film already in favorites', status_code=400)

    favorite = FavoriteFilm(user_id=user_id, film_id=film_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/users/<int:user_id>/favorites/films/<int:film_id>', methods=['DELETE'])
def remove_favorite_film(user_id, film_id):
    favorite = FavoriteFilm.query.filter_by(
        user_id=user_id, film_id=film_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
