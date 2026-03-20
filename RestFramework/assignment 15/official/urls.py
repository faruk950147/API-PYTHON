from django.urls import path
from official.views import (
    PostCreateAPIView,
    PostListAPIView,
    PostRetrieveAPIView,
    PostUpdateAPIView,
    PostDestroyAPIView
)

urlpatterns = [
    # List all posts
    path('posts/', PostListAPIView.as_view(), name='post-list'),

    # Create new post
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),

    # Retrieve a single post
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),

    # Update a post
    path('posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),

    # Delete a post
    path('posts/<int:pk>/delete/', PostDestroyAPIView.as_view(), name='post-delete'),
]