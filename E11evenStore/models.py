# ---------------- MODELS.PY ----------------

from django.db import models


# REGISTRO CLIENTE
class Cliente(models.Model):
    rut = models.CharField(primary_key=True, max_length=12, verbose_name="RUT")
    nombre = models.CharField(max_length=200, verbose_name="Nombres")
    apellidos = models.CharField(max_length=200, verbose_name="Apellidos")
    usuario = models.CharField(
        max_length=150, unique=True, verbose_name="Nombre Usuario", blank=True
    )
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    clave = models.CharField(max_length=128, verbose_name="Contraseña")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    direccion = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Dirección"
    )

    class Meta:
        db_table = "E11EVENSTORE_CLIENTES"

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellidos:
            self.apellidos = self.apellidos.upper()
        if self.usuario:
            self.usuario = self.usuario.upper()
        if self.email:
            self.email = self.email.lower()
        if self.direccion:
            self.direccion = self.direccion.upper()
        super().save(*args, **kwargs)


# REGISTRO ADMINISTRADORES
class Administrativo(models.Model):
    rut = models.CharField(unique=True, max_length=12)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    clave = models.CharField(max_length=128)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "E11EVENSTORE_ADMINISTRATIVOS"

    def __str__(self):
        return f"Administrativo: {self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellidos:
            self.apellidos = self.apellidos.upper()
        if self.email:
            self.email = self.email.lower()
        if self.direccion:
            self.direccion = self.direccion.upper()
        super().save(*args, **kwargs)


# PRODUCTOS
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    precio = models.PositiveIntegerField()
    CATEGORIAS = [
        ("CAT_1-Carreras", "Carreras"),
        ("CAT_2-Terror", "Terror"),
        ("CAT_3-Mundo abierto", "Mundo abierto"),
        ("CAT_4-Free to play", "Free to play"),
        ("CAT_5-Accion", "Acción"),
        ("CAT_6-Supervivencia", "Supervivencia"),
    ]
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    imagen = models.URLField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"


def save(self, *args, **kwargs):
    if self.nombre:
        self.nombre = self.nombre.upper()
    super().save(*args, **kwargs)


class Compra(models.Model):
    cliente = models.ForeignKey(
        Cliente, to_field="rut", on_delete=models.CASCADE, related_name="compras"
    )
    numero_compra = models.CharField(
        max_length=20, unique=True, verbose_name="Número de compra"
    )
    direccion_envio = models.CharField(
        max_length=255, verbose_name="Dirección de envío"
    )
    metodo_pago = models.CharField(max_length=50, verbose_name="Método de pago")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de compra")
    estado = models.CharField(
        max_length=20,
        choices=[("pendiente", "Pendiente"), ("enviado", "Enviado")],
        default="pendiente",
        verbose_name="Estado de compra",
    )

    def __str__(self):
        return f"Compra #{self.numero_compra} - {self.cliente}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra, on_delete=models.CASCADE, related_name="detalles", default=1
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Compra {self.compra.numero_compra})"


# Transacciones de pago
class TransaccionPago(models.Model):
    COMPRA_ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("completado", "Completado"),
        ("fallido", "Fallido"),
    ]

    compra = models.ForeignKey(
        "Compra", on_delete=models.CASCADE, related_name="transacciones"
    )
    metodo_pago = models.CharField(
        max_length=30,
        choices=[
            ("giftcard", "GiftCard"),
            ("debito", "Débito"),
            ("credito", "Crédito"),
            ("transferencia", "Transferencia Bancaria"),
        ],
    )
    estado = models.CharField(
        max_length=15, choices=COMPRA_ESTADO_CHOICES, default="pendiente"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    codigo_autorizacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.metodo_pago} - {self.estado} - ${self.monto}"
