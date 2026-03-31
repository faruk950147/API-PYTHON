from rest_framework.views import APIView
from rest_framework.response import Response
from official.models import Post
from official.serializers import PostSerializer

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)