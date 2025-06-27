# core/utils.py

from django.core.mail import send_mass_mail
from django.conf import settings
import logging

# Use Django's logger

from django.core.mail import send_mass_mail

def send_bulk_email(subject, message, recipient_list):
    if not recipient_list:
        return

    messages = [
        (subject, message, 'testingbasava8431@gmail.com', [recipient])
        for recipient in recipient_list
    ]

    try:
        send_mass_mail(messages, fail_silently=False)
        print("✅ Emails sent successfully.")
    except Exception as e:
        print(f"❌ Error sending emails: {e}")


def send_bulk_sms(message, phone_numbers):
    for number in phone_numbers:
        print(f"Sending SMS to {number}: {message}")  # Replace this with actual SMS API logic
from datetime import date
from .models import Candidate, FollowUpSession

def update_today_follow_up_session():
    today = date.today()

    # Get or create today's session
    session, _ = FollowUpSession.objects.get_or_create(date=today, defaults={'speaker_name': 'N/A'})

    # Update today's stats
    session.candidates_followed_up = Candidate.objects.filter(
        followed_up=True, follow_up_status_date=today, deleted=False
    ).count()

    session.candidates_attended = Candidate.objects.filter(
        attended=True, follow_up_status_date=today, deleted=False
    ).count()

    session.candidates_newly_registered = Candidate.objects.filter(
        registration_date=today, deleted=False
    ).count()

    session.followed_up_but_not_attended = Candidate.objects.filter(
        followed_up=True, attended=False, follow_up_status_date=today, deleted=False
    ).count()

    session.save()
