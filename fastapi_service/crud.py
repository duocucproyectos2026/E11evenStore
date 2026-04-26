from urllib.response import addbase
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def crear_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def obtener_clientes(db: Session):
    return db.query(models.Cliente).all()

def crear_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_productos(db: Session):
    return db.query(models.Producto).all()

def crear_compra(db: Session, compra: schemas.CompraCreate):
    db_compra = models.Compra(**compra.dict())
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def obtener_compras(db: Session):
    return db.query(models.Compra).all()

def obtener_compras_by_rut(db: Session, rut: str):
    return db.query(models.Compra).filter(models.Compra.cliente_id == rut).all()

def obtener_detalles_by_compra(db: Session, compra_id: int):
    return db.query(models.DetalleCompra).filter(models.DetalleCompra.compra_id == compra_id).all()
    
def get_usuario(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = models.Usuario(username=usuario.username, hashed_password=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
    
def get_cliente(db: Session, rut: str):
    return db.query(models.Cliente).filter(models.Cliente.rut == rut).first()

def get_producto(db: Session, id: int):
    return db.query(models.Producto).filter(models.Producto.id == id).first()

def get_compras(db: Session):
    return db.query(models.Compra).all()

def get_compras_by_rut(db: Session, rut: str):
    return db.query(models.Compra).filter(models.Compra.cliente_id == rut).all()

def get_detalles_by_compra(db: Session, compra_id: int):
    return db.query(models.DetalleCompra).filter(models.DetalleCompra.compra_id == compra_id).all()
