from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import froms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render


# Create your views here.

class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPost(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("post").get(username__iexact=self.kwargs.get("username"))

        except User.DoesNotExist:
            raise Http404
        else:
            self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )
