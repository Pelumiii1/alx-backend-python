from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True,blank=True)
    edited_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='edited_messages',null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    
    objects = models.Manager()  # The default manager.
    unread = UnreadMessagesManager()  # The custom manager.

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    

class MessageHistory(models.Model):
    old_content = models.TextField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE,related_name="history")  
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for message {self.message.id}"
     

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)    
    

    