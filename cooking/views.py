from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Category, Post, Comment
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentAddForm
from .mixins import SuccessMessageMixin
from .serializers import PostSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


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


class PostDetail(SuccessMessageMixin, DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Перегружаем метод для фильтрации"""
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Перегружаем метод для динамических данных"""
        context = super().get_context_data()
        post = self.object
        post.increment_views()

        context['title'] = post.title
        context['post'] = post
        context['comments'] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentAddForm()
        return context


# def add_post(request):
#     """Добавление статьи от пользователя"""
#     if request.method == 'POST':
#         form = PostAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save()
#             messages.success(request, 'Вы успешно создали статью!')
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostAddForm()
#     context = {
#         'form': form,
#         'title': 'Добавить статью',
#
#     }
#     return render(request, 'cooking/article_add_form.html', context)


class AddPost(SuccessMessageMixin, CreateView):
    """Добавление статьи от пользователя"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Добавить статью'}
    success_message = 'Вы успешно создали статью!'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Вот где присваивается автор
        return super().form_valid(form)


class UpdatePost(SuccessMessageMixin, UpdateView):
    """Изменение статьи по кнопке"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Изменить статью'}
    success_message = 'Вы успешно изменили статью!'


class DeletePost(SuccessMessageMixin, DeleteView):
    """Удаление статьи по кнопке"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'
    success_message = 'Вы успешно удалили статью!'


class SearchResult(Index):
    """Поиск в заголовках и содержании статей"""

    def get_queryset(self):
        """Функция фильтрации выборок из базы"""
        word = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


def add_comment(request, post_id):
    """Добавление комментария к посту"""
    form = CommentAddForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = Post.objects.get(pk=post_id)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен!')

    return redirect('post_detail', pk=post_id)


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


def user_profile(request, user_id: int):
    """Функция отображения странички пользователя"""
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'title': f'Страница пользователя {user.username}',
        'user': user,
        'posts': posts,
    }
    return render(request, 'cooking/user_profile.html', context)


class UserChangePassword(SuccessMessageMixin, PasswordChangeView):
    """Смена пароля пользователя"""
    template_name = 'cooking/password_change_form.html'
    success_message = 'Пароль успешно изменён'
    success_url = reverse_lazy('index')


class CookingAPI(ListAPIView):
    """Выдача всех статей по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingAPIDetail(RetrieveAPIView):
    """Выдача статьи по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class CookingCategoryAPI(ListAPIView):
    """Выдача всех категорий по API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CookingCategoryAPIDetail(RetrieveAPIView):
    """Выдача категории по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializer


