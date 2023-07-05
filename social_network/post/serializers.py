from rest_framework import serializers

from .models import PostModel
from user.serializers import UserSerializer


class CreatePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostModel
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        exclude = ('likes', 'dislikes')

    def get_likes_count(self, obj) -> int:
        return obj.likes_count()

    def get_dislikes_count(self, obj) -> int:
        return obj.dislikes_count()
