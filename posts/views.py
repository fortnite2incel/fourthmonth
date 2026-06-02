from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import JsonResponse
from posts.models import Post
from .models import Category
# Create your views here.

def hello_world(request):

    return HttpResponse("Hello World!")

def about(request):

    return render(request, "about.html")

def post(request):
    posts = Post.objects.all()

    text = ""
    
    for post in posts:

        text += f"<h1> {post.title} <h1> <br> {post.content}<br>"
    
    return HttpResponse(text)

def actvie_categories(request):
    categories = Category.objects.filter(is_active=True)

    data = []
    for category in categories:
        data.append(
            {
                "id": category.id,
                "title": category.title, 
                "description": category.description,
                "is_active": category.is_active
            }
        )
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
