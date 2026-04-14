import sys
from pathlib import Path

# Add the parent directory to the path so we can import our Django project
sys.path.insert(0, str(Path(__file__).parent.parent))

from candidate_management.wsgi import application

# Export the application for Vercel
def handler(request):
    """Handler for Vercel serverless functions"""
    return application(request)
