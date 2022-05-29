from django.db import models
from django.conf import settings
from ex.models.post import PostModel


class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id', related_name='comments')
    comment = models.CharField(
        max_length=512, null=False)
    creationDate = models.DateTimeField(
        auto_now_add=True, null=False)
    updateDate = models.DateTimeField(
        auto_now=True, null=False)

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('creationDate',)

    def __str__(self):
        return self.comment

    def get_comments(self):
        return CommentModel.objects.filter(parent=self, is_active=True)

    def get_replayform(self):
        from ex.forms.comment import CommentForm
        form = CommentForm()
        form.fields['parent'].initial = self.id
        return form
