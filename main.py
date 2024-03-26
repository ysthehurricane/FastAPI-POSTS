# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, User, Post, Base
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import hashlib
from models import User, Post
# Initialize app
app = FastAPI()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Token
SECRET_KEY = "ggrt456fd233rff32!#_76f3#z$dfgb1W"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Verify password
def verify_password(plain_password, hashed_password):

    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

# Authenticate user
def authenticate_user(db: Session, username: str, password: str):

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return False
    return user

# Get current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# Sign Up Endpoint
@app.post("/signup")
def sign_up(user: User, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()

    return {"message": "User created successfully"}

# Login Endpoint
@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = authenticate_user(db, username, password)

    if not user:

        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Add Post Endpoint

@app.post("/addPost")
def add_post(post: Post, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = Post(**post.dict(), owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    return {"postID": db_post.id}

    

# Get Posts Endpoint
@app.get("/getPosts", response_model=List[Post])
def get_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return db.query(Post).filter(Post.owner_id == current_user.id).all()

# Delete Post Endpoint
@app.delete("/deletePost")
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == current_user.id).first()

    if not post:

        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)

    db.commit()

    return {"message": "Post deleted successfully"}
