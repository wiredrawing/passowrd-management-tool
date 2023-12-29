"""
WSGI config for microblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from wsgi_basic_auth import BasicAuth
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'microblog.settings')

# basic認証でラップする
# application = get_wsgi_application()

application = BasicAuth(get_wsgi_application())
