from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        current_site_domain = '0.0.0.0:8000'
        send_activation_email_async.delay(user.id, current_site_domain)


