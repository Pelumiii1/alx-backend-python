from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status, filters
from .models import User, Conversation, Message
from .serializers import  ConversationSerializer,MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes= [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user])


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']


    def get_queryset(self):
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__pk=conversation_pk, conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_pk = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_pk)
        serializer.save(sender=self.request.user, conversation=conversation)

