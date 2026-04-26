# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cliente
from .models import Producto


@receiver(user_logged_in)
def migrar_carro_despues_login(sender, request, user, **kwargs):
    carro = request.session.get("carro", [])
    if not carro:
        return

    cliente = Cliente.objects.filter(email=user.email).first()
    if not cliente:
        return  # No hay cliente asociados al email

    # Opcional: evitar duplicados
    productos_existentes = set()
    for item in carro:
        productos_existentes.add(item["producto_id"])

    print(
        f"Migrando {len(productos_existentes)} productos al perfil de {cliente.nombre}"
    )

    # El carro sigue en session, pero ligado al cliente
    request.session["email_cliente"] = cliente.email
