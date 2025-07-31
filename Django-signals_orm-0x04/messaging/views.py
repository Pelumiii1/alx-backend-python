from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, RetrieveAPIView, ListAPIView
from .models import Message
from django.db.models import Prefetch, Q
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer

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

class ThreadedMessageView(RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(parent_message__isnull=True) & (Q(sender=user) | Q(receiver=user))
        ).prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').prefetch_related(
                Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
            ))
        ).select_related('sender', 'receiver')

class UnreadMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.unread.filter(receiver=self.request.user).only('sender', 'content', 'timestamp')
        
