from django.urls import path
from django.views.decorators.cache import cache_page

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import *

urlpatterns = [
    # path('', index, name='index'),
    path('', Index.as_view(), name='index'),
    # Кэширование главной страницы на базе файловой системы
    # path('', cache_page(60 * 15)(Index.as_view()), name='index'),
    # path('category/<int:pk>/', posts_by_category, name='posts_by_category'),
    path('category/<int:pk>/', PostByCategory.as_view(), name='posts_by_category'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    # path('add_article/', add_post, name='add'),
    path('add_article/', AddPost.as_view(), name='add'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete_post'),
    path('search/', SearchResult.as_view(), name='search'),
    path('change_password/', UserChangePassword.as_view(), name='change_password'),

    path('add_comment/<int:post_id>', add_comment, name='add_comment'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/<int:user_id>', user_profile, name='profile'),

    # API
    path('posts/api/', CookingAPI.as_view(), name='CookingAPI'),
    path('posts/api/<int:pk>', CookingAPIDetail.as_view(), name='CookingAPIDetail'),
    path('categories/api/', CookingCategoryAPI.as_view(), name='CookingCategoryAPI'),
    path('categories/api/<int:pk>', CookingCategoryAPIDetail.as_view(), name='CookingCategoryAPIDetail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
