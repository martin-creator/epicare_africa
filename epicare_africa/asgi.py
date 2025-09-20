"""
ASGI config for epicare_africa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'epicare_africa.settings')

application = get_asgi_application()

# pws: oALQ1tAB5XcCnqYR
# db_name: epicarea_production
# db_user: epicarea_epicare_admin