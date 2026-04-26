# ----------- SERIALIZERS ---------------
from rest_framework import serializers
from .models import Producto, Compra, DetalleCompra

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class DetalleCompraSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad']

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    class Meta:
        model = Compra
        fields = ['numero_compra', 'direccion_envio', 'metodo_pago', 'fecha', 'estado', 'detalles']
