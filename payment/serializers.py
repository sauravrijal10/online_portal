from rest_framework import serializers

from .models import Payment
from django.core.exceptions import ValidationError


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['payment_creator'] = instance.payment_creator.email
        return representation

    def validate(self, data):
        payment_type = data.get('payment_type')
        invoice_id = data.get('invoice_id')
        payment_status = data.get('payment_status')

        if payment_type == Payment.PaymentType.THIRD.value:
            first_payment_exists = Payment.objects.filter(payment_type=Payment.PaymentType.FIRST.value, invoice_id=invoice_id).exists()
            second_payment_exists = Payment.objects.filter(payment_type=Payment.PaymentType.SECOND.value, invoice_id=invoice_id).exists()
            if not (first_payment_exists and second_payment_exists):
                raise serializers.ValidationError({'payment_type': 'Cannot select THIRD without creating payment objects for both FIRST and SECOND with the same invoice_id.'})
        if payment_type == Payment.PaymentType.SECOND.value:
            first_payment_exists = Payment.objects.filter(payment_type=Payment.PaymentType.FIRST.value, invoice_id=invoice_id).exists()
            if not (first_payment_exists):
                raise serializers.ValidationError({'payment_type': 'Cannot select SECOND without creating payment objects for both FIRST with the same invoice_id.'})
        if payment_type == Payment.PaymentType.SECOND.value:
            first_payment_completed = Payment.objects.filter(payment_type=Payment.PaymentType.FIRST.value, invoice_id=invoice_id, payment_status=Payment.status.COMPLETED.value).exists()
            if not first_payment_completed:
                raise serializers.ValidationError({'payment_type': 'Cannot select SECOND until payment of type FIRST is completed.'})

        if payment_type == Payment.PaymentType.THIRD.value:
            second_payment_completed = Payment.objects.filter(payment_type=Payment.PaymentType.SECOND.value, invoice_id=invoice_id, payment_status=Payment.status.COMPLETED.value).exists()
            if not second_payment_completed:
                raise serializers.ValidationError({'payment_type': 'Cannot select THIRD until payment of type SECOND is completed.'})
        if payment_status == Payment.status.COMPLETED.value:
            existing_completed_payments = Payment.objects.filter(
                payment_type=payment_type,
                invoice_id=invoice_id,
                payment_status=Payment.status.COMPLETED.value
            ).exclude(id=self.instance.id if self.instance else None)

            if existing_completed_payments.exists():
                raise serializers.ValidationError({
                    'payment_status': 'A payment of the same type with status COMPLETED already exists for this invoice_id.'
                })
        if payment_status != Payment.status.COMPLETED.value:
            completed_payment_exists = Payment.objects.filter(
                payment_type=payment_type,
                invoice_id=invoice_id,
                payment_status=Payment.status.COMPLETED.value
            ).exists()

            if completed_payment_exists:
                raise serializers.ValidationError({
                    'payment_status': f'A payment of type {payment_type} with status COMPLETED already exists for this invoice_id.'
                })
            
        return data