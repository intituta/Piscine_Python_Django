from django import forms


class PostForm(forms.Form):
    text = forms.CharField(label='input text', max_length=200)
