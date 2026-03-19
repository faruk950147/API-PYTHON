from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from official.models import Author, Tag, Post, Comment
from official.serializers import AuthorSerializer, TagSerializer, CommentSerializer, PostSerializer

# API Root
class APIRootView(viewsets.ViewSet):
    """
    API Root: Main entry point
    """
    def list(self, request):
        return Response({
            'authors': reverse('author-list', request=request),
            'tags': reverse('tag-list', request=request),
            'posts': reverse('post-list', request=request),
            'comments': reverse('comment-list', request=request),
        })


# Individual Model ViewSets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer