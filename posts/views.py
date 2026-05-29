from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def hello_world(request):

    return HttpResponse("Hello World!")

def about(request):

    return render(request, "about.html")