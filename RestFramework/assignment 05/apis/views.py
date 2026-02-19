from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import models and serializers
from apis.models import Admission
from apis.sterilizers import AdmissionSerializer
class AdmissionInfoView(APIView):
    # get method to get all admissions
    def get(self, request):
        # get all admissions query set
        admissions = Admission.objects.filter(status='Active')
        # serialize the admissions query set
        serializer = AdmissionSerializer(admissions, many=True)
        # return the serialized data
        return Response(admissions, status=status.HTTP_200_OK)