# Django built-in response class
from django.http import HttpResponse

# DRF core classes
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

# Your Model and Serializer
from official.models import Post
from official.serializers import PostSerializer


class PostAPIView(APIView):
    def get(self, request):
        # Fetch all posts from the database
        posts = Post.objects.all()

        # Debug: print queryset in console
        print(f'Queryset: {posts}')

        # Convert queryset to Python dict using serializer
        serializer = PostSerializer(posts, many=True)

        # Debug: print serialized data
        print(f'Serialized Data: {serializer.data}')

        # Convert Python dict to JSON
        json_data = JSONRenderer().render(serializer.data)

        # Return JSON response to client
        return HttpResponse(
            json_data,
            content_type='application/json'
        )
    def post(self, request):

        # Get incoming data from client
        serializer = PostSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():

            # Save valid data to database
            serializer.save()

            # Convert saved data to JSON
            json_data = JSONRenderer().render(serializer.data)

            # Return success response (201 Created)
            return HttpResponse(
                json_data,
                content_type='application/json',
                status=201
            )

        # If validation fails, return errors
        json_data = JSONRenderer().render(serializer.errors)

        return HttpResponse(
            json_data,
            content_type='application/json',
            status=400
        )