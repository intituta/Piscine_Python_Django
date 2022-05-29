from typing import Any
from django import http
from django.urls import reverse_lazy
from django.contrib import messages
from django.http.response import HttpResponseBase
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('ex:main')
    login_url = reverse_lazy('ex:login')

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        logout(request)
        messages.success(request, "Logout Success!")
        return super().get(request, *args, **kwargs)
