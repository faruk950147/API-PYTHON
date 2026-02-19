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

# AdmissionInfoView is a class-based view that gets all admissions
# it is used to get all admissions
# it is a GET request
# it is used to get all admissions
@method_decorator(never_cache, name='dispatch')
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
        
# AdmissionInfoEditView is a class-based view that updates an admission
# it is used to update an admission by id
# it is a PUT request
# it is used to update an admission by id
@method_decorator(never_cache, name='dispatch')
class AdmissionInfoEditView(APIView):
    # put method to update an admission
    def put(self, request, id):
        # get the admission by id
        admission = get_object_or_404(Admission, id=id)
        # serialize the request data
        serializer = AdmissionSerializer(admission, data=request.data)
        # validate the data
        if serializer.is_valid():
            # save the data
            serializer.save()
            # return the serialized data
            return Response({
                'message': 'Admission updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        # return the error message
        return Response({
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    # patch method to patch an admission
    def patch(self, request, id):
            # get the admission by id
            admission = get_object_or_404(Admission, id=id)
            # serialize the request data
            serializer = AdmissionSerializer(admission, data=request.data, partial=True)
            # validate the data
            if serializer.is_valid():
                # save the data
                serializer.save()
                # return the serialized data
                return Response({
                    'message': 'Admission updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            # return the error message
            return Response({
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            

# AdmissionInfoDeleteView is a class-based view that deletes an admission
# it is used to delete an admission by id
# it is a DELETE request
# it is used to delete an admission by id
@method_decorator(never_cache, name='dispatch')
class AdmissionInfoDeleteView(APIView):
    # delete method to delete an admission
    def delete(self, request, id):
        # get the admission by id
        admission = get_object_or_404(Admission, id=id)

        # delete the admission
        admission.delete()

        # return success response
        return Response({
            'message': 'Admission deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)