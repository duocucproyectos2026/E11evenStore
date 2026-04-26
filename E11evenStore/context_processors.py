from .models import Producto
from .models import Cliente
import requests
from django.conf import settings


def contador_carro(request):
    carro = request.session.get("carro", [])
    total_items = sum(item["cantidad"] for item in carro)
    total_precio = 0
    for item in carro:
        try:
            producto = Producto.objects.get(id=item["producto_id"])
            total_precio += producto.precio * item["cantidad"]
        except Producto.DoesNotExist:
            pass
    return {"contador_carro": total_items, "precio_carro": total_precio}


def cliente_context(request):
    email = request.session.get("email_cliente")
    cliente = None
    if email:
        try:
            cliente = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            pass
    return {"cliente": cliente}


# vista externa API�S
def vista_externa(request):
    # Obtener los juegos desde la API de RAWG
    api_key_rawg = settings.RAWG_API_KEY
    juegos = []

    try:
        response = requests.get(
            "https://api.rawg.io/api/games",  # endpoints
            params={"key": api_key_rawg, "ordering": "-rating", "page_size": 6},
        )
        if response.status_code == 200:
            juegos = response.json().get("results", [])
    except Exception as e:
        print("Error cargando juegos:", e)

    # Obtener noticias desde NewsAPI
    api_key_news = settings.NEWS_API_KEY
    noticias = []

    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",  # endpoints
            params={
                "q": "videojuegos",
                "apiKey": api_key_news,
                "language": "es",  # Noticias en espa�ol
                "pageSize": 6,  # cantidad en vista
            },
        )
        if response.status_code == 200:
            noticias = response.json().get("articles", [])
    except Exception as e:
        print("Error cargando noticias:", e)

    return {"juegos": juegos, "noticias": noticias}
