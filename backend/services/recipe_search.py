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
 
 api_key = Config.GOOGLE_SEARCH_API_KEY
 engine_id = Config.SEARCH_ENGINE_ID
 
 
 def google_search(api_key, engine_id, query, **params):
     base_url = 'https://www.googleapis.com/customsearch/v1'
     params = {
         'key' : api_key,
         'cx' : engine_id,
         'q' : query,
         **params
     }
     
     # Create a client with custom timeout settings
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
 
 #recipe_queries = []
 def search_recipes(preferences):
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
             response = google_search(
                 api_key,
                 engine_id,
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
 
 test_search = search_recipes(['low carb', 'keto'])
 print(test_search)
 print(len(test_search['low carb']))