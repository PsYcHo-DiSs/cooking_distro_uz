from django.shortcuts import render
from .models import Category, Post
from django.db.models import F


def index(request):
    """Для главной странички"""
    posts = Post.objects.all()  # SELECT * FROM Post
    # categories = Category.objects.all()
    context = {
        'title': 'Главная страница',
        'posts': posts,
        # 'category': categories
    }
    return render(request, 'cooking/index.html', context)


def posts_by_category(request, pk: int):
    """Возврат ответа на нажатие кнопок категорий"""
    # categories = Category.objects.all()
    filtered_posts = Post.objects.filter(category_id=pk)  # returns QuerySet
    context = {
        'title': filtered_posts[0].category,
        'posts': filtered_posts,
        # 'categories': categories
    }
    return render(request, 'cooking/index.html', context)


def post_detail(request, pk: int):
    """Страница статьи"""
    post = Post.objects.filter(pk=pk)
    post.update(watched=F('watched') + 1)
    context = {
        'title': post[0].title,
        'post': post[0]
    }
    return render(request, 'cooking/article_detail.html', context)
