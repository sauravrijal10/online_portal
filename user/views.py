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



from .serializers import UserSerializer
# from .utils import send_activation_email

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
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(email=serializer.validated_data.get('email'), password=password,
                                        first_name=serializer.validated_data.get('first_name'),
                                        last_name=serializer.validated_data.get('last_name'),
                                        username=serializer.validated_data.get('username')
                                        )
        request = self.request
        if request:
            current_site_domain = request.get_host()
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
