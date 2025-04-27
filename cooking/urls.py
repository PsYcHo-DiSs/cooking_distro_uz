from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', posts_by_category, name='posts_by_category'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('add_article/', add_post, name='add'),
]
