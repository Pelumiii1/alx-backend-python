from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    
    def __str__(self):
        return self.username


class Conversation(models.Model):
  participate = models.ManyToManyField(User, related_name="conversations")
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender} in {self.conversation}"
    