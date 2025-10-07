from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas.auth import Token, UserCreate, UserLogin
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.core.logging import logger
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

# Mock user database (in production, use a real database)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "is_active": True,
    }
}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint for user authentication.
    
    - **username**: Username
    - **password**: Password
    
    Returns JWT access token.
    """
    try:
        user = fake_users_db.get(form_data.username)
        
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            logger.warning("Login failed", username=form_data.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user["is_active"]:
            logger.warning("Login attempt for inactive user", username=form_data.username)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user["username"]}, 
            expires_delta=access_token_expires
        )
        
        logger.info("User logged in successfully", username=form_data.username)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login error", error=str(e), username=form_data.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/register")
async def register(user: UserCreate):
    """
    Register a new user.
    
    - **username**: Username (must be unique)
    - **email**: Email address
    - **password**: Password
    
    Returns success message.
    """
    try:
        if user.username in fake_users_db:
            logger.warning("Registration attempt with existing username", username=user.username)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        fake_users_db[user.username] = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "is_active": True,
        }
        
        logger.info("User registered successfully", username=user.username)
        
        return {
            "message": "User registered successfully",
            "username": user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration error", error=str(e), username=user.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information.
    
    Returns user details for the authenticated user.
    """
    try:
        username = current_user["username"]
        user = fake_users_db.get(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "username": user["username"],
            "email": user["email"],
            "is_active": user["is_active"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Get user info error", error=str(e), username=current_user.get("username"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
