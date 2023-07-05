from rest_framework import serializers
from .models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        exclude = ('password',)

    def create(self, validated_data):
        return CustomUserModel.objects.create_user(**validated_data)


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('last_login', 'last_activity')
