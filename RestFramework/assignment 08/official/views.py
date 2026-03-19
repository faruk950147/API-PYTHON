from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse

from official.models import Author, Tag, Post, Comment
from official.serializers import (
    AuthorSerializer,
    TagSerializer,
    PostSerializer,
    CommentSerializer
)

# API ROOT
class APIRootView(viewsets.ViewSet):
    def list(self, request):
        return Response({
            'authors': reverse('author-list', request=request),
            'tags': reverse('tag-list', request=request),
            'posts': reverse('post-list', request=request),
            'comments': reverse('comment-list', request=request),
        })


# Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, pk=None):
        obj = Author.objects.get(pk=pk)
        serializer = self.get_serializer(obj)

        return Response({
            "status": True,
            "message": "Author Details",
            "data": serializer.data
        })


# Tag
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def retrieve(self, request, pk=None):
        obj = Tag.objects.get(pk=pk)
        serializer = self.get_serializer(obj)

        return Response({
            "status": True,
            "message": "Tag Details",
            "data": serializer.data
        })


# Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, pk=None):
        obj = Post.objects.get(pk=pk)
        serializer = self.get_serializer(obj)

        return Response({
            "status": True,
            "message": "Post Details",
            "data": serializer.data
        })

    # Extra: Post → Comments
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)

        return Response({
            "status": True,
            "message": "Post Comments",
            "data": serializer.data
        })


# Comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk=None):
        obj = Comment.objects.get(pk=pk)
        serializer = self.get_serializer(obj)

        return Response({
            "status": True,
            "message": "Comment Details",
            "data": serializer.data
        })