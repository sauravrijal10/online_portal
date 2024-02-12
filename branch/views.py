from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import AllowAny

from .models import Branch
from .serializers import BranchSerializer

# from rest_framework.response import Response
# from rest_framework import status

from online_portal.permissions import IsSuperuserOrReadOnly, IsAdminOrSuperuser

class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrSuperuser]

    # def perform_create(self,serializer):
    #     serializer.is_valid(raise_exception=True)
    #     user = self.request.user
    #     serializer.save(added_by = user)
    #     response_data = serializer.data
    #     return Response(response_data, status=status.HTTP_201_CREATED)

