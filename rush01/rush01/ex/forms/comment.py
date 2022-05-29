from django import forms
from ex.models.comment import CommentModel

class CommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = CommentModel
        fields = ['comment',]
