from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config
import certifi

def setup_database():
    try:
        # Connect to MongoDB
        client = MongoClient(
            Config.MONGO_URI,
            tlsCAFile=certifi.where()
        )
        db = client.get_database()

        # Create collections if they don't exist
        collections = {
            'users': {
                'indexes': [
                    [('email', ASCENDING), {'unique': True}],
                    [('google_id', ASCENDING), {'unique': True, 'sparse': True}]
                ]
            },
            'restaurants': {
                'indexes': [
                    [('place_id', ASCENDING), {'unique': True}],
                    [('name', ASCENDING)],
                    [('location', '2dsphere')]
                ]
            },
            'food_items': {
                'indexes': [
                    [('restaurant_id', ASCENDING)],
                    [('name', ASCENDING)],
                    [('health_score', DESCENDING)]
                ]
            },
            'user_preferences': {
                'indexes': [
                    [('user_id', ASCENDING), {'unique': True}]
                ]
            }
        }

        # Create collections and indexes
        for collection_name, config in collections.items():
            if collection_name not in db.list_collection_names():
                print(f"Creating collection: {collection_name}")
                db.create_collection(collection_name)
            
            # Create indexes
            for index in config['indexes']:
                try:
                    db[collection_name].create_index(index[0], **index[1])
                    print(f"Created index on {collection_name}: {index[0]}")
                except Exception as e:
                    print(f"Error creating index on {collection_name}: {e}")

        print("\n✅ Database setup completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database() 