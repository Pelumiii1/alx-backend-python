from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_notification(recipient_email, subject, message):
    """Sends an email notification."""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,   
    )
