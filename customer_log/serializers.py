from rest_framework import serializers

from .models import Customer_log


class CustomerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_log
        fields = "__all__"