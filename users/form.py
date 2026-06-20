from typing import Any

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    second_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password", "second_password"]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        raw_password = cleaned_data["password"]
        second_password = cleaned_data["second_password"]

        if raw_password != second_password:
            raise forms.ValidationError("Пароли должны совпадать!")

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()