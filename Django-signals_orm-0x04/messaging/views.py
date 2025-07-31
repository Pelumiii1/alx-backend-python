from django.shortcuts import render
from rest_framework.generics import DestroyAPIView

# Create your views here.


class DeleteUserView(DestroyAPIView):
    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        instance.delete()