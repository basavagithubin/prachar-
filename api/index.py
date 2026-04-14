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

# Export WSGI application for Vercel
app = get_wsgi_application()

# For compatibility
application = app

