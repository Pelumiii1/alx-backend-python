from django.shortcuts import render
from rest_framework.generics import DestroyAPIView
from .models import Message
from django.db.models import Prefetch
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
        

def get_threaded_messages(message_id):
    messages = Message.objects.prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).select_related('sender', 'receiver').filter(parent_message__isnull=True)



    return messages