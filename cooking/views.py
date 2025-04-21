from django.shortcuts import render
from .models import Category, Post


def index(request):
    """Для главной странички"""
    posts = Post.objects.all()  # SELECT * FROM Post
    categories = Category.objects.all()  # SELECT * FROM Category
    context = {
        'title': 'Главная страница',
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'cooking/index.html', context)
