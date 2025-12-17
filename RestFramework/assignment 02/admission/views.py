from rest_framework.views import APIView
from rest_framework.response import Response
from admission.models import Registration
from admission.serializers import RegistrationSerializer

class UrlsView(APIView):
    def get(self, request):
        return Response({
            "status": "success",
            "message": "Admission API endpoints available",
            "endpoints": {
                "get_urls": "http://127.0.0.1:8000/",
                "register": "http://127.0.0.1:8000/registration/"
            }
        })
    
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Admission registration successful"
            }, status=201)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=400)
