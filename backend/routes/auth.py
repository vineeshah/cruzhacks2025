from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import create_access_token
from models.user import User
from flask_bcrypt import generate_password_hash
import requests
import os
from oauthlib.oauth2 import WebApplicationClient
import json

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Define blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        password_hash = generate_password_hash(data['password']).decode('utf-8')
        user = User.create(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            health_goals=data.get('health_goals', []),
            dietary_restrictions=data.get('dietary_restrictions', []),
            budget_preference=data.get('budget_preference', 'medium')
        )
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.authenticate(data['email'], data['password'])
        if user:
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify({"access_token": access_token}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/google-login', methods=['GET'])
def google_login():
    try:
        # Get Google OAuth configuration
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Create request URI
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/google-login/callback', methods=['GET'])
def google_callback():
    try:
        # Get authorization code
        code = request.args.get("code")
        
        # Get Google OAuth configuration
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]
        
        # Prepare and send request to get tokens
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        
        # Parse tokens
        client.parse_request_body_response(json.dumps(token_response.json()))
        
        # Get userinfo
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        
        # Check if user exists
        user = User.find_by_email(users_email)
        if not user:
            # Create new user
            user = User.create(
                username=users_name,
                email=users_email,
                password=None,  # Google users don't need password
                google_id=unique_id
            )
        
        # Create JWT token
        access_token = create_access_token(identity=str(user['_id']))
        
        # Redirect to frontend with token
        return redirect(f"{os.environ.get('FRONTEND_URL')}/auth/callback?token={access_token}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400
