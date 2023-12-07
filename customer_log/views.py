from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Customer_log
from .serializers import CustomerLogSerializer

class CustomerLogViewSet(ModelViewSet):
    queryset = Customer_log.objects.all()
    serializer_class = CustomerLogSerializer
    permission_classes = [AllowAny]