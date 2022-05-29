from django.db import models
from django.conf import settings


class PostModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(null=False)
    creationDate = models.DateTimeField(auto_now_add=True, null=False)
    updateDate = models.DateTimeField(auto_now=True, null=False)
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        ordering = ('creationDate',)

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.filter(parent=None, is_active=True)
