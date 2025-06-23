from fastapi import APIRouter, Request, Response, Depends, HTTPException, status, Security
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests as req
import json
import secrets

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID").strip('"')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET").strip('"')
JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_hex(32)).strip('"')
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://mindgarden-app-6xntrakg7q-nw.a.run.app")
# Use environment variable for redirect URI with a development fallback
# Make sure this matches exactly what's configured in Google Cloud Console
REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://mindgarden-6xntrakg7q-nw.a.run.app/auth/google/callback")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24  # 24 hours

# Router
router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

def create_jwt_token(user_data: Dict) -> str:
    """Create a JWT token for the authenticated user"""
    payload = {
        "sub": user_data["user_id"],
        "email": user_data["email"],
        "name": user_data.get("name", ""),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth login"""
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20email%20profile&access_type=offline&prompt=consent"
    return RedirectResponse(url=auth_url)

@router.get("/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        response = req.post(token_url, data=payload)
        token_data = response.json()
        
        if "error" in token_data:
            return JSONResponse(
                status_code=400,
                content={"detail": f"OAuth error: {token_data.get('error_description', token_data['error'])}"}
            )
        
        if "id_token" not in token_data:
            return JSONResponse(
                status_code=400,
                content={"detail": "Authentication failed"}
            )
        
        # Get user info from Google
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        userinfo_response = req.get(userinfo_url, headers=headers)
        user_info = userinfo_response.json()
        
        if "error" in user_info:
            return JSONResponse(
                status_code=400,
                content={"detail": "Failed to get user info"}
            )
        
        # Create user data
        user_data = {
            "user_id": user_info["sub"],
            "email": user_info["email"],
            "name": user_info.get("name", ""),
            "picture": user_info.get("picture", ""),
        }
        
        # Here you would typically save user to database
        # For example: await save_user(user_data)

        # Create JWT token
        access_token = create_jwt_token(user_data)
        
        # Redirect to frontend
        redirect_url = f"{FRONTEND_URL}?token={access_token}"
        print(f"Redirecting to: {redirect_url}")
        print(f"FRONTEND_URL from env: {os.environ.get('FRONTEND_URL', 'Not set')}")
        print(f"FRONTEND_URL used: {FRONTEND_URL}")
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Authentication failed: {str(e)}"}
        )

# For client-side token verification (used by the existing frontend)
@router.post("/verify-google-token")
async def verify_google_token(token: str):
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        
        # Check if the token is issued by Google
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer')
            
        # Create user data
        user_data = {
            "user_id": idinfo["sub"],
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
        }
        
        # Create JWT token
        access_token = create_jwt_token(user_data)
        
        # Return the token and user information
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_data["user_id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "picture": user_data.get("picture", "")
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check if token is expired
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
            
        return {
            "user_id": payload["sub"],
            "email": payload["email"],
            "name": payload.get("name", "")
        }
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me")
async def get_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information from JWT token"""
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "name": current_user.get("name", "")
    }
