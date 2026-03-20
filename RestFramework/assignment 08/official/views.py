'''
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
'''
""" 
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

# ================= API ROOT =================
class APIRootView(viewsets.ViewSet):
    def list(self, request):
        return Response({
            'authors': reverse('author-list', request=request),
            'tags': reverse('tag-list', request=request),
            'posts': reverse('post-list', request=request),
            'comments': reverse('comment-list', request=request),
        })

# ================= Author =================
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

# ================= Tag =================
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

# ================= Post =================
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

    # Custom: post -> all comments
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": True,
            "message": f"All Comments for Post {pk}",
            "data": serializer.data
        })

    # Custom: post -> specific comment
    @action(detail=True, methods=['get'], url_path='comments/(?P<comment_id>[^/.]+)')
    def comment_detail(self, request, pk=None, comment_id=None):
        post = Post.objects.get(pk=pk)
        comment = post.comment_set.get(pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response({
            "status": True,
            "message": f"Comment {comment_id} for Post {pk}",
            "data": serializer.data
        })

# ================= Comment =================
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Retrieve single comment
    def retrieve(self, request, pk=None):
        obj = Comment.objects.get(pk=pk)
        serializer = self.get_serializer(obj)
        return Response({
            "status": True,
            "message": "Comment Details",
            "data": serializer.data
        })

    # Custom: all comments for a specific post
    @action(detail=False, methods=['get'], url_path='post/(?P<post_id>[^/.]+)')
    def post_comments(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": True,
            "message": f"Comments for Post {post_id}",
            "data": serializer.data
        }) 
"""

from rest_framework import viewsets, status
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

# ================= API ROOT =================
class APIRootView(viewsets.ViewSet):
    def list(self, request):
        return Response({
            'authors': reverse('author-list', request=request),
            'tags': reverse('tag-list', request=request),
            'posts': reverse('post-list', request=request),
            'comments': reverse('comment-list', request=request),
        })


# ================= Author =================
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # perform_create
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '').capitalize()
        serializer.save(name=name)

    # Custom create response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "status": True,
            "message": "Author Created Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response({
            "status": True,
            "message": "Author Details",
            "data": serializer.data
        })


# ================= Tag =================
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '').lower()
        serializer.save(name=name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "status": True,
            "message": "Tag Created Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response({
            "status": True,
            "message": "Tag Details",
            "data": serializer.data
        })


# ================= Post =================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title', '').capitalize()
        serializer.save(author=self.request.user, title=title)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "status": True,
            "message": "Post Created Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response({
            "status": True,
            "message": "Post Details",
            "data": serializer.data
        })

    # All comments of a post
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)

        return Response({
            "status": True,
            "message": f"All Comments for Post {pk}",
            "data": serializer.data
        })

    # Specific comment
    @action(detail=True, methods=['get'], url_path='comments/(?P<comment_id>[^/.]+)')
    def comment_detail(self, request, pk=None, comment_id=None):
        post = self.get_object()
        comment = post.comment_set.get(pk=comment_id)
        serializer = CommentSerializer(comment)

        return Response({
            "status": True,
            "message": f"Comment {comment_id} for Post {pk}",
            "data": serializer.data
        })


# ================= Comment =================
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        text = serializer.validated_data.get('text', '').strip()
        serializer.save(user=self.request.user, text=text)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "status": True,
            "message": "Comment Created Successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)

        return Response({
            "status": True,
            "message": "Comment Details",
            "data": serializer.data
        })

    # All comments for a specific post
    @action(detail=False, methods=['get'], url_path='post/(?P<post_id>[^/.]+)')
    def post_comments(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)

        return Response({
            "status": True,
            "message": f"Comments for Post {post_id}",
            "data": serializer.data
        })
        
