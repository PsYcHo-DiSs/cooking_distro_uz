from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', posts_by_category, name='posts_by_category'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
