import boto3
import uuid
import logging
from django.core.exceptions import RequestDataTooBig

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from customer_log.models import Customer_log
from .models import Customer
from .serializers import CustomerSerializer

from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            customer_instance = serializer.save(customer_creator = user, branch=user.branch)
            response_data = serializer.data
            response_data['id'] = customer_instance.id  
            return Response(response_data, status=status.HTTP_201_CREATED)
        except RequestDataTooBig as e:
            error_message = 'Request data is too big. Please upload a smaller file.'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    def perform_update(self, serializer):
        print('here')
        try:
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            # customer_instance = get_object_or_404(Customer, pk=self.kwargs['pk'])
            # print(f"Queryset: {customer_instance.query}")
            queryset = Customer.objects.filter(pk=self.kwargs['pk'])
            # queryset = self.filter_queryset(self.get_queryset()).filter()
            # queryset = self.filter_queryset()
            customer_instance = queryset.first()
            print(customer_instance)
            if not customer_instance:
                error_message = f"Customer with ID {self.kwargs['pk']} not found."
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

            if user.is_admin or user.is_superuser:
                serializer.save()
            else:
                if customer_instance.branch != user.branch:
                    error_message = f"Staff of branch {user.branch} cannot update customer from another branch."
                    raise PermissionDenied(detail=error_message)
                serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except RequestDataTooBig as e:
            error_message = 'Request data is too big. Please upload a smaller file.'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            error_message = f"Customer with ID {self.kwargs['pk']} not found."
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
        
    def get_queryset(self):
        user = self.request.user

        if user.is_admin or user.is_superuser:
            return Customer.objects.all()
            
        else:
            return Customer.objects.filter(branch=user.branch)
            

def get_presigned_url(request):
    s3_client = boto3.client('s3',
                             aws_access_key_id="AKIAVJ5WIBK3RUVMVX6I",
                             aws_secret_access_key="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",
                            
                             region_name="ap-south-1")
    customer_id = request.GET.get('id')
    if customer_id is None:
        return HttpResponseBadRequest('Parameter "customer_id" is missing')

    bucket_name = 'hamro-booking-images'
    image_id = str(uuid.uuid4())

    object_key = f'{customer_id}/{image_id}.pdf'
    max_content_length = 5 * 1024 * 1024
    presigned_url = s3_client.generate_presigned_url('put_object',
                                                     Params={'Bucket': bucket_name,
                                                             'Key': object_key},
                                                     ExpiresIn=86400,
                                                     HttpMethod='PUT',
                                                     )  
    return JsonResponse({'presigned_url': presigned_url})

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_upload(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'File uploaded successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)