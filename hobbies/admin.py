from django.contrib import admin

from django.contrib import admin
from .models import Category, Post, Comment, Like

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')  
    return render(request, 'hobbies/home.html', {'posts': posts})

