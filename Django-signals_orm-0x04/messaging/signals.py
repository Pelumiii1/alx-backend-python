from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import Message,Notification,MessageHistory


@receiver(post_save, sender=Message)
def send_notification(sender, instance,created,**kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance, content=f"New message from {instance.sender}:{instance.content}")
        
        
@receiver(pre_save, sender=Message)
def create_message_history(sender,instance,created,**kwargs):
    if instance.id:
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:
                MessageHistory.objects.create(message=instance,old_content=old_message.content)
        except Message.DoesNotExist:
            pass