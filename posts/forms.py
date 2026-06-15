from django import forms
from posts.models import Category, Post
 
 
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Write your post here…"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
 
    def clean_content(self) -> str:
        """Validate that content has at least 50 characters."""
        content: str = self.cleaned_data.get("content", "")
        if len(content) < 50:
            raise forms.ValidationError(
                f"Content is too short ({len(content)} chars). "
                "Please write at least 50 characters."
            )
        return content
 
 
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}),
        }
 
