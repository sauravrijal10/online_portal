from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            branch=validated_data['branch'],
        )
       
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # def validate(self, data):
    #     is_admin=data.get('is_admin')
    #     branch = data.get('branch')
    #     if is_admin and User.objects.filter(branch=branch, is_admin=True).exists():
    #         raise serializers.ValidationError({'admin user for this branch exists'})
    #     return data
    
    