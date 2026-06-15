from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from users.form import UserForm


def register_user(request: HttpRequest):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                user = User(email=form.cleaned_data["email"])
                raw_password = form.cleaned_data["password"]

                user.set_password(raw_password)
                user.save()
                login(request, user)
                return redirect("posts")
        except IntegrityError:
            form.add_error("email", "Пользователь с таким email уже существует!")
    return render(request, "users/register.html", context={"form": form})
