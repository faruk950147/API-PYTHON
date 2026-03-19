from django.urls import path, include
from rest_framework.routers import DefaultRouter
from official.views import APIRootView, AuthorViewSet, TagViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', APIRootView.as_view({'get': 'list'}), name='api-root'),
    path('', include(router.urls)),
]