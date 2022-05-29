from django.views.generic.base import RedirectView
from ex.models.post import PostModel
from django import http
from ex.models.comment import CommentModel
from typing import Any, Dict, Optional
from django.contrib import messages
from django.http.response import HttpResponse, Http404, HttpResponseBase
from django.urls.base import reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from ex.forms import CommentForm


class PostCheckMixin:
    def dispatch(self, request: http.HttpRequest, post_id,  *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            post: PostModel = PostModel.objects.get(id=post_id)
        except PostModel.DoesNotExist:
            raise Http404()
        self.instance = post
        return super().dispatch(request, post_id, *args, **kwargs)


class CommentView(LoginRequiredMixin, PostCheckMixin, FormView):
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse('ex:post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

    def get(self, *args, **kwargs):
        raise Http404

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        return initial

    def form_valid(self, form: CommentForm) -> HttpResponse:
        comment: CommentModel = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.instance
        if form.cleaned_data['parent']:
            try:
                parent = CommentModel.objects.get(id=form.cleaned_data['parent'])
                comment.parent = parent
            except CommentModel.DoesNotExist:
                pass
        comment.save()
        return super().form_valid(form)

    def form_invalid(self, form: CommentForm) -> HttpResponse:
        return super().form_invalid(form)


class CommentDeleteView(LoginRequiredMixin, PostCheckMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse('ex:post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        comment_id = self.kwargs.get('comment_id')
        try:
            comment:CommentModel = CommentModel.objects.get(id=comment_id)
            comment.is_active = False
            comment.save()
        except CommentModel.DoesNotExist:
            raise Http404()
        messages.info(request, "Delete Comment success!")
        return super().get(request, *args, **kwargs)
