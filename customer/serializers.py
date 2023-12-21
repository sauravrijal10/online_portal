from rest_framework import serializers

from .models import Customer

# def validate_file_size(value):
#     max_size = 5 * 1024 * 1024

#     if value.size > max_size:
#         raise serializers.ValidationError("File size exceeds the maximum limit of 5MB.")
class CustomerSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(validators=[validate_file_size])
    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer_creator'] = instance.customer_creator.email
        # representation['invoice'] = instance.invoice.remark
        representation['branch'] = instance.branch.name
        return representation
    