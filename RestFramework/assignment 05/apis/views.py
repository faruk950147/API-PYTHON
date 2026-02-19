from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache, cache_page
from django.shortcuts import get_object_or_404
from django.contrib import messages
# import models and serializers
from apis.models import Admission
from apis.sterilizers import AdmissionSerializer

@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class AdmissionInfoView(APIView):
    # get method to get all admissions
    def get(self, request):
        # get all active admissions
        admissions = Admission.objects.filter(status='Active')
        # serialize the admissions queryset
        serializer = AdmissionSerializer(admissions, many=True)
        # return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # post method to create a new admission
    def post(self, request):
        # serialize the request data
        serializer = AdmissionSerializer(data=request.data)
        # validate the data
        if serializer.is_valid():
            # save the data
            serializer.save()
            # return the serialized data
            return Response({
                'message': 'Admission created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        # return the error message
        return Response({
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
