from typing import Any, Dict
from django import http
from django.contrib import messages
from django.http.response import Http404, HttpResponse, HttpResponseBase
from django.urls.base import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from ex.models import PostModel
from ex.forms import PostForm, CommentForm


class PostUserCheckMixin:
    def dispatch(self, request: http.HttpRequest, post_id,  *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            post: PostModel = PostModel.objects.get(id=post_id)
        except PostModel.DoesNotExist:
            raise Http404()
        if post.author != request.user and not request.user.is_staff:
            messages.error(request, "permission denied")
            return redirect('ex:main')
        self.instance = post
        return super().dispatch(request, post_id, *args, **kwargs)


class PostView(LoginRequiredMixin, FormView):
    template_name = 'ex/pages/post/new.html'
    form_class = PostForm
    login_url = reverse_lazy('ex:login')

    def get_success_url(self) -> str:
        return reverse('ex:post-detail', args=[self.instance.id])

    def form_valid(self, form: PostForm) -> HttpResponse:
        post: PostModel = form.save(commit=False)
        post.author = self.request.user
        post.save()
        self.instance = post
        messages.success(self.request, 'Create post success!')
        return super().form_valid(form)

    def form_invalid(self, form: PostForm) -> HttpResponse:
        return super().form_invalid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ex/pages/post/post.html'
    login_url = reverse_lazy('ex:login')
    model = PostModel
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post: PostModel = context['object']
        if post.is_active == False:
            raise Http404()
        context["comment_form"] = CommentForm()
        return context


class PostEditView(LoginRequiredMixin, PostUserCheckMixin, FormView):
    template_name = 'ex/pages/post/edit.html'
    form_class = PostForm
    login_url = reverse_lazy('ex:login')

    def get_success_url(self) -> str:
        return reverse('ex:post-detail',
                       kwargs={'post_id': self.kwargs.get('post_id')})

    def get_initial(self) -> Dict[str, Any]:
        post: PostModel = self.instance
        initial = super().get_initial()
        initial['title'] = post.title
        initial['content'] = post.content
        return initial

    def form_valid(self, form: PostForm) -> HttpResponse:
        self.instance.title = form.cleaned_data['title']
        self.instance.content = form.cleaned_data['content']
        self.instance.save()
        return super().form_valid(form)

    def form_invalid(self, form: PostForm) -> HttpResponse:
        return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, PostUserCheckMixin, RedirectView):
    url = reverse_lazy('ex:main')

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        self.instance.is_active = False
        for comment in self.instance.get_comments():
            comment.is_active = False
            comment.save()
        self.instance.save()
        messages.info(request, "Delete post success!")
        return super().get(request, *args, **kwargs)
