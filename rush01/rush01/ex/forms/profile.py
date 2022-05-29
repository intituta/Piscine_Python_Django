from django import forms
from ex.models import User


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['surname', 'name', 'profile_image', 'description']
