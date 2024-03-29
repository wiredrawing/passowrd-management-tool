from django.shortcuts import render

# Create your views here.
from .models import  Post
from .forms import CommentForm
from blog.forms.CommentForm import CommentForm
from django.shortcuts import redirect
def frontpage(request):
    # DBから投稿を取得
    posts = Post.objects.all()
    return render(request, "blog/frontpage.html", {"posts": posts})


def post_detail(request, slug):

    # DBから投稿を取得
    post = Post.objects.get(slug = slug)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()

            return redirect("post_detail", slug=post.slug)
    else :
        form = CommentForm()
    # return
    return render(request, "blog/post_detail.html", {
        "post": post,
        "form": form,
    })
