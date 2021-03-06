"""
WSGI config for ripple project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from ripple.load_env import init_env

init_env('../.env.current')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ripple.settings")

application = get_wsgi_application()
