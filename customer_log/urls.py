from rest_framework.routers import DefaultRouter
from .views import CustomerLogViewSet

router = DefaultRouter()
router.register('', CustomerLogViewSet, basename='customer_log')

urlpatterns = router.urls