import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from requests import Session

from backend.classes.db_classes import User
from backend.database.Service import UserService
from backend.database.dependency_db import get_db
from backend.other import helper

ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_KEY = helper.generate_jwt_key_file_if_not_exist()
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: datetime.timedelta =  datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session) -> dict[str, str]:
    user = UserService.get_by_mail(form_data.username, db)

    if user is None:
        raise HTTPException(401, "User not found")

    verified = verify_password(form_data.password, user.user_password)

    if not verified:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {"sub": user.user_email},
        expires_delta= datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}   # This is just how you do it


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])    # decode the token with the key.
        email: str = payload.get("sub")     # read the email from it, which we put there when user logged in.
        if email is None or email == "":
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    return UserService.get_by_mail(email, db)  # return the user associated with this mail


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def encode_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


