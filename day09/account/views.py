from django.shortcuts import render, reverse, HttpResponse
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect

class GetContent(FormView):

    def get(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseRedirect(reverse('index'))
        if self.request.user.is_authenticated:
            user_n = self.request.user.username
            return render(request, 'account/templates/connect.html', {"user":user_n})
        form = forms.LoginForm()
        return render(request, 'account/templates/disconnect.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_n = self.request.user.username
            return render(request, 'account/templates/connect.html', {"user":user_n})
        form = forms.LoginForm(request.POST)
        if form.is_valid():            
            u_name = form.data.get("name")
            u_pass = form.cleaned_data.get("password")
            try:
                User.objects.get(username=str(u_name))
                user = authenticate(username = u_name, password = u_pass)
                if user is not None:
                    login(request, user)
                    return self.get(request)
                else:
                    form._errors['password'] = ErrorList()
                    form._errors['password'].append("Incorrect password")
            except:
                form._errors['name'] = ErrorList()
                form._errors['name'].append("User not found")
        else:
            form = forms.LoginForm()
        return render(request, 'account/templates/disconnect.html', {'form': form})

def index(request):
    return render(request, 'account/templates/base.html')

def disconnect(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return render(request, 'account/templates/disconnect.html', {"form":forms.LoginForm()})
        else:
            user_n = request.user.username
            return render(request, 'account/templates/connect.html', {"user":user_n})
    else:
        return HttpResponseRedirect(reverse('index'))
