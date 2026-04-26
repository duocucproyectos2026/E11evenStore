from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

#para usar tokens
class Usuario(Base):
    __tablename__ = "E11EVENSTORE_ADMINISTRATIVOS"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, index=True)  
    clave = Column(String(128))


class Cliente(Base):
    __tablename__ = "E11EVENSTORE_CLIENTES"
    rut = Column(String(12), primary_key=True, index=True)
    nombre = Column(String(200))
    apellidos = Column(String(200))
    usuario = Column(String(150))
    email = Column(String(254), unique=True)
    clave = Column(String(128))
    fechaNacimiento = Column("FECHANACIMIENTO", Date)
    direccion = Column(String(255), nullable=True)
    compras = relationship("Compra", back_populates="cliente")

class Producto(Base):
    __tablename__ = "E11EVENSTORE_PRODUCTO"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    descripcion = Column(String(500), nullable=True)
    precio = Column(Integer)
    categoria = Column(String(50))
    imagen = Column(String(2000))
    stock = Column(Integer, default=0)

class Compra(Base):
    __tablename__ = "E11EVENSTORE_COMPRA"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column("CLIENTE_ID", String(12), ForeignKey('E11EVENSTORE_CLIENTES.rut'))
    numero_compra = Column(String(20), unique=True, index=True)
    direccion_envio = Column(String(255))
    metodo_pago = Column(String(50))
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="pendiente")
    cliente = relationship("Cliente", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra")

class DetalleCompra(Base):
    __tablename__ = "E11EVENSTORE_DETALLECOMPRA"
    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey('E11EVENSTORE_COMPRA.id'))
    producto_id = Column(Integer, ForeignKey('E11EVENSTORE_PRODUCTO.id'))
    cantidad = Column(Integer)
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto")
