from pymongo import MongoClient
from config import Config
import google.generativeai as genai
import googlemaps
import sys
import ssl
import certifi

# def list_gemini_models():
#     try:
#         print("\nListing available Gemini models...")
#         genai.configure(api_key=Config.GEMINI_API_KEY)
#         for m in genai.list_models():
#             if 'generateContent' in m.supported_generation_methods:
#                 print(f"Model: {m.name}")
#                 print(f"Description: {m.description}")
#                 print(f"Supported methods: {m.supported_generation_methods}")
#                 print("---")
#         return True
#     except Exception as e:
#         print(f"❌ Failed to list models: {str(e)}")
#         return False

def test_mongodb_connection():
    try:
        print("Attempting to connect to MongoDB...")
        print(f"Python version: {sys.version}")
        print(f"SSL version: {ssl.OPENSSL_VERSION}")
        print(f"Using connection string: {Config.MONGO_URI}")
        
        # Test connection with SSL verification
        client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=30000,
            socketTimeoutMS=30000,
            connectTimeoutMS=30000,
            retryWrites=True,
            retryReads=True,
            maxPoolSize=50,
            minPoolSize=10,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=False,
            tlsAllowInvalidHostnames=False
        )
        
        # Force a connection and get server info
        print("\nTesting server connection...")
        server_info = client.server_info()
        print("✅ Server connection successful!")
        print(f"Server version: {server_info.get('version', 'unknown')}")
        print(f"Server type: {server_info.get('type', 'unknown')}")
        
        # Test database access
        print("\nTesting database access...")
        db = client.get_database()
        print(f"✅ Connected to database: {db.name}")
        
        # List all collections
        print("\nCollections in database:")
        for collection in db.list_collection_names():
            print(f"- {collection}")
        
        return True
    except Exception as e:
        print(f"\n❌ MongoDB connection failed: {str(e)}")
        print(f"Connection URI: {Config.MONGO_URI}")
        print(f"Error type: {type(e).__name__}")
        print("\nTroubleshooting steps:")
        print("1. Check if your IP address is whitelisted in MongoDB Atlas")
        print("2. Verify your MongoDB Atlas cluster is running")
        print("3. Check your internet connection")
        print("4. Try connecting using MongoDB Compass")
        print("5. Verify the connection string matches exactly with Compass")
        print("6. Check if SSL certificates are properly installed")
        return False

def test_gemini_connection():
    try:
        print("\nAttempting to connect to Gemini API...")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello")
        print("✅ Gemini API connection successful!")
        return True
    except Exception as e:
        print(f"❌ Gemini API connection failed: {str(e)}")
        return False

def test_google_places_connection():
    try:
        print("\nAttempting to connect to Google Places API...")
        print(f"Using API Key: {Config.GOOGLE_PLACES_API_KEY[:10]}...")
        
        # Test direct client creation
        client = googlemaps.Client(key=Config.GOOGLE_PLACES_API_KEY)
        print("✅ Google Maps client created successfully")
        
        # Test with a known place ID (e.g., Google HQ)
        result = client.place('ChIJj61dQgK6j4AR4GeTYWZsKWw', fields=['name', 'formatted_address'])
        print("✅ Google Places API connection successful")
        print(f"Test place: {result.get('result', {}).get('name', 'Unknown')}")
        print(f"Address: {result.get('result', {}).get('formatted_address', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Google Places API connection failed: {e}")
        print("Error details:")
        print(f"Status: {getattr(e, 'status_code', 'Unknown')}")
        print(f"Message: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing all API connections...")
    print("Python version:", sys.version)
    
    # List Gemini models first
    # list_gemini_models()
    
    mongo_success = test_mongodb_connection()
    gemini_success = test_gemini_connection()
    places_success = test_google_places_connection()
    
    if all([mongo_success, gemini_success, places_success]):
        print("\n🎉 All connections successful!")
    else:
        print("\n❌ Some connections failed. Please check the error messages above.") 