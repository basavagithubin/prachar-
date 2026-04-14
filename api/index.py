import sys
import os
from pathlib import Path

# Add the parent directory to the path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candidate_management.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.http import HttpRequest, HttpResponse

# Get the WSGI application
wsgi_app = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler for Django.
    Converts Vercel's request format to WSGI format.
    """
    # Import here to avoid import errors before Django setup
    from asgiref.wsgi import WsgiToAsgi
    
    # Convert WSGI to ASGI for better compatibility
    asgi_app = WsgiToAsgi(wsgi_app)
    
    # Return the WSGI app result
    return wsgi_app

