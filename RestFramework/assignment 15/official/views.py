from rest_framework import generics
from official.models import Post
from official.serializers import PostSerializer

# CreateAPIView
class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # new post author automatically assign
        serializer.save(author=self.request.user)


# ListAPIView
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# RetrieveAPIView
class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# UpdateAPIView
class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        # Optional: extra update logic
        serializer.save()


# DestroyAPIView
class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_destroy(self, instance):
        # Optional: soft delete
        # instance.is_deleted = True
        # instance.save()
        instance.delete()