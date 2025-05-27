from django import template
from cooking.models import Category, Post
from django.core.cache import cache
from django.db.models import Count, Q

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Получение всех категорий"""
    # return Category.objects.all()
    # return Category.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return Category.objects.annotate(cnt=Count('posts', filter=Q(posts__is_published=True))).filter(cnt__gt=0)


@register.simple_tag()
def get_top_5_posts():
    """Получение топа статей с кэшированием"""
    top_5_posts = cache.get('top_5_posts')
    if not top_5_posts:
        top_5_posts = Post.objects.filter(is_published=True).order_by('-watched')[:5]
        cache.set('top_5_posts', top_5_posts, 60)
    return top_5_posts


@register.simple_tag()
def get_user_posts():
    """"""
