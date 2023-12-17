from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['invoice_created_by'] = instance.invoice_created_by.email
        return representation
