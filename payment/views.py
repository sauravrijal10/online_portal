from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        payment_instance = serializer.save(payment_creator=user)
        response_data = serializer.data
        response_data['id']=payment_instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)