from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from rest_framework import status
from celery import shared_task
from .tasks import send_activation_email_async

from .serializers import UserSerializer
# from .utils import send_activation_email

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
import logging

# from rest_framework_swagger.decorators import swagger_schema

logger = logging.getLogger('application_logger')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Account has been activated', status=status.HTTP_200_OK)  
    else:
        return HttpResponse('Account cannot be activated', status=status.HTTP_400_BAD_REQUEST) 


# @swagger_schema(
#     request={
#         'parameters': [
#             {
#                 'name': 'limit',
#                 'required': False,
#                 'type': 'integer',
#                 'in': 'query',
#                 'description': 'The maximum number of users to return in the response.'
#             },
#             {
#                 'name': 'offset',
#                 'required': False,
#                 'type': 'integer',
#                 'in': 'query',
#                 'description': 'The number of users to skip in the response.'
#             }
#         ]
#     },
#     responses={
#         '200': {
#             'description': 'A list of users',
#             'schema': UserSerializer
#         }
#     }
# )
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(email=serializer.validated_data.get('email'), password=password)
        # user = serializer.save()
        current_site_domain = '0.0.0.0:8000'
        send_activation_email_async.delay(user.id, current_site_domain)

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    refresh = RefreshToken.for_user(user)
    return Response({"message":"user logged-in",
                      "access_token":str(refresh.access_token),
                      "refresh_token":str(refresh),
                      "user_role": user.user_role
                      })
