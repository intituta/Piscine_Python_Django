from django.urls import reverse_lazy
from django.contrib import messages
from django.http.response import HttpResponse
from django.views.generic import FormView
from ex.forms.user import UserLoginFrom


class LoginView(FormView):
    template_name = 'ex/pages/login.html'
    form_class = UserLoginFrom
    success_url = reverse_lazy('ex:main')

    def get_success_url(self) -> str:
        next = self.request.GET.get('next', None)
        if next is not None:
            return next
        return self.success_url

    def form_valid(self, form: UserLoginFrom) -> HttpResponse:
        try:
            form.login(self.request)
            messages.success(self.request, "Login Success!")
        except UserLoginFrom.AuthFail:
            messages.error(self.request, "Login Fail..!")
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form: UserLoginFrom) -> HttpResponse:
        messages.error(self.request, "Login Fail..!")
        return super().form_invalid(form)
