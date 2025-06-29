from django import template
from cooking.models import Category, Post
from django.core.cache import cache
from django.db.models import Count, Q

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Получение всех категорий"""
    cat_buttons = cache.get('categories')
    if not cat_buttons:
        categories = Category.objects.annotate(cnt=Count('posts', filter=Q(posts__is_published=True))).filter(cnt__gt=0)
        cache.set('categories', categories, 60)
    return cat_buttons


@register.simple_tag()
def get_top_5_posts():
    """Получение топа статей с кэшированием"""
    top_5_posts = cache.get('top_5_posts')
    if not top_5_posts:
        top_5_posts = Post.objects.filter(is_published=True).order_by('-watched')[:5]
        cache.set('top_5_posts', top_5_posts, 60)
    return top_5_posts
