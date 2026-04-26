from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class ClienteBase(BaseModel):
    rut: str
    nombre: str
    apellidos: str
    usuario: str
    email: str
    clave: str
    fechaNacimiento: date
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    class Config:
        orm_mode = True

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int
    categoria: str
    imagen: Optional[str] = None
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    class Config:
        orm_mode = True

class DetalleCompraBase(BaseModel):
    producto_id: int
    cantidad: int
    class Config:
        orm_mode = True

class DetalleCompraCreate(BaseModel):
    pass

class DetalleCompraOut(BaseModel):
    id: int
    class Config:
        orm_mode = True

class CompraBase(BaseModel):
    id: int
    numero_compra: str
    direccion_envio: str
    metodo_pago: str
    fecha: datetime
    estado: str
    detalles: List[DetalleCompraBase] = []
    class Config:
        orm_mode = True

class CompraCreate(BaseModel):
    pass

class CompraOut(BaseModel):
    id: int
    class Config:
        orm_mode = True

# usuario tokens vista protegida
class UsuarioBase(BaseModel):
    email: str  # email usado como usuario 

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
