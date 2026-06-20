import uuid
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from users.form import UserForm, LoginForm


def register_user(request: HttpRequest):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                user = User(email=form.cleaned_data["email"])
                user.username = str(uuid.uuid4())
                raw_password = form.cleaned_data["password"]

                user.set_password(raw_password)
                user.save()
                login(request, user)
                return redirect("posts")
        except IntegrityError as e:
            print(e)
            form.add_error("email", "Пользователь с таким email уже существует!")
    return render(request, "users/register.html", context={"form": form})


def login_user(request: HttpRequest):
    form = LoginForm()

    if request.method.lower() == "post":
        form = LoginForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.get(email=cleaned_data["email"])
            if user.check_password(cleaned_data["password"]):
                login(request, user)
                return redirect("posts")
            form.add_error("password", "Wrong password!")

    return render(request, "users/login.html", {"form": form})


def logout_user(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect("posts")