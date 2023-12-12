import boto3
import uuid
from django.core.exceptions import RequestDataTooBig

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from .serializers import CustomerSerializer

from django.http import JsonResponse


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         # Call the parent class's create method to perform the default behavior
    #         return super().create(request, *args, **kwargs)

    #     except RequestDataTooBig as e:
    #         # Catch the RequestDataTooBig exception
    #         error_message = 'Request data is too big. Please upload a smaller file.'
    #         return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except RequestDataTooBig as e:
            # Catch the RequestDataTooBig exception
            error_message = 'Request data is too big. Please upload a smaller file.'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET'])
# @permission_classes([AllowAny])
def get_presigned_url(request):
    s3_client = boto3.client('s3',
                             aws_access_key_id="AKIAVJ5WIBK3RUVMVX6I",
                             aws_secret_access_key="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",
                            #  aws_secret_access_key = quote_plus("dLRLFsvvzZw29YAa+VV7kbCnZmOJQx4MlVhTVXuL"),
                            #  config=Config(signature_version='s3v4'),
                            #  signature_version='s3v4',
                             region_name="ap-south-1")

    bucket_name = 'hamro-booking-images'
    image_id = str(uuid.uuid4())

    object_key = f'{image_id}.pdf'
    presigned_url = s3_client.generate_presigned_url('put_object',
                                                     Params={'Bucket': bucket_name,
                                                             'Key': object_key},
                                                     ExpiresIn=86400)  # Set the expiration time in seconds
    return JsonResponse({'presigned_url': presigned_url})

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_upload(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # return Response({
        #         'data': serializer.data,
        #         'message': 'Room created successfully'

        #     }, status = status.HTTP_201_CREATED)
        return JsonResponse({'message': 'File uploaded successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)