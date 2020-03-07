from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', blog_post_list_view, name='list'),
    path('<str:slug>/', blog_post_detail_view, name='detail'),
    path('<str:slug>/edit/', blog_post_update_view),
    path('<str:slug>/delete/', blog_post_delete_view),
]
