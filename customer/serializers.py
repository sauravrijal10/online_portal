from rest_framework import serializers

from .models import Customer

#
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer_creator'] = instance.customer_creator.email
        if instance.branch is not None:
            representation['branch'] = instance.branch.name
        else:
            representation['branch'] = None
        return representation
    