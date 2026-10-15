
import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


app = FastAPI(title="FastAPI JWT Authentication Practice")


# JWT CONFIGURATION
# Set SECRET_KEY in your environment before running the app.
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Set it as an environment variable."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# PASSWORD HASHING SETUP
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


# OAUTH2 SETUP
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DEMO USER DATABASE
# Learning example only. Do not use this in production.
fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234")
    }
}


# VERIFY PASSWORD
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# CREATE ACCESS TOKEN
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# LOGIN API
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_user_db.get(form_data.username)

    if not user or not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        {"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# VERIFY ACCESS TOKEN
def verify_token(
    token: str = Depends(oauth2_scheme)
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username or not isinstance(username, str):
            raise credentials_exception

        return username

    except JWTError:
        raise credentials_exception


# PROTECTED API
@app.get("/protected")
def protected_data(
    username: str = Depends(verify_token)
):
    return {
        "message": (
            f"Hello {username}, you have access "
            "to this protected route!"
        ),
        "user": username
    }
