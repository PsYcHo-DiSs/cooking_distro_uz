from django.shortcuts import render, redirect
from .models import Category, Post
from .forms import PostAddForm


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
    post = Post.objects.get(pk=pk)
    post.increment_views()
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'cooking/article_detail.html', context)


def add_post(request):
    """Добавление статьи от пользователя"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('post_detail', pk=post.pk)

    form = PostAddForm()
    context = {
        'form': form,
        'title': 'Добавить статью',

    }
    return render(request, 'cooking/article_add_form.html', context)
