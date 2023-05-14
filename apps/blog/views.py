from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, "post_detail.html", {"post": post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "post_list.html"
