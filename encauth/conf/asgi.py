"""
Standard asgi entry point for the django application
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encauth.conf.settings')
application = get_asgi_application()
