from django import template
from cooking.models import Category, Post

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Получение всех категорий"""
    return Category.objects.all()


# @register.simple_tag()
# def get_all_posts():
#     """Получение всех постов"""
#     return Post.objects.all()
