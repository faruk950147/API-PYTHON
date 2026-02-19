from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import models and serializers
from apis.models import Admission
from apis.sterilizers import AdmissionSerializer

class AdmissionInfoView(APIView):
    # get method to get all admissions
    def get(self, request):
        # get all active admissions
        admissions = Admission.objects.filter(status='Active')
        # serialize the admissions queryset
        serializer = AdmissionSerializer(admissions, many=True)
        # return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
