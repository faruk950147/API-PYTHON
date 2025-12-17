from rest_framework.views import APIView
from rest_framework.response import Response


class UrlsView(APIView):
    def get(self, request):
        return Response({
            "status": "success",
            "message": "Admission API endpoints available",
            "endpoints": {
                "get_urls": "GET /api/urls/",
                "register": "POST /api/registration/"
            }
        })
    
class RegistrationView(APIView):
    def post(self, request):
        return Response({
            "status": "success",
            "message": "Admission registration successful"
        })
