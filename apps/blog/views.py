from django.core.mail import send_mail
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404

from environs import Env

from .models import Post
from .forms import EmailPostForm

env = Env()
env.read_env()


def post_list(request):
    posts = Post.published.all()
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "post_detail.html", {"post": post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "post_list.html"


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.methos == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, env.str("EMAIL_HOST_USER"), [cd["to"]])

            sent = True

    else:
        form = EmailPostForm()
    return render(
        request, "post_share.html", {"post": post, "form": form, "sent": sent}
    )
