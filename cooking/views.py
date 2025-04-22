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


def posts_by_category(request, pk: int):
    """Возврат ответа на нажатие кнопок категорий"""
    categories = Category.objects.all()
    filtered_posts = Post.objects.filter(category_id=pk)  # returns QuerySet

    context = {
        'title': filtered_posts[0].category,
        'categories': categories,
        'posts': filtered_posts,
    }
    return render(request, 'cooking/index.html', context)
