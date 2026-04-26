from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from . import models  
from sqlalchemy.orm import Session
from .database import get_db  
import os

# Configuración de la clave secreta y el algoritmo para JWT
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32)) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para manejo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esto sirve para obtener el token desde el encabezado de la petición
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener el usuario actual a partir del token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Validando token...")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Extraemos el 'sub' del token, que es el email
        if username is None:
            raise credentials_exception
        # Obtener el usuario de la base de datos
        user = db.query(models.Usuario).filter(models.Usuario.email == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

# Función para hashear las contraseñas (si decides usar contraseñas hasheadas)
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Función para verificar la contraseña (si decides usar contraseñas hasheadas)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
