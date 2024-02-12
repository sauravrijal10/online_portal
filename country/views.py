from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Country
from .serializers import CountrySerializer

from online_portal.permissions import IsAdminOrSuperuser

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrSuperuser]

    def perform_create(self,serializer):
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        serializer.save(added_by = user)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)
        

