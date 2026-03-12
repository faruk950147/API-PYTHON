from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apis.models import Admission
from apis.serializers import AdmissionSerializer


class AdmissionListCreateAPIView(APIView):
    # GET All
    def get(self, request):
        admissions = Admission.objects.all()
        serializer = AdmissionSerializer(admissions, many=True)
        return Response(serializer.data)

    # POST Create
    def post(self, request):
        serializer = AdmissionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdmissionDetailAPIView(APIView):
    # Helper method
    def get_object(self, pk):
        return get_object_or_404(Admission, pk=pk)

    # GET single admission
    def get(self, request, pk):
        admission = self.get_object(pk)
        serializer = AdmissionSerializer(admission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT (Full update)
    def put(self, request, pk):
        admission = self.get_object(pk)
        serializer = AdmissionSerializer(admission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH (Partial update)
    def patch(self, request, pk):
        admission = self.get_object(pk)
        serializer = AdmissionSerializer(admission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        admission = self.get_object(pk)
        admission.delete()
        return Response(
            {"message": "Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )