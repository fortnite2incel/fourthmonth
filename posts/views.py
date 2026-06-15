from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
 
from posts.forms import CategoryModelForm, PostModelForm
from posts.models import Category, Post
 

# Create your views here.


def home(request: HttpRequest):
    return render(request, "base.html")


def about(request: HttpRequest):

    return render(request, "about.html")


def me(request: HttpRequest):

    return HttpResponse("<h1>ITS TEST!</h1>")


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
 
    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
 
    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

# def get_posts(request: HttpRequest):
#     posts = Post.objects.all()

#     return render(request, "posts/post_list.html", context={"posts": posts})




# def get_post(request: HttpRequest, pk: int):
#     post = Post.objects.get(id=pk)
#     return render(request, "posts/post_detail.html", context={"post": post})

@login_required
def create_post(request: HttpRequest) -> HttpResponse:
    form = PostModelForm()
 
    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.rate = 5
            post.save()
            return redirect("post_list")
        return render(request, "posts/create_post.html", {"form": form, "errors": form.errors})
 
    return render(request, "posts/create_post.html", {"form": form})
 

@login_required
def create_category(request: HttpRequest) -> HttpResponse:
    form = CategoryModelForm()
 
    if request.method == "POST":
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_list")
        return render(request, "posts/create_category.html", {"form": form, "errors": form.errors})
 
    return render(request, "posts/create_category.html", {"form": form})

class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/my_posts.html"
    context_object_name = "posts"
 
    def get_queryset(self): 
        return Post.objects.filter(user=self.request.user)
 
 
@login_required
def edit_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if post.user != request.user:
        return HttpResponse("Forbidden: you are not the author of this post.", status=403)
 
    form = PostModelForm(instance=post)
 
    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
 
    return render(request, "posts/edit_post.html", {"form": form, "post": post})
 
 
@login_required
def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
 
    if post.user != request.user:
        return HttpResponse("Forbidden: you are not the author of this post.", status=403)
 
    if request.method == "POST":
        post.delete()
        return redirect("my_posts")
 
    return render(request, "posts/delete_post.html", {"post": post})
 
