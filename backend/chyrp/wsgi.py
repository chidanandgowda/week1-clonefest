"""
WSGI config for chyrp project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chyrp.settings')

application = get_wsgi_application()
