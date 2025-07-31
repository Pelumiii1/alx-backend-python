from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, RetrieveAPIView
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

    def get_queryset(self,request):
        user = self.request.user
        return Message.objects.filter(
            sender=request.user
        ).select_related(
            'sender', 'receiver', 'conversation', 'parent_message'
        ).prefetch_related(
            'replies__sender', 'replies__receiver'
        )
        
