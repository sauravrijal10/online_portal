import boto3
import uuid
import logging
from django.core.exceptions import RequestDataTooBig

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from customer_log.models import Customer_log
from .models import Customer
from .serializers import CustomerSerializer

from django.http import JsonResponse, HttpResponseBadRequest
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
        try:
            serializer.is_valid(raise_exception=True)
            customer_instance = serializer.save()

            previous_values = getattr(customer_instance, '_previous_values', {})

            changed_data = {}
            for field_name, previous_value in previous_values.items():
                current_value = getattr(customer_instance, field_name)

                previous_value_stripped = str(previous_value).strip().lower()
                current_value_stripped = str(current_value).strip().lower()

                if previous_value_stripped != current_value_stripped:
                    changed_data[field_name] = {
                        'previous': previous_value,
                        'current': current_value,
                    }

            if changed_data:
                current_user = self.request.user 
                log_data = {
                    'customer': customer_instance,
                    'remark': ', '.join([f"{key}: {value['previous']} -> {value['current']}" for key, value in changed_data.items()]),
                    'user': current_user if self.request.user.is_authenticated else None # Assign the User instance
                }
                # Create a CustomerLog instance whenever a Customer is updated
                Customer_log.objects.create(**log_data)
                logger.info("Log entry created.")

            return Response(serializer.data, status=status.HTTP_200_OK)
        except RequestDataTooBig as e:
            error_message = 'Request data is too big. Please upload a smaller file.'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

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