from ex.models.post import PostModel
from typing import Any, Dict
from django import http
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.urls.base import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from ex.models import User
from ex.forms import ProfileForm


class ProfileUserCheckMixin:
    def dispatch(self, request: http.HttpRequest, user_id,  *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            user: User = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404()
        self.instance = user
        if user != request.user and not request.user.is_staff:
            messages.error(request, "permission denied")
            return redirect('ex:main')
        return super().dispatch(request, user_id, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'profile_user'
    template_name = 'ex/pages/profile/profile.html'
    login_url = reverse_lazy('ex:login')
    model = User
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = context['object']
        posts = PostModel.objects.filter(
            is_active=True, author=user).order_by('-id')[:10]
        context['posts'] = posts
        return context


class ProfileEditView(LoginRequiredMixin, ProfileUserCheckMixin, FormView):
    context_object_name = 'profile_user'
    template_name = 'ex/pages/profile/edit.html'
    login_url = reverse_lazy('ex:login:edit')
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('ex:profile-detail',
                       kwargs={'user_id': self.kwargs.get('user_id')})

    def get_initial(self):
        profile = self.instance
        initial = super().get_initial()
        initial['name'] = profile.name
        initial['surname'] = profile.surname
        initial['email'] = profile.email
        initial['profile_image'] = profile.profile_image
        initial['description'] = profile.description
        return initial

    def form_valid(self, form):
        self.instance.name = form.cleaned_data['name']
        self.instance.surname = form.cleaned_data['surname']
        self.instance.profile_image = form.cleaned_data['profile_image']
        self.instance.description = form.cleaned_data['description']

        email = form.cleaned_data['email']
        if self.instance.email != email:
            try:
                User.objects.get(email=email)
                form.errors['email'] = ("email error", )
                return self.form_invalid(form)
            except User.DoesNotExist:
                pass
        self.instance.email = email
        self.instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
