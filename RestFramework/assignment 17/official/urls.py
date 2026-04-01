from django.urls import path
from official.views import (
    PostList,
)

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
]