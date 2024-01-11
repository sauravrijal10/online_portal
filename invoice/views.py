from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        invoice_instance = serializer.save(invoice_created_by=user)
        response_data = serializer.data
        response_data['id']=invoice_instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)