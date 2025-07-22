from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass

class Conversation(models.Model):
  participants = models.ManyToManyField(User, related_name="conversations")
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message {self.id} from {self.sender} in {self.conversation}"
    