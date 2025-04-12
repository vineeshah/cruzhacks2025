# services/recommendation.py
import os
import google.generativeai as genai
from run import mongo
from bson import ObjectId
from config import Config
from models.user import User
import json

# Configure the Gemini API with your key
genai.configure(api_key=Config.GEMINI_API_KEY)

class RecommendationService:
    def __init__(self):
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def analyze_food_health(self, food_name):
        try:
            prompt = f"""
            Analyze the healthiness of this food item: {food_name}
            
            Consider:
            - Nutritional content
            - Processing level
            - Ingredient quality
            - Health impact
            
            Return a health rating (1-10) and brief explanation.
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_food_analysis(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def get_menu_health(self, restaurant_id, user_id):
        """Get health analysis for a restaurant's menu"""
        try:
            # Get user preferences
            user = User.find_by_id(user_id)
            if not user:
                return {"error": "User not found"}
            
            user_preferences = {
                "health_goals": user.get('health_goals', []),
                "dietary_restrictions": user.get('dietary_restrictions', [])
            }
            
            # Get menu items
            from services.google_places_service import GooglePlacesService
            places_service = GooglePlacesService()
            menu_items = places_service.get_menu(restaurant_id)
            
            if not menu_items:
                return {"error": "No menu items found"}
            
            # Create prompt for Gemini
            prompt = f"""
            User preferences:
            - Health goals: {user_preferences['health_goals']}
            - Dietary restrictions: {user_preferences['dietary_restrictions']}
            
            Menu items to analyze:
            {[f"- {item['name']}: {item.get('description', '')}" for item in menu_items]}
            
            For each menu item, provide:
            1. Health rating (1-10)
            2. Brief explanation
            3. Key nutritional concerns
            4. Healthier alternatives
            
            Format the response as a JSON array with these fields for each item:
            - name
            - health_rating
            - explanation
            - concerns
            - alternatives
            """
            
            # Get analysis from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            try:
                analysis = json.loads(response.text)
                return {
                    "menu_items": analysis,
                    "overall_rating": sum(item['health_rating'] for item in analysis) / len(analysis) if analysis else 0
                }
            except json.JSONDecodeError:
                return {"error": "Failed to analyze menu items"}
                
        except Exception as e:
            print(f"Error analyzing menu: {str(e)}")
            return {"error": str(e)}
    
    def _parse_food_analysis(self, text):
        # Parse the AI response into structured data
        try:
            rating = int(text.split()[0])
            explanation = ' '.join(text.split()[1:])
            return {
                "rating": rating,
                "explanation": explanation
            }
        except:
            return {
                "rating": 5,
                "explanation": "Unable to analyze food health"
            }