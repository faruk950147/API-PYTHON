from rest_framework.views import APIView
from rest_framework.response import Response


class AddmissionUrlsView(APIView):
    def get(self, request):
        return Response({
            "All addmissions url": "GET /api/addmissions/"
        })
    
class AddmissionDetailView(APIView):
    def post(self, request):
        return Response({
        })
