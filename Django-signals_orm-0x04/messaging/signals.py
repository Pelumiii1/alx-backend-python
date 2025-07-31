from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete
from .models import Message,Notification,MessageHistory
from django.contrib.auth.models import User
from django.utils import timezone


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
                instance.edited = True
                instance.edited_at = timezone.now()
                instance.edited_by = instance.sender
                MessageHistory.objects.create(message=instance,old_content=old_message.content)
        except Message.DoesNotExist:
            pass
        
@receiver(post_delete, sender=User)
def delete_user_messages(sender,instance,**kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()