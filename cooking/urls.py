from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    path('', Index.as_view(), name='index'),
    # path('category/<int:pk>/', posts_by_category, name='posts_by_category'),
    path('category/<int:pk>/', PostByCategory.as_view(), name='posts_by_category'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    # path('add_article/', add_post, name='add'),
    path('add_article/', AddPost.as_view(), name='add'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete_post'),
    path('search/', SearchResult.as_view(), name='search'),

    path('add_comment/<int:post_id>', add_comment, name='add_comment'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
]
