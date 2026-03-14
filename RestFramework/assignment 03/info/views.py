from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from info.models import Admission
from info.serializers import AdmissionSerializer

# Create your views here.
class GenericAPIView(APIView):
    def get(self, request):
        return Response({
            "status": "success",
            "endpoints": [
                "http://127.0.0.1:8000/admission-info/"
            ]
        })

class AdmissionInfoView(APIView):
    def get_object(self, request):
        try:
            id = request.data.get('id')
            admission = Admission.objects.get(id=id)
            return admission
        except Admission.DoesNotExist:
            return None
        
    def get(self, request):
        admissions = Admission.objects.all()
        serializer = AdmissionSerializer(admissions, many=True)
        return Response({
            "msg": "Admissions retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AdmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Admission created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        admission = get_object(request)
        serializer = AdmissionSerializer(admission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Admission updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        admission = get_object(request)
        serializer = AdmissionSerializer(admission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Admission partially updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        admission = get_object(request)
        admission.delete()
        return Response({
            "msg": "Admission deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
        
