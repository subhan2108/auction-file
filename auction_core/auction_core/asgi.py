import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ✅ Set the settings module before importing anything Django-related
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_core.settings')

# ✅ Setup Django
django.setup()  # 👈 THIS LINE IS IMPORTANT to load apps properly

# ✅ Import AFTER setup
from django.core.asgi import get_asgi_application
import auctions.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            auctions.routing.websocket_urlpatterns
        )
    ),
})
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ✅ Set the settings module before importing anything Django-related
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_core.settings')

# ✅ Setup Django
django.setup()  # 👈 THIS LINE IS IMPORTANT to load apps properly

# ✅ Import AFTER setup
from django.core.asgi import get_asgi_application
import auctions.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            auctions.routing.websocket_urlpatterns
        )
    ),
})
