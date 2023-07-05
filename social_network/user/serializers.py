from rest_framework import serializers
from .models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        exclude = ('password',)

    def create(self, validated_data):
        return CustomUserModel.objects.create_user(**validated_data)
