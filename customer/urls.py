from .views import get_presigned_url
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, upload_success
from django.urls import path, include


router = DefaultRouter()
router.register('', CustomerViewSet, basename='customer')
# router.register('get-presigned-url', get_presigned_url, basename='url')

urlpatterns =[
    path('get-presigned-url/', get_presigned_url, name='get_presigned_url'),
    path('upload-success/', upload_success, name='upload_success'),
    path('', include(router.urls)),
   
    
]