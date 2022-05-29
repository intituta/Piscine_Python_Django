from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.contrib.auth import login, authenticate, password_validation
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
from django.http.request import HttpRequest
from django.utils.translation import gettext, gettext_lazy as _

from ex.models import User


class UserLoginFrom(forms.Form):
    id = forms.CharField()
    password = forms.CharField(widget=PasswordInput)

    class AuthFail(Exception):
        def __str__(self) -> str:
            return 'authenticate fail'

    def login(self, request: HttpRequest):
        id = self.cleaned_data['id']
        password = self.cleaned_data['password']
        user = authenticate(
            request=request,
            id=id,
            password=password,
        )
        if user is None:
            raise self.AuthFail()
        return login(request, user)


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('id', 'email')
        field_classes = {'id': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'surname', 'description',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
