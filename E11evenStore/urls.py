from django.urls import path
from E11evenStore import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.formulario_registro, name="formulario_registro"),
    path("carro/", views.carro_compras, name="carro_compras"),
    path("inicio_sesion/", views.inicio_sesion, name="inicio_sesion"),
    path("categorias/", views.menu_categorias, name="menu_categorias"),
    path("login_cliente/", views.login_cliente, name="login_cliente"),
    path("login_admin/", views.login_admin, name="login_admin"),
    # Categorías
    path("categoria_accion/", views.categoria_accion, name="accion"),
    path("categoria_carreras/", views.categoria_carreras, name="carreras"),
    path("categoria_free_to_play/", views.categoria_free_to_play, name="free_to_play"),
    path(
        "categoria_mundo_abierto/", views.categoria_mundo_abierto, name="mundo_abierto"
    ),
    path(
        "categoria_supervivencia/", views.categoria_supervivencia, name="supervivencia"
    ),
    path("categoria_terror/", views.categoria_terror, name="terror"),
    path(
        "agregar-carro/<int:producto_id>/",
        views.agregar_al_carro,
        name="agregar_al_carro",
    ),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
]
