import os
import httpx
import pandas as pd
import sys
from pathlib import Path
import time
import json
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

class RecipeSearchService:
    def __init__(self):
        self.api_key = Config.GOOGLE_SEARCH_API_KEY
        self.engine_id = Config.SEARCH_ENGINE_ID


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
    
