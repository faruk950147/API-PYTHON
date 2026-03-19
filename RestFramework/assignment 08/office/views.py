from rest_framework.views import APIView
from rest_framework.response import Response

# API Root
class APIRoot(APIView):
    """
    API Root: Main entry point for the office app
    """

    def get(self, request, format=None):
        return Response({
            'employees': reverse('employee-list', request=request, format=format),
        })