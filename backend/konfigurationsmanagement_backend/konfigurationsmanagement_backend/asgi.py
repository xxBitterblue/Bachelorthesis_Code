"""
ASGI config for konfigurationsmanagement_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import authentication.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'konfigurationsmanagement_backend.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
          authentication.routing.websocket_urlpatterns
        )
    ),
})
