from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse
from rest_framework import status
from .tasks import send_activation_email_async
from rest_framework.exceptions import PermissionDenied,ValidationError



from .serializers import UserSerializer

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
import logging


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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        is_admin = self.request.data.get('is_admin', False)       
        password = serializer.validated_data.get('password')
        is_staff = serializer.validated_data.get('is_staff', False)

        if is_admin and not self.request.user.is_superuser:
            raise PermissionDenied("Only superusers can create an admin user.")
        
        if is_staff and not (self.request.user.is_admin or self.request.user.is_superuser):
            raise PermissionDenied("Only admins or superusers can create a staff user")

        user = User.objects.create_user(email=serializer.validated_data.get('email'), password=password,
                                        first_name=serializer.validated_data.get('first_name'),
                                        last_name=serializer.validated_data.get('last_name'),
                                        username=serializer.validated_data.get('username'),
                                        is_admin=serializer.validated_data.get('is_admin'),
                                        is_staff=is_staff,
                                        branch=serializer.validated_data.get('branch'),
                                        )
        request = self.request
        if request:
            current_site_domain = request.get_host()
        send_activation_email_async.delay(user.id, current_site_domain)
        
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def user_login(request):
    try:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({"message":"user logged-in",
                        "access_token":str(refresh.access_token),
                        "refresh_token":str(refresh),
                        "user_data": {
                            "user_id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "branch": user.branch.name,
                            "is_active": user.is_active,
                            "is_staff": user.is_staff,
                            "is_admin": user.is_admin,
                            "is_superuser": user.is_superuser,
                            }
                        })
    except ValidationError as e:
        error_details = e.detail
        return Response({"error": "Validation error", "details": error_details}, status=400)

        

    except Exception as e:
        return HttpResponse('This account cannot be logged in due to validation issues')