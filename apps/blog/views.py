from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, "post_detail.html", {"post": post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "post_list.html"
