from rest_framework import serializers

from .models import Customer

def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB in bytes

    if value.size > max_size:
        raise serializers.ValidationError("File size exceeds the maximum limit of 5MB.")
class CustomerSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_file_size])
    class Meta:
        model = Customer
        fields = "__all__"