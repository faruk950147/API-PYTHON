from rest_framework.views import APIView
from rest_framework.response import Response
from admission.models import Student
from admission.serializers import StudentSerializer

class UrlsView(APIView):
    def get(self, request):
        return Response({
            "status": "success",
            "message": "Admission API endpoints available",
            "endpoints": {
                "root": "http://127.0.0.1:8000/",
            }
        })
    

class StudentAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

 

