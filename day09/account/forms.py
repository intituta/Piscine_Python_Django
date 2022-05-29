from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)
