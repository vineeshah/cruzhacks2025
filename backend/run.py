from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from config import Config
from db import mongo

def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Configure app
    app.config["MONGO_URI"] = Config.MONGO_URI
    app.config["GEMINI_API_KEY"] = Config.GEMINI_API_KEY
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    # Initialize extensions
    mongo.init_app(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.food import food_bp
    from routes.recipes import recipe_bp
    from routes.restaurants import restaurant_bp
    from routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(food_bp, url_prefix='/api/food')
    app.register_blueprint(recipe_bp, url_prefix='/api/recipes')
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)