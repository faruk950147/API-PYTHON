from rest_framework.views import APIView
from rest_framework.response import Response

# API Root
class APIRoot(APIView):
    """
    API Root: Main entry point for the official app
    """

    def get(self, request, format=None):
        return Response({
            'posts': reverse('post-list', request=request, format=format),
        })