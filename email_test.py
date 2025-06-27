import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candidate_management.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email sent from Django.',
    'testingbasava8431@gmail.com',  # From
    ['your-other-email@gmail.com'],  # To — use your own email here
    fail_silently=False,
)
