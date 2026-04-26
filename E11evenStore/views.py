# ------------- VIEWS.PY ---------------------

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import LoginForm
from .models import Administrativo
from .models import Cliente
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Producto, Compra, DetalleCompra
from .forms import DireccionEnvioForm, MetodoPagoForm
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditarClienteForm
from django.contrib.admin.views.decorators import staff_member_required
from .serializers import ProductoSerializer, CompraSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .decorators import cliente_login_required
from .decorators import admin_login_required
from django.shortcuts import render, redirect
from .models import Producto
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import TransaccionPago


def inicio(request):
    return render(request, "index.html")


def contacto(request):
    return render(request, "contacto.html")


def menu_categorias(request):
    return render(request, "menu_categorias.html")

    # categorias menu #


def categoria_accion(request):
    productos = Producto.objects.filter(categoria="CAT_5-Accion")
    return render(request, "accion.html", {"productos": productos})


def categoria_terror(request):
    productos = Producto.objects.filter(categoria="CAT_2-Terror")
    return render(request, "terror.html", {"productos": productos})


def categoria_mundo_abierto(request):
    productos = Producto.objects.filter(categoria="CAT_3-Mundo abierto")
    return render(request, "mundo_abierto.html", {"productos": productos})


def categoria_free_to_play(request):
    productos = Producto.objects.filter(categoria="CAT_4-Free to play")
    return render(request, "free_to_play.html", {"productos": productos})


def categoria_supervivencia(request):
    productos = Producto.objects.filter(categoria="CAT_6-Supervivencia")
    return render(request, "supervivencia.html", {"productos": productos})


def categoria_carreras(request):
    productos = Producto.objects.filter(categoria="CAT_1-Carreras")
    return render(request, "carreras.html", {"productos": productos})


# INICIO SESION COMUN
def inicio_sesion(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            clave = form.cleaned_data["clave"]
            es_admin = request.POST.get(
                "es_admin"
            )  # Esto nos indica si es admin o cliente

            if es_admin == "1":
                try:
                    admin = Administrativo.objects.get(email=email, clave=clave)
                    request.session["email_admin"] = admin.email
                    messages.success(request, "¡Bienvenido Administrador!")
                    return redirect("login_admin")
                except Administrativo.DoesNotExist:
                    form.add_error(
                        None, "Acceso denegado. Administrador no registrado."
                    )
            else:
                # inicio sesion como cliente
                try:
                    cliente = Cliente.objects.get(email=email, clave=clave)
                    # Guardar datos del cliente en la sesión como diccionario
                    request.session["cliente"] = {
                        "nombre": cliente.nombre,
                        "email": cliente.email,
                    }
                    request.session["email_cliente"] = cliente.email
                    messages.success(request, "¡Bienvenido Cliente!")
                    return redirect("login_cliente")
                except Cliente.DoesNotExist:
                    form.add_error(None, "Correo o contraseña incorrectos.")

    return render(request, "inicio_sesion.html", {"form": form})


# REGISTRO FORMULARIO CLIENTES
def formulario_registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            messages.success(
                request, f" ✅ Registro exitoso. Ahora puedes ingresar sesión 🔑 "
            )
            return redirect("inicio_sesion")
        else:
            print("Errores del formulario:", form.errors.as_data())  #
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistroForm()

    return render(request, "formulario_registro.html", {"form": form})


# CARRO COMPRAS
def carro_compras(request):
    carro = request.session.get("carro", [])
    email_cliente = request.session.get("email_cliente")
    cliente = Cliente.objects.filter(email=email_cliente).first()

    # Mostrar productos del carro
    productos_carro = []
    total = 3990  # Costo fijo de envío

    for item in carro:
        producto = Producto.objects.get(id=item["producto_id"])
        cantidad = item["cantidad"]
        subtotal = producto.precio * cantidad
        total += subtotal
        productos_carro.append(
            {
                "producto": producto,
                "cantidad": cantidad,
                "precio": producto.precio,
                "subtotal": subtotal,
            }
        )

    if request.method == "POST":
        if not cliente:
            messages.warning(
                request, "Debes iniciar sesión o registrarte para completar la compra."
            )
            return redirect("inicio_sesion")

        # Eliminar producto individual
        if "eliminar_producto" in request.POST:
            producto_id = int(request.POST["eliminar_producto"])
            carro = [item for item in carro if item["producto_id"] != producto_id]
            request.session["carro"] = carro
            return redirect("carro_compras")

        # Vaciar carro completo
        elif "vaciar_carro" in request.POST:
            request.session["carro"] = []
            return redirect("carro_compras")

        form_direccion = DireccionEnvioForm(request.POST)
        form_pago = MetodoPagoForm(request.POST)

        if form_direccion.is_valid() and form_pago.is_valid():
            if not carro:
                messages.error(request, "Tu carro está vacío.")
                return redirect("carro_compras")

            numero_compra = f"E11-{random.randint(100000, 999999)}"
            metodo_pago = form_pago.cleaned_data["metodo_pago"]
            direccion_envio = form_direccion.cleaned_data["direccion"]

            codigo_giftcard = None
            if metodo_pago == "GiftCard":
                codigo_giftcard = request.POST.get("codigo_giftcard", "").strip()
                if not codigo_giftcard or len(codigo_giftcard) < 6:
                    messages.error(
                        request, "Debes ingresar un código de GiftCard válido."
                    )
                    return redirect("carro_compras")

            compra = Compra.objects.create(
                cliente=cliente,
                numero_compra=numero_compra,
                direccion_envio=direccion_envio,
                metodo_pago=metodo_pago,
                estado="Aprobado",  # valor por defecto
            )

            total = 0
            for item in carro:
                producto = get_object_or_404(Producto, id=item["producto_id"])
                cantidad = item["cantidad"]
                DetalleCompra.objects.create(
                    compra=compra, producto=producto, cantidad=cantidad
                )
                total += producto.precio * cantidad

            total += 3990

            # Crear transacción de pago vinculada a la compra
            TransaccionPago.objects.create(
                compra=compra,
                metodo_pago=metodo_pago.lower(),
                estado="Aprobado",
                monto=total,
                codigo_autorizacion=(
                    codigo_giftcard if metodo_pago == "GiftCard" else None
                ),
            )

            # Mensajes según método de pago
            if metodo_pago == "Transferencia":
                messages.success(
                    request,
                    "Te hemos enviado a tu correo registrado los datos de transferencia...",
                )
            elif metodo_pago == "GiftCard":
                messages.success(
                    request,
                    "Se ha validado tu GiftCard. Compra registrada correctamente.",
                )
            elif metodo_pago == "Debito/Credito":
                messages.info(request, "Redirigiéndote a Webpay...")
                messages.success(request, "¡Felicidades! Compra realizada con éxito.")

            # Enviar correo de confirmación
            send_mail(
                "Confirmación de compra - E11ven Store",
                f"Tu número de compra es {numero_compra}. Total: ${total}. Dirección de envío: {direccion_envio}",
                "E11venStore@gmail.com",
                [cliente.email],
                fail_silently=True,
            )

            # Limpiar carro
            request.session["carro"] = []
            messages.success(request, f"Compra {numero_compra} confirmada ✅")
            return redirect("login_cliente")

    else:
        form_direccion = DireccionEnvioForm() if cliente else None
        form_pago = MetodoPagoForm() if cliente else None

    return render(
        request,
        "carro_compras.html",
        {
            "form_direccion": form_direccion,
            "form_pago": form_pago,
            "productos_carro": productos_carro,
            "total": total,
            "cliente": cliente,
            "cliente_logeado": cliente is not None,
        },
    )


# AGREGAR AL CARRO
@require_POST
def agregar_al_carro(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get("cantidad", 1))

    carro = request.session.get("carro", [])

    for item in carro:
        if item["producto_id"] == producto.id:
            item["cantidad"] += cantidad
            break
    else:
        carro.append(
            {
                "producto_id": producto.id,
                "cantidad": cantidad,
                "precio": producto.precio,  # Guarda el precio actual
            }
        )

    request.session["carro"] = carro
    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect(request.META.get("HTTP_REFERER", "menu_categorias"))


# Panel administrador
@admin_login_required
def login_admin(request):
    productos = Producto.objects.all().order_by("nombre", "categoria")
    compras_recientes = Compra.objects.all().order_by("-fecha")[:10]
    historial = []
    cliente = None
    categoria = ""
    tab_activa = "carrito"

    if request.method == "POST":
        if "buscar_cliente" in request.POST:
            rut = request.POST.get("rut")
            print(">>> RUT ingresado:", rut)
            if rut:
                rut = limpiar_rut(rut)
            try:
                cliente = Cliente.objects.get(rut=rut)
                print(">>> Cliente encontrado:", cliente)
                historial = Compra.objects.filter(cliente=cliente).order_by("-fecha")
                tab_activa = "buscar_compras"
            except Cliente.DoesNotExist:
                print(">>> Cliente NO encontrado")
                messages.error(request, "Cliente no encontrado.")
                tab_activa = "buscar_compras"

        elif "buscar_categoria" in request.POST:  # Botón buscar_categoria
            categoria = request.POST.get("categoria")
            if categoria:
                productos = Producto.objects.filter(categoria=categoria).order_by(
                    "nombre"
                )
            tab_activa = "inventario"

        else:
            # Aquí debería ser guardado un nuevo producto
            nombre = request.POST.get("nombre")
            descripcion = request.POST.get("descripcion")
            precio = request.POST.get("precio")
            categoria = request.POST.get("categoria")
            stock = request.POST.get("stock")
            imagen = request.FILES.get("imagen")

            if nombre and descripcion and precio and categoria and stock:
                Producto.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    categoria=categoria,
                    stock=stock,
                    imagen=imagen,
                )
                messages.success(request, "Producto guardado exitosamente.")
            else:
                messages.error(
                    request, "Todos los campos son requeridos para agregar un producto."
                )
            tab_activa = "productos"

    context = {
        "productos": productos,
        "compras_recientes": compras_recientes,
        "compras": historial,
        "cliente": cliente,
        "tab_activa": tab_activa,
        "categoria_seleccionada": categoria,
    }
    return render(request, "login_admin.html", context)


def limpiar_rut(rut):
    if rut:
        return rut.replace(".", "").strip()
    return rut


@admin_login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect("login_admin")


# DATOS CLIENTES
@cliente_login_required
def login_cliente(request):
    email = request.session.get("email_cliente")

    if not email:
        messages.error(request, "Debes iniciar sesión para acceder.")
        return redirect("inicio_sesion")

    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect("inicio_sesion")

    compras = Compra.objects.filter(cliente=cliente).order_by("-fecha")

    # Calcular totales para cada compra
    compras_con_totales = []

    if compras.exists():
        for compra in compras:
            total = sum(detalle.subtotal() for detalle in compra.detalles.all())
            compras_con_totales.append(
                {
                    "compra": compra,
                    "total": total,
                }
            )
    else:
        compras_con_totales.append(
            {
                "compra": None,
                "total": 0,
            }
        )

    if request.method == "POST":
        form = EditarClienteForm(request.POST, instance=cliente)
        pass_form = PasswordChangeForm(user=request.user, data=request.POST)

        if "guardar_datos" in request.POST and form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente")
        elif "cambiar_contraseña" in request.POST and pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, "Contraseña actualizada")
        else:
            messages.error(request, "Error al guardar los cambios")
    else:
        form = EditarClienteForm(instance=cliente)
        pass_form = PasswordChangeForm(user=request.user)

    return render(
        request,
        "login_cliente.html",
        {
            "cliente": cliente,
            "compras_con_totales": compras_con_totales,
            "form": form,
            "pass_form": pass_form,
        },
    )


# cierre de sesion
def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada exitosamente.")
    return redirect("inicio")


# VISTA DE PAGO POR WEBPAY SIMULADA
@login_required
def redirigir_webpay(request):
    # Simulación: redirigir a una URL de prueba de WebPay
    return redirect("https://webpay3g.transbank.cl/webpay-server/initTransaction")
