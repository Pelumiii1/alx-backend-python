from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from .models import Message
from django.db.models import Prefetch
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

def get_threaded_messages(message_id):
    messages = Message.objects.prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).select_related('sender', 'receiver').filter(parent_message__isnull=True)



    return messages