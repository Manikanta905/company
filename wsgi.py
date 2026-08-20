import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mktechsolutions.settings')

# Vercel looks for either 'application' (Django standard) or 'app'
application = get_wsgi_application()
app = application
