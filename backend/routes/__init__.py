from .auth import auth_bp
from .user import user_bp
from .restaurants import restaurants_bp
from .food import food_bp
from .recipes import recipe_bp

__all__ = ['auth_bp', 'user_bp', 'restaurant_bp', 'food_bp', 'recipe_bp']