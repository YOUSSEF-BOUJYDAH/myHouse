from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Initialisation des extensions (sans les lier à une application Flask pour l'instant)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    # Créer l'application Flask
    app = Flask(__name__)

    # Configuration de l'application
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialisation des extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importer et enregistrer les Blueprints
    from app.routes.auth_routes import auth_routes
    from app.routes.user_routes import user_routes
    from app.routes.property_routes import property_routes

    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(property_routes, url_prefix='/api/properties')

    return app