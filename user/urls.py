from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, activate_account

# router = DefaultRouter()
# router.register('', UserViewSet, basename='user')
# router.register('activate/<str:uidb64>/<str:token>/', activate_account, basename='activate')
# urlpatterns = router.urls
urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}),name="userviewset"),
    # path('<int:pk>', UserViewSet.as_view({'get': 'list', 'post': 'create'}),name="userviewset"),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name="activate")
]