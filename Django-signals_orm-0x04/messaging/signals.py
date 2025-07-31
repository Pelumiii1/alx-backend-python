from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message,Notification


@receiver(post_save, sender=Message)
def send_notification(sender, instance,created,**kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance, content=f"New message from {instance.sender}:{instance.content}")