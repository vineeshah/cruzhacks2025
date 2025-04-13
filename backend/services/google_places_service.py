import os
from googlemaps import Client
from config import Config
from models.user import User
import googlemaps
import google.generativeai as genai

class GooglePlacesService:
    def __init__(self):
        print("\n=== Initializing Google Places Service ===")
        try:
            self.api_key = Config.GOOGLE_PLACES_API_KEY
            print(f"API Key: {self.api_key[:5]}...{self.api_key[-5:] if self.api_key else 'None'}")
            
            if not self.api_key:
                raise ValueError("Google Places API key not found in configuration")
                
            # Test the API key with a simple request
            self.client = Client(key=self.api_key)
            test_result = self.client.geocode('New York, NY')
            print(f"API Key test successful: {bool(test_result)}")
            
            # Initialize Gemini
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            
            print("Google Places client initialized successfully")
            print("=== End of Initialization ===\n")
        except Exception as e:
            print(f"\nError initializing Google Places service: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise

    def calculate_health_score_with_gemini(self, place, user_preferences):
        """Calculate health score using Gemini AI"""
        try:
            # Prepare the prompt for Gemini
            prompt = f"""
            Analyze this restaurant's healthiness based on the following information:
            
            Restaurant Name: {place.get('name', '')}
            Types: {', '.join(place.get('types', []))}
            User Health Goals: {', '.join(user_preferences.get('health_goals', []))}
            User Dietary Restrictions: {', '.join(user_preferences.get('dietary_restrictions', []))}
            
            Please provide:
            1. A health score from 0-100
            2. A brief explanation of the score
            3. Key factors that influenced the score
            
            Format your response as:
            Score: [number]
            Explanation: [text]
            Factors: [bullet points]
            """
            
            # Get Gemini's response
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Parse the response to extract the score
            score = 50  # Default score if parsing fails
            try:
                score_line = next(line for line in response_text.split('\n') if line.startswith('Score:'))
                score = float(score_line.split(':')[1].strip())
                score = max(0, min(100, score))  # Ensure score is between 0 and 100
            except:
                print("Failed to parse score from Gemini response")
            
            return {
                'score': round(score, 1),
                'explanation': response_text
            }
            
        except Exception as e:
            print(f"Error calculating health score with Gemini: {str(e)}")
            return {
                'score': 50,
                'explanation': "Unable to calculate health score"
            }

    def get_menu(self, place_id):
        """Get menu items for a place"""
        try:
            # Get place details
            place_details = self.client.place(place_id, fields=['types', 'name', 'menu_items'])
            if not place_details:
                return []
            
            # Check if it's a food establishment
            if 'types' not in place_details or not any(t in place_details['types'] for t in ['restaurant', 'food', 'cafe', 'bar']):
                return []
            
            # Get menu items
            menu_items = place_details.get('menu_items', [])
            
            # Format menu items
            formatted_items = []
            for item in menu_items:
                formatted_items.append({
                    'name': item.get('name', ''),
                    'description': item.get('description', ''),
                    'price': item.get('price', ''),
                    'category': item.get('category', '')
                })
            
            return formatted_items
        except Exception as e:
            print(f"Error getting menu: {str(e)}")
            return []

    def analyze_menu_with_gemini(self, website_url, user_preferences):
        """Analyze restaurant menu using Gemini AI"""
        try:
            print(f"\nAnalyzing menu for website: {website_url}")
            if not website_url:
                print("No website URL provided")
                return {
                    'score': 50,
                    'keywords': ["No menu available"]
                }

            # Prepare the prompt for Gemini
            prompt = f"""
            Analyze this restaurant's menu healthiness based on the following information:
            
            Website URL: {website_url}
            User Health Goals: {', '.join(user_preferences.get('health_goals', []))}
            User Dietary Restrictions: {', '.join(user_preferences.get('dietary_restrictions', []))}
            
            Please visit the website and analyze the menu. Consider:
            1. The availability of healthy options
            2. How well the menu matches the user's health goals
            3. How well the menu accommodates dietary restrictions
            4. The overall balance of healthy vs unhealthy options
            
            Please provide:
            1. A health score from 0-100 (be specific and use the full range)
            2. 3-5 keywords that best describe the menu's healthiness
            
            Format your response as:
            Score: [number between 0-100]
            Keywords: [comma-separated keywords]
            """
            
            print("Sending prompt to Gemini...")
            # Get Gemini's response
            response = self.model.generate_content(prompt)
            response_text = response.text
            print(f"Gemini response: {response_text}")
            
            # Parse the response to extract score and keywords
            score = 50  # Default score
            keywords = ["Unable to analyze"]
            
            try:
                # Extract score
                score_line = next(line for line in response_text.split('\n') if line.startswith('Score:'))
                score = float(score_line.split(':')[1].strip())
                score = max(0, min(100, score))  # Ensure score is between 0 and 100
                
                # Extract keywords
                keywords_line = next(line for line in response_text.split('\n') if line.startswith('Keywords:'))
                keywords = [k.strip() for k in keywords_line.split(':')[1].split(',')]
                
                print(f"Extracted score: {score}")
                print(f"Extracted keywords: {keywords}")
            except Exception as e:
                print(f"Failed to parse response from Gemini: {str(e)}")
                # If parsing fails, try to extract meaningful words from the response
                words = response_text.split()
                keywords = [word.strip(',.') for word in words if len(word) > 3][:5]
            
            return {
                'score': score,
                'keywords': keywords
            }
            
        except Exception as e:
            print(f"Error analyzing menu with Gemini: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return {
                'score': 50,
                'keywords': ["Analysis failed"]
            }

    def search_places(self, location, radius, user_preferences=None):
        """Search for places near a location with optional user preferences filtering"""
        try:
            # Convert location to tuple if it's a string
            if isinstance(location, str):
                lat, lng = map(float, location.split(','))
                location = (lat, lng)
            
            print(f"\nSearching for restaurants near {location} with radius {radius}m")
            
            # Get user preferences
            health_goals = user_preferences.get('health_goals', []) if user_preferences else []
            dietary_restrictions = user_preferences.get('dietary_restrictions', []) if user_preferences else []
            
            print(f"User preferences - Health goals: {health_goals}")
            print(f"User preferences - Dietary restrictions: {dietary_restrictions}")
            
            # Build search criteria
            search_criteria = {
                'location': location,
                'radius': radius,
                'type': 'restaurant'
            }
            
            # Add all health goals as keywords
            if health_goals:
                search_criteria['keyword'] = ' '.join(health_goals)
            if dietary_restrictions:
                search_criteria['keyword'] = ' '.join(dietary_restrictions)
            
            print(f"Search criteria: {search_criteria}")
            
            # Search for places
            places = self.client.places_nearby(**search_criteria)
            
            if places.get('status') == 'REQUEST_DENIED':
                print("API request was denied. Check API key permissions.")
                return []
            
            if places.get('status') == 'INVALID_REQUEST':
                print("Invalid request parameters. Check location and radius.")
                return []
            
            print(f"Found {len(places.get('results', []))} restaurants")
            
            # Format results
            results = []
            for place in places.get('results', []):
                print(f"\nProcessing restaurant: {place['name']}")
                
                # Get place details including website
                place_details = self.client.place(
                    place['place_id'],
                    fields=['name', 'formatted_address', 'rating', 'price_level', 'website', 'opening_hours']
                )
                place_data = place_details.get('result', {})
                
                website_url = place_data.get('website', '')
                print(f"Found website URL: {website_url}")
                
                # Calculate health score using Gemini
                health_analysis = self.analyze_menu_with_gemini(website_url, user_preferences)
                
                # Extract cuisine types
                cuisine_types = [
                    t for t in place.get('types', [])
                    if t not in ['restaurant', 'food', 'point_of_interest', 'establishment']
                ]
                
                result = {
                    'place_id': place['place_id'],
                    'name': place['name'],
                    'address': place.get('vicinity', ''),
                    'rating': place.get('rating', 0),
                    'price_level': place.get('price_level', 0),
                    'website': website_url,
                    'cuisine_types': cuisine_types,
                    'health_score': health_analysis['score'],
                    'health_keywords': health_analysis['keywords'],
                    'user_preferences': user_preferences
                }
                results.append(result)
                print(f"Added restaurant: {place['name']}")
            
            # Sort results by health score in descending order
            results.sort(key=lambda x: x['health_score'], reverse=True)
            print(f"\nReturning {len(results)} restaurants")
            return results
            
        except Exception as e:
            print(f"Error searching places: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return []

    def get_place_details(self, place_id):
        """Get detailed information about a place"""
        try:
            place = self.client.place(
                place_id,
                fields=['name', 'formatted_address', 'rating', 'price_level', 'website', 'opening_hours']
            )
            return place.get('result', {})
        except Exception as e:
            print(f"Error getting place details: {str(e)}")
            return {}

    # def search_places(self, location, radius, keyword='restaurant'):
    #     """Search for places with menu data"""
    #     try:
    #         results = self.client.places_nearby(
    #             location=location,
    #             radius=radius,
    #             keyword=keyword,
    #             type='restaurant'
    #         )
            
    #         places = []
    #         for place in results.get('results', []):
    #             # Get basic details
    #             place_details = {
    #                 'place_id': place['place_id'],
    #                 'name': place['name'],
    #                 'rating': place.get('rating', 0),
    #                 'price_level': place.get('price_level', 0),
    #                 'types': place.get('types', []),
    #                 'geometry': place.get('geometry', {}),
    #                 'vicinity': place.get('vicinity', '')
    #             }
                
    #             # Check if menu is available
    #             if 'menu' in place.get('types', []):
    #                 place_details['has_menu'] = True
                
    #             places.append(place_details)
            
    #         return places
    #     except Exception as e:
    #         print(f"Error searching places: {e}")
    #         return [] 