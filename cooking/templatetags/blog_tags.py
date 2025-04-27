from django import template
from cooking.models import Category, Post
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Получение всех категорий"""
    return Category.objects.all()


@register.simple_tag()
def get_top_5_posts():
    """Получение топа статей с кэшированием"""
    top_5_posts = cache.get('top_5_posts')
    if not top_5_posts:
        top_5_posts = Post.objects.filter(is_published=True).order_by('-watched')[:5]
        cache.set('top_5_posts', top_5_posts, 60)
    return top_5_posts


# @register.simple_tag()
# def get_all_posts():
#     """Получение всех постов"""
#     return Post.objects.all()
