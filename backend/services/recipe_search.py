import os
import httpx
import sys
from pathlib import Path
import time
import json
import sys
sys.path.append(str(Path(__file__).parent.parent))
import google.generativeai as genai
from models.user import User
from config import Config

class RecipeSearchService:
    def __init__(self):
        self.api_key = Config.GOOGLE_SEARCH_API_KEY
        self.engine_id = Config.SEARCH_ENGINE_ID
        # Initialize Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def get_recipe_recommendations(self, food_item, user_id):
        """Get healthier recipe alternatives using Gemini"""
        try:
            # Get user preferences
            user = User.find_by_id(user_id)
            if not user:
                return {"error": "User not found"}
            
            user_preferences = {
                "health_goals": user.get('health_goals', []),
                "dietary_restrictions": user.get('dietary_restrictions', [])
            }
            
            # Create prompt for Gemini
            prompt = f"""
            Given these user preferences:
            - Health goals: {user_preferences['health_goals']}
            - Dietary restrictions: {user_preferences['dietary_restrictions']}

            For the food item: {food_item}

            Respond with EXACTLY 3 healthier alternative dishes.
            Format your response as a simple numbered list with ONLY the names:
            1. [First Alternative]
            2. [Second Alternative]
            3. [Third Alternative]

            Do not include any explanations, descriptions, or additional information.
            Just the numbered names of the dishes.
            """
            
            # Get alternatives from Gemini
            response = self.model.generate_content(prompt)
            print("\n=== Gemini Response ===")
            print(response.text)
            
            lines = [line.strip().replace('"', '') for line in response.text.split('\n') if line.strip()]
    
            # Extract alternatives (removing the number and dot at the start of each line)
            alternatives = [line[2:].strip() for line in lines if line[0].isdigit()]
            
            # Get recipe details for each alternative
            recipe_details = []
            for alt in alternatives:
                recipe_info = self.search_recipes(alt)
                if recipe_info and alt in recipe_info:
                    recipe_data = recipe_info[alt]
                    print('helloooooooooooo', recipe_data[1])
                    recipe_details.append({
                        "recipe_name": alt,
                        "description": recipe_data[0] if len(recipe_data) > 0 else "No description available",
                        "benefits": recipe_data[1] if len(recipe_data) > 1 else "No health benefits information available",
                        "link": recipe_data[2] if len(recipe_data) > 2 else "#",
                        "food_item": food_item,
                        "user_preferences": user_preferences
                    })
            
            return {
                "alternatives": recipe_details
            }

        except Exception as e:
            print(f"Error parsing alternatives: {str(e)}")
            return {"error": str(e)}

    def google_search(self, query, **params):
        '''Performs single search query'''
        base_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key' : self.api_key,
            'cx' : self.engine_id,
            'q' : query,
            **params
        }

        with httpx.Client(timeout=60.0) as client:
            try:
                response = client.get(base_url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.ConnectTimeout:
                print("Connection timed out. This could be due to network issues or API restrictions.")
                # Return a mock response for testing purposes
                #return create_mock_response(query)
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code == 429:
                    print("Rate limit exceeded. Try again later.")
                #return create_mock_response(query)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                #return create_mock_response(query)


    def search_recipes(self, food):
        '''Returns recipe queries of inputted food'''
        recipe_queries = {}
        query_keys = []
        # Main execution
        try:
            print("Starting Google Search API test...")
            # Test with a simple query first
            query = food + ' recipe'
            print(f"Searching for: {query}")

            search_results = []
            # Limit to just one page of results for testing
            response = self.google_search(
                query, 
                num=10)

            if 'items' in response:
                search_results.extend(response.get('items', []))
                print(f"Found {len(search_results)} results")

                if search_results:
                    for entry in search_results:
                        if 'reddit' not in entry['link']:
                            print(entry)
                            # Extract title and link as strings
                            title = entry.get('title', 'No title available')
                            link = entry.get('link', '#')
                            
                            # Create a description from the title
                            description = f"A delicious {food.lower()} recipe"
                            
                            # Create a simple benefits string
                            benefits = f"Healthy and nutritious {title.lower()}"
                            
                            query_keys.append([description, benefits, link])
                else:
                    print("No results found")
                    # Add default values if no results found
                    query_keys.append([
                        f"No description available for {food}",
                        f"No health benefits information available for {food}",
                        "#"
                    ])

            else:
                print("No 'items' found in the response")
                print(f"Response: {json.dumps(response, indent=2)}")
                # Add default values if no items found
                query_keys.append([
                    f"No description available for {food}",
                    f"No health benefits information available for {food}",
                    "#"
                ])
        except Exception as e:
                print(f"Error in main execution: {str(e)}")
                # Add default values if an error occurs
                query_keys.append([
                    f"No description available for {food}",
                    f"No health benefits information available for {food}",
                    "#"
                ])

        recipe_queries[food] = query_keys[0]
        print('AHHHHHHHH', recipe_queries)
        return recipe_queries

r = RecipeSearchService()
search = r.search_recipes('pizza')
print(search)