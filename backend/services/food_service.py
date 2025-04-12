import google.generativeai as genai
from config import Config

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class FoodService:
    @staticmethod
    def analyze_food(food_name: str, ingredients: list = None) -> dict:
        """Analyze food using Gemini"""
        prompt = f"""
        Analyze this food item and provide detailed information:
        Name: {food_name}
        Ingredients: {', '.join(ingredients) if ingredients else 'Not specified'}
        
        Please provide:
        1. Health rating (1-10)
        2. Key nutritional benefits
        3. Potential health concerns
        4. Processing level (low/medium/high)
        5. Suitable for which dietary preferences
        6. Alternative healthier options
        
        Format as JSON with these keys:
        - health_rating
        - benefits
        - concerns
        - processing_level
        - suitable_for
        - alternatives
        """
        
        response = model.generate_content(prompt)
        try:
            # Parse the response into structured data
            analysis = eval(response.text)  # Note: In production, use proper JSON parsing
            return analysis
        except:
            return {
                "health_rating": 5,
                "benefits": [],
                "concerns": [],
                "processing_level": "medium",
                "suitable_for": [],
                "alternatives": []
            } 