# cruzhacks2025

# IdealMeal

Your personal guide to healthier eating, connecting you directly to healthier alternatives for any food craving.

## Features

-  Find healthier restaurant options near you
-  Access healthy recipes from trusted sources
-  Personalized recommendations based on your preferences
-  Filter by health goals and dietary restrictions
-  Clean, intuitive interface

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- MongoDB
- Google Places API key
- Google Gemini API key

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/idealmeal.git
cd idealmeal/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with:
```env
MONGODB_URI=your_mongodb_uri
GOOGLE_PLACES_API_KEY=your_google_places_api_key
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET=your_jwt_secret
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:5000
```

## Running the Application

### Start the Backend Server

1. Make sure you're in the backend directory and your virtual environment is activated
2. Run the Flask server:
```bash
python app.py
```

The backend server will start on `http://localhost:5000`

### Start the Frontend Development Server

1. Make sure you're in the frontend directory
2. Start the React development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## API Documentation

The backend API documentation is available at `http://localhost:5000/api/docs` when the server is running.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Places API for location services
- Google Gemini AI for intelligent recommendations
- All the amazing recipe websites that make healthy eating possible

## Support

For support, email support@idealmeal.com or open an issue in the GitHub repository.
