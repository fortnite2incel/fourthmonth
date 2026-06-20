from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from django.shortcuts import render
from django.views.generic import DetailView, ListView, DeleteView, CreateView, UpdateView
 
from posts.forms import CategoryModelForm, PostModelForm
from posts.models import Post, Category
 

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
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Post]:
        qs = super().get_queryset()
        q = self.request.GET.get("q", None)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        return qs


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

# def get_posts(request: HttpRequest):
#     posts = Post.objects.all()

#     return render(request, "posts/post_list.html", context={"posts": posts})




# def get_post(request: HttpRequest, pk: int):
#     post = Post.objects.get(id=pk)
#     return render(request, "posts/post_detail.html", context={"post": post})

# @login_required
# def create_post(request: HttpRequest) -> HttpResponse:
#     form = PostModelForm()
 
#     if request.method == "POST":
#         form = PostModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.rate = 5
#             post.save()
#             return redirect("posts")
#         return render(request, "post/create_post.html", {"form": form, "errors": form.errors})
 
#     return render(request, "post/create_post.html", {"form": form})
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("posts")

    # Метод для автоматической привязки автора и рейтинга перед сохранением
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rate = 5
        return super().form_valid(form)

# @login_required
# def create_category(request: HttpRequest) -> HttpResponse:
#     form = CategoryModelForm()
 
#     if request.method == "POST":
#         form = CategoryModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("posts")
#         return render(request, "posts/create_category.html", {"form": form, "errors": form.errors})
 
#     return render(request, "posts/create_category.html", {"form": form})

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category  
    form_class = CategoryModelForm
    template_name = "posts/create_category.html"
    success_url = reverse_lazy("posts")

class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/my_posts.html"
    context_object_name = "posts"
 
    def get_queryset(self): 
        return Post.objects.filter(user=self.request.user)
 
 
# @login_required
# def edit_post(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)

#     if post.user != request.user:
#         return HttpResponse("Forbidden: you are not the author of this post.", status=403)
 
#     form = PostModelForm(instance=post)
 
#     if request.method == "POST":
#         form = PostModelForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect("my_posts")
 
#     return render(request, "posts/edit_post.html", {"form": form, "post": post})
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = "posts/create_post.html"  
    success_url = reverse_lazy("my_posts")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором этого поста.")
        return obj

 
# @login_required
# def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     if post.user != request.user:
#         return HttpResponse("Forbidden", status=403)
#     if request.method == "POST":
#         post.delete()
#         return redirect("my_posts")
#     return render(request, "posts/delete_post.html", {"post": post})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy("my_posts")
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором этого поста.")
        return obj