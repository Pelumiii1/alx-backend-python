from django.db import models
from django.db.models import Q

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(receiver=user).exclude(read_receipts__user=user)
