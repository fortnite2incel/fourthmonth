from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
 
 
class Tag(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self) -> str:
        return str(self.name)
 
 
class Category(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self) -> str:
        return str(self.name)
 

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField(default=5)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
 
    def __str__(self) -> str:
        name = str(self.category.name) if self.category else "-"
        return f"{self.title} -- {name}"
 
    def get_absolute_url(self) -> str:
        return reverse("post_detail", kwargs={"pk": self.pk})
 
    class Meta:
        ordering = ["-created_at"]
