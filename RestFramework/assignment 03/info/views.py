from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from info.models import Admission
from info.serializers import AdmissionSerializer


class EndPointAPIView(APIView):
    """
    API Root: Lists all available endpoints for the Admission app.
    """
    def get(self, request):
        return Response({
            "status": "success",
            "endpoints": [
                "/admission-info/",
            ]
        }, status=status.HTTP_200_OK)
        

class AdmissionInfoView(APIView):
    """
    Handles CRUD operations for Admission records.

    Supported methods:
    - GET: List all admissions
    - POST: Create a new admission
    - PUT: Update an existing admission (requires 'id' in request.data)
    - PATCH: Partially update an admission (requires 'id' in request.data)
    - DELETE: Delete an admission (requires 'id' in request.data)
    """

    def get_object(self, pk):
        """
        Retrieve a single Admission by ID.
        Raises Http404 if not found.
        """
        try:
            return Admission.objects.get(pk=pk)
        except Admission.DoesNotExist:
            raise Http404("Admission not found")
        
    # List all admissions
    def get(self, request):
        admissions = Admission.objects.all()
        serializer = AdmissionSerializer(admissions, many=True)
        return Response({
            "msg": "Admissions retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    # Create a new admission
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
    
    # Update an admission completely
    def put(self, request):
        admission_id = request.data.get('id')
        if not admission_id:
            return Response({"msg": "Admission ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        admission = self.get_object(admission_id)
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

    # Partial update of an admission
    def patch(self, request):
        admission_id = request.data.get('id')
        if not admission_id:
            return Response({"msg": "Admission ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        admission = self.get_object(admission_id)
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
    
    # Delete an admission
    def delete(self, request):
        admission_id = request.data.get('id')
        if not admission_id:
            return Response({"msg": "Admission ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        admission = self.get_object(admission_id)
        admission.delete()
        return Response({
            "msg": "Admission deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)