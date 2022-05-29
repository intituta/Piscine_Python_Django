from email import message
from django.db import models
from django.contrib.auth.models import User


class ChatsName(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

class ChatsMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(ChatsName, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

# Create your models here.
