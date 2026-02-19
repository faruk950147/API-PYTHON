from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404

from apis.models import Admission
from apis.sterilizers import AdmissionSerializer


# ===============================
# LIST + CREATE
# ===============================
@method_decorator(never_cache, name='dispatch')
class AdmissionInfoView(APIView):

    def get(self, request):
        admissions = Admission.objects.filter(status='Active')
        serializer = AdmissionSerializer(admissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, message="Admission created successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, message="Invalid data")


# ===============================
# UPDATE (PUT + PATCH)
# ===============================
@method_decorator(never_cache, name='dispatch')
class AdmissionInfoEditView(APIView):

    def get_object(self, id):
        return get_object_or_404(Admission, id=id)

    def put(self, request, id):
        admission = self.get_object(id)
        serializer = AdmissionSerializer(admission, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, message="Admission updated successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, message="Invalid data")

    def patch(self, request, id):
        admission = self.get_object(id)
        serializer = AdmissionSerializer(
            admission, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, message="Admission updated successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, message="Invalid data")


# ===============================
# DELETE
# ===============================
@method_decorator(never_cache, name='dispatch')
class AdmissionInfoDeleteView(APIView):

    def get_object(self, id):
        return get_object_or_404(Admission, id=id)

    def delete(self, request, id):
        admission = self.get_object(id)
        admission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, message="Admission deleted successfully")
