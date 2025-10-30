import os
from flask_admin import Admin
from models import (
    db, User, Character, Planet, Vehicle, Starship, Film,
    BlogPost, Comment, FavoriteCharacter, FavoritePlanet,
    FavoriteVehicle, FavoriteStarship, FavoriteFilm
)
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Star Wars Blog Admin', template_mode='bootstrap3')

    # Add all models to admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(ModelView(Film, db.session))
    admin.add_view(ModelView(BlogPost, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(FavoriteCharacter, db.session))
    admin.add_view(ModelView(FavoritePlanet, db.session))
    admin.add_view(ModelView(FavoriteVehicle, db.session))
    admin.add_view(ModelView(FavoriteStarship, db.session))
    admin.add_view(ModelView(FavoriteFilm, db.session))