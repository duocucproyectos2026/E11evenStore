from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from .auth import create_access_token, get_current_user
from fastapi import status
from passlib.context import CryptContext
from . import models, schemas, crud
from .database import get_db


# Inicialización de la base de datos
models.Base.metadata.create_all(bind=engine)

# Cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear la app FastAPI
app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],  # Permite dominios locales para pruebas
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de seguridad OAuth2 para los tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# **Rutas protegidas con token**

@app.get("/protected")
def protected_route(user: models.Usuario = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": user.username}

# **Generación de token (Login)**

@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Buscar al usuario en la base de datos
    print(f"Buscando usuario con email: {form_data.username}")  # Depuración
    admin = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()

    if not admin:
        print("Usuario no encontrado")  # Depuración
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Depuración: Mostrar el usuario encontrado
    print(f"Usuario encontrado: {admin.email}")  # Depuración

    # Comparar la contraseña en texto plano
    if form_data.password != admin.clave:  
        print(f"Contraseña incorrecta: {form_data.password} != {admin.clave}")  # Depuración
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Si las credenciales son correctas, generamos el token
    access_token = create_access_token(data={"sub": admin.email})
    print(f"Token generado para el usuario: {admin.email}")  # Depuración

    return {"access_token": access_token, "token_type": "bearer"}

# **Crear Cliente**

@app.post("/clientes/", response_model=schemas.ClienteOut)
def crear_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db),
):
    return crud.crear_cliente(db, cliente)

# **Crear Producto**

@app.post("/productos/", response_model=schemas.ProductoOut)
def crear_producto(
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db),
):
    return crud.crear_producto(db, producto)

# **Listar Clientes**

@app.get("/clientes/", response_model=List[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.obtener_clientes(db)

# **Obtener Cliente por RUT**

@app.get("/clientes/{rut}", response_model=schemas.ClienteBase)
def obtener_cliente(rut: str, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, rut)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# **Listar Productos**

@app.get("/productos/", response_model=List[schemas.ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

# **Obtener Producto por ID**

@app.get("/productos/{id}", response_model=schemas.ProductoBase)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = crud.get_producto(db, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# **Listar Compras**

@app.get("/compras", response_model=List[schemas.CompraBase])
def listar_compras(db: Session = Depends(get_db)):
    return crud.get_compras(db)

# **Listar Compras por Cliente**

@app.get("/compras/{rut}", response_model=List[schemas.CompraBase])
def listar_compras_cliente(rut: str, db: Session = Depends(get_db)):
    return crud.get_compras_by_rut(db, rut)

# **Obtener Detalles de Compra**

@app.get("/detalles/{compra_id}", response_model=List[schemas.DetalleCompraBase])
def obtener_detalles(compra_id: int, db: Session = Depends(get_db)):
    return crud.get_detalles_by_compra(db, compra_id)
