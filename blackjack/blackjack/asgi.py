import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import game.routing  # Импортируем маршруты WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Обычные HTTP-запросы
    "websocket": URLRouter(game.routing.websocket_urlpatterns),  # WebSockets
})
