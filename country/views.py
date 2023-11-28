from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
