from rest_framework import serializers

from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = instance.country.name
        return representation