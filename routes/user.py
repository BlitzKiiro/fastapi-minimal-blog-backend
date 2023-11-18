from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import datetime

from auth.auth import get_password_hash, verify_password, create_access_token, decode_access_token, OAuth2PasswordRequestForm, oauth2_scheme
from db.database import get_db
from dto.user import UserCreate, UserResponse
from dto.token import Token
from repository import user as user_repository

UserRouter = APIRouter()

# @desc   create new user
# @route  post /api/user/register
# @access public
@UserRouter.post('/register')
def register_user(user: UserCreate, db: Session =  Depends(get_db)):
    existing_user = user_repository.get_user_by_username(db=db, username=user.username)
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
    hashed_pwd = get_password_hash(user.password)
    user.password = hashed_pwd
    created_user = user_repository.create_user(db, user)
    token = create_access_token(data={"sub": created_user.username}, expires_delta=datetime.timedelta(minutes=1440))
    return Token(access_token=token, token_type="bearer")


# @desc   login user
# @route  post /api/user/authorize
# @access public
@UserRouter.post('/authorize', response_model=Token)
def login_user(credentials: OAuth2PasswordRequestForm = Depends(), db: Session =  Depends(get_db)):
    user = user_repository.get_user_by_username(db=db, username=credentials.username);
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    isValid = verify_password(credentials.password, user.password)
    if not isValid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username}, expires_delta=datetime.timedelta(minutes=1440))
    return Token(access_token=token, token_type="bearer")

# @desc   get current user
# @route  get /api/user/me
# @access Private
@UserRouter.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session =  Depends(get_db)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = user_repository.get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user