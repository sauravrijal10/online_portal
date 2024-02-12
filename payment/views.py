from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action



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
    
    @action(detail=False, methods=['put','patch'])
    def bulk_update_status(self, request):
        payment_ids = request.data.get('payment_ids', [])
        new_status = request.data.get('new_status')

        if not payment_ids or not new_status:
            return Response({'error': 'payment_ids and new_status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payments = Payment.objects.filter(id__in=payment_ids)
            payments.update(payment_status=new_status)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Bulk update successful'}, status=status.HTTP_200_OK)
    
