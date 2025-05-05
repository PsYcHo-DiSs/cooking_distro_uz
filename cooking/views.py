from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Category, Post
from .forms import PostAddForm, LoginForm, RegistrationForm
from .mixins import SuccessMessageMixin


# def index(request):
#     """Для главной странички"""
#     posts = Post.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'posts': posts,
#         # 'category': categories
#     }
#     return render(request, 'cooking/index.html', context)


class Index(ListView):
    """Для главной странички"""
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Главная страница'}


#
# def posts_by_category(request, pk: int):
#     """Возврат ответа на нажатие кнопок категорий"""
#     # categories = Category.objects.all()
#     filtered_posts = Post.objects.filter(category_id=pk)  # returns QuerySet
#     context = {
#         'title': filtered_posts[0].category,
#         'posts': filtered_posts,
#         # 'categories': categories
#     }
#     return render(request, 'cooking/index.html', context)


class PostByCategory(Index):
    """Возврат ответа на нажатие кнопок категорий"""

    def get_queryset(self):
        """Перегружаем метод для фильтрации"""
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Перегружаем метод для динамических данных"""
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


# def post_detail(request, pk: int):
#     """Страница статьи"""
#     post = Post.objects.get(pk=pk)
#     post.increment_views()
#     context = {
#         'title': post.title,
#         'post': post,
#     }
#     return render(request, 'cooking/article_detail.html', context)


class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Перегружаем метод для фильтрации"""
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Перегружаем метод для динамических данных"""
        context = super().get_context_data()
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.increment_views()
        context['title'] = post.title
        context['post'] = post
        return context


def add_post(request):
    """Добавление статьи от пользователя"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Вы успешно создали статью!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostAddForm()
    context = {
        'form': form,
        'title': 'Добавить статью',

    }
    return render(request, 'cooking/article_add_form.html', context)


class AddPost(SuccessMessageMixin, CreateView):
    """Добавление статьи от пользователя"""
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Добавить статью'}
    success_message = 'Вы успешно создали статью!'


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт!')
            return redirect('index')
    else:
        form = LoginForm()
    context = {
        'title': 'Авторизация пользователя',
        'form': form,
    }
    return render(request, 'cooking/login_form.html', context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')


def user_register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'cooking/register_form.html', context)

# def user_detail(request, pk: int):
#     """Страница пользователя"""
#     user = User.objects.filter(pk=pk)
#     if user[0]:
#         context = {
#
#         }
#         return render(request, 'cooking/profile.html', context)
