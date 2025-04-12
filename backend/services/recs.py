# services/recommendation.py
import os
import google.generativeai as genai
from run import mongo
from bson import ObjectId
from config import Config
from models.user import User
from models.food import Food
from models.recipe import Recipe

# Configure the Gemini API with your key
genai.configure(api_key=Config.GEMINI_API_KEY)

class RecommendationService:
    def __init__(self):
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def get_healthier_food_alternatives(self, food_id, user_id=None):
        """Generate healthier alternatives for a food item using Gemini AI"""
        # Get the original food item
        food = mongo.db.food_items.find_one({"_id": ObjectId(food_id)})
        if not food:
            return {"error": "Food not found"}, 404
        
        # Get user health goals if available
        user_goals = None
        if user_id:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user and 'health_goals' in user:
                user_goals = user['health_goals']
        
        # Create prompt for Gemini
        prompt = self._create_food_alternative_prompt(food, user_goals)
        
        # Generate response from Gemini
        response = self.model.generate_content(prompt)
        
        # Parse and format the response
        alternatives = self._parse_food_alternatives(response.text)
        
        return alternatives
    
    def get_recipe_recommendations(self, recipe_id, user_id=None):
        """Generate healthier recipe alternatives using Gemini AI"""
        # Get the original recipe
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            return {"error": "Recipe not found"}, 404
        
        # Get user health goals if available
        user_goals = None
        if user_id:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user and 'health_goals' in user:
                user_goals = user['health_goals']
        
        # Create prompt for Gemini
        prompt = self._create_recipe_alternative_prompt(recipe, user_goals)
        
        # Generate response from Gemini
        response = self.model.generate_content(prompt)
        
        # Parse and format the response
        alternatives = self._parse_recipe_alternatives(response.text)
        
        return alternatives
    
    def get_restaurant_recommendations(self, restaurant_id, user_id):
        try:
            # Get restaurant data from database
            from models.restaurant import Restaurant
            restaurant = Restaurant.find_by_id(restaurant_id)
            user = User.find_by_id(user_id)
            
            if not restaurant or not user:
                return {"error": "Restaurant or user not found"}
            
            prompt = f"""
            User preferences:
            - Health goals: {user.get('health_goals', [])}
            - Dietary restrictions: {user.get('dietary_restrictions', [])}
            - Budget preference: {user.get('budget_preference', 'medium')}
            
            Current restaurant: {restaurant['name']}
            
            Suggest 3-5 healthier restaurant alternatives that:
            - Match user preferences
            - Are within budget
            - Have better health ratings
            - Are nearby
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_restaurant_alternatives(response.text)
        except Exception as e:
            return {"error": str(e)}

    def get_healthier_options(self, restaurant_id, user_id):
        try:
            # Get restaurant data from database
            from models.restaurant import Restaurant
            restaurant = Restaurant.find_by_id(restaurant_id)
            user = User.find_by_id(user_id)
            
            if not restaurant or not user:
                return {"error": "Restaurant or user not found"}
            
            prompt = f"""
            User preferences:
            - Health goals: {user.get('health_goals', [])}
            - Dietary restrictions: {user.get('dietary_restrictions', [])}
            
            Restaurant menu items: {restaurant.get('menu_items', [])}
            
            For each menu item, suggest a healthier alternative that:
            - Uses better ingredients
            - Has better nutritional value
            - Matches user preferences
            - Is practical to make
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_menu_alternatives(response.text)
        except Exception as e:
            return {"error": str(e)}

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
    
    def _create_food_alternative_prompt(self, food, user_goals=None):
        """Create a prompt for Gemini to generate healthier food alternatives"""
        prompt = f"""
        I need healthier alternatives to the following food item:
        
        Food: {food['name']}
        Category: {food['category']}
        Processed Level: {food['processed_level']}/10
        Nutritional Info: {food['nutritional_info']}
        
        """
        
        if user_goals:
            prompt += f"""
            The user has the following health goals:
            - Goal type: {user_goals.get('goal_type', 'Not specified')}
            - Dietary restrictions: {', '.join(user_goals.get('dietary_restrictions', ['None']))}
            - Health conditions: {', '.join(user_goals.get('health_conditions', ['None']))}
            - Target calories: {user_goals.get('target_calories', 'Not specified')}
            """
        
        prompt += """
        Please provide 3-5 healthier alternatives with the following information for each:
        1. Name of the alternative food
        2. Why it's healthier
        3. Nutritional comparison
        4. How to substitute it in common recipes
        
        Format your response as a structured list with clear sections for each alternative.
        """
        
        return prompt
    
    def _create_recipe_alternative_prompt(self, recipe, user_goals=None):
        """Create a prompt for Gemini to generate healthier recipe alternatives"""
        # Create ingredients list
        ingredients_list = []
        for ingredient in recipe.get('ingredients', []):
            ingredients_list.append(f"- {ingredient.get('quantity', '')} {ingredient.get('unit', '')} {ingredient.get('name', '')}")
        
        ingredients_text = "\n".join(ingredients_list)
        
        prompt = f"""
        I need a healthier version of the following recipe:
        
        Recipe: {recipe['name']}
        Description: {recipe.get('description', 'No description provided')}
        
        Ingredients:
        {ingredients_text}
        
        Nutritional Info (per serving):
        - Calories: {recipe.get('nutritional_info', {}).get('calories', 'Not specified')}
        - Protein: {recipe.get('nutritional_info', {}).get('protein', 'Not specified')}
        - Carbs: {recipe.get('nutritional_info', {}).get('carbs', 'Not specified')}
        - Fat: {recipe.get('nutritional_info', {}).get('fat', 'Not specified')}
        """
        
        if user_goals:
            prompt += f"""
            The user has the following health goals:
            - Goal type: {user_goals.get('goal_type', 'Not specified')}
            - Dietary restrictions: {', '.join(user_goals.get('dietary_restrictions', ['None']))}
            - Health conditions: {', '.join(user_goals.get('health_conditions', ['None']))}
            - Target calories: {user_goals.get('target_calories', 'Not specified')}
            """
        
        prompt += """
        Please provide a healthier version of this recipe with:
        1. Modified ingredients list (with quantities)
        2. Updated cooking instructions if needed
        3. Explanation of why your changes make it healthier
        4. Estimated nutritional information for the new version
        
        Format your response as a structured recipe with clear sections.
        """
        
        return prompt
    
    def _parse_food_alternatives(self, response_text):
        """Parse and format Gemini's response about food alternatives"""
        # In a production environment, you would implement more robust parsing
        # This is a simple implementation to get you started
        alternatives = []
        
        # Split the response into sections based on numbers at the beginning of lines
        import re
        sections = re.split(r'^\d+\.', response_text, flags=re.MULTILINE)
        
        # Remove the first empty section if it exists
        if sections and not sections[0].strip():
            sections = sections[1:]
        
        # Process each section
        for i, section in enumerate(sections):
            if not section.strip():
                continue
                
            # Try to extract the name from the first line
            lines = section.strip().split('\n')
            name = lines[0].strip() if lines else f"Alternative {i+1}"
            
            # Create a structured alternative
            alternative = {
                "name": name,
                "description": section.strip(),
                "position": i + 1
            }
            
            alternatives.append(alternative)
        
        return alternatives
    
    def _parse_recipe_alternatives(self, response_text):
        """Parse and format Gemini's response about recipe alternatives"""
        # For simplicity, we'll return the full text for now
        # In a production app, you'd want to parse this into structured data
        return {
            "healthier_recipe": {
                "description": response_text.strip()
            }
        }
    
    def _parse_restaurant_alternatives(self, text):
        # Parse the AI response into structured data
        alternatives = []
        lines = text.split('\n')
        for line in lines:
            if line.strip():
                alternatives.append({
                    "name": line.split(':')[0].strip(),
                    "reason": line.split(':')[1].strip() if ':' in line else ""
                })
        return alternatives

    def _parse_menu_alternatives(self, text):
        # Parse the AI response into structured data
        alternatives = []
        lines = text.split('\n')
        current_item = None
        for line in lines:
            if line.strip():
                if ':' in line:
                    current_item = line.split(':')[0].strip()
                    alternatives.append({
                        "original": current_item,
                        "alternative": line.split(':')[1].strip()
                    })
        return alternatives

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