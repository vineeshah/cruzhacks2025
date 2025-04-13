import os
import httpx
import sys
from pathlib import Path
import time
import json
import sys
import google.generativeai as genai
from config import Config
from models.user import User

sys.path.append(str(Path(__file__).parent.parent))

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
            User preferences:
            - Health goals: {user_preferences['health_goals']}
            - Dietary restrictions: {user_preferences['dietary_restrictions']}
            
            Food Item: {food_item}
            
            Suggest 3-5 healthier alternatives to this food item that align with the user's preferences.
            For each alternative, provide:
            1. Food item name
            2. Recipe name
            3. Brief description
            4. Key health benefits
            5. Link to a recipe website
            
            Important requirements:
            - Only use recipes from these specific websites:
              * Allrecipes.com
              * FoodNetwork.com
              * EatingWell.com
              * MinimalistBaker.com
              * CookieAndKate.com
              * LoveAndLemons.com
              * OhSheGlows.com
              * BudgetBytes.com
              * Skinnytaste.com
              * PinchOfYum.com
            
            - The link must be a direct URL to a specific recipe on one of these websites
            - The recipe must actually exist on the website
            - Do not make up or generate fake URLs
            - All links must start with https://
            
            Format the response as a JSON array with these fields for each alternative:
            - food_item
            - recipe_name
            - description
            - benefits
            - link
            
            Return ONLY the JSON array, nothing else.
            """
            
            # Get alternatives from Gemini
            response = self.model.generate_content(prompt)
            print("\n=== Gemini Response ===")
            print(response.text)
            
            # Clean the response text
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse the response
            try:
                alternatives = json.loads(response_text)
                print("\n=== Parsed Alternatives ===")
                print(json.dumps(alternatives, indent=2))
                
                # Validate and clean links
                valid_domains = [
                    'allrecipes.com',
                    'foodnetwork.com',
                    'eatingwell.com',
                    'minimalistbaker.com',
                    'cookieandkate.com',
                    'loveandlemons.com',
                    'ohsheglows.com',
                    'budgetbytes.com',
                    'skinnytaste.com',
                    'pinchofyum.com'
                ]
                
                for alt in alternatives:
                    if 'link' in alt:
                        # Ensure link starts with https://
                        if not alt['link'].startswith('https://'):
                            alt['link'] = 'https://' + alt['link']
                        
                        # Remove any trailing characters that might break the URL
                        alt['link'] = alt['link'].split(' ')[0].split('\n')[0].strip()
                        
                        # Validate domain
                        from urllib.parse import urlparse
                        domain = urlparse(alt['link']).netloc.lower()
                        if not any(valid_domain in domain for valid_domain in valid_domains):
                            print(f"\n=== Invalid Domain Warning ===")
                            print(f"Invalid domain in link: {alt['link']}")
                            alt['link'] = '#'  # Set to invalid link if domain is not in our list
                
                return {
                    "alternatives": alternatives,
                    "user_preferences": user_preferences
                }
            except json.JSONDecodeError as e:
                print(f"\n=== JSON Parse Error ===")
                print(f"Error: {str(e)}")
                print(f"Response text: {response_text}")
                return {"error": "Failed to parse recipe alternatives"}
                
        except Exception as e:
            print(f"\n=== Error in get_recipe_recommendations ===")
            print(f"Error: {str(e)}")
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


    def search_recipes(self, preferences):
        '''Returns all recipes based on user's preferences'''
        recipe_queries = {}
        for pref in preferences:
            sub_queries = []
            # Main execution
            try:
                print("Starting Google Search API test...")
                # Test with a simple query first
                query = pref + ' recipe'
                print(f"Searching for: {query}")

                search_results = []
                # Limit to just one page of results for testing
                response = self.google_search(
                    query, 
                    num=10)  # Limit to 10 results for testing

                if 'items' in response:
                    search_results.extend(response.get('items', []))
                    print(f"Found {len(search_results)} results")

                    if search_results:
                        for entry in search_results:
                            if 'reddit' not in entry['link']:
                                entry_info = {}
                                entry_info['title'] = entry['title']
                                entry_info['link'] = entry['link']
                                sub_queries.append(entry_info)
                    else:
                        print("No results found")

                else:
                   print("No 'items' found in the response")
                   print(f"Response: {json.dumps(response, indent=2)}")
            except Exception as e:
                   print(f"Error in main execution: {str(e)}")

            recipe_queries[pref] = sub_queries
        return recipe_queries
