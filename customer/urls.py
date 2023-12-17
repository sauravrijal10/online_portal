from .views import get_presigned_url
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet
from django.urls import path, include


router = DefaultRouter()
router.register('', CustomerViewSet, basename='customer')
# router.register('get-presigned-url', get_presigned_url, basename='url')

urlpatterns =[
    path('get-presigned-url/', get_presigned_url, name='get_presigned_url'),
    path('', include(router.urls)),
   
    # path('confirm-upload/', confirm_upload, name='confirm_upload'),
]