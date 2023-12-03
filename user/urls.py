from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, activate_account, user_login

from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "user"

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}),name="userviewset"),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name="activate"),
    path('login/', user_login, name="login"),
]