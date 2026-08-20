import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mktechsolutions.settings')

# 'application' is the standard Django name
# 'app' is the name Vercel's @vercel/python runtime looks for
application = get_wsgi_application()
app = application
