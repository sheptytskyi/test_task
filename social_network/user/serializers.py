from rest_framework import serializers
from .models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        exclude = ('password',)


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('last_login', 'last_activity')
