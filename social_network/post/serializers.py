from rest_framework import serializers

from .models import PostModel, LikePostModel
from user.serializers import UserSerializer


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


class PostAnalyticSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = LikePostModel
        exclude = ('user', 'id')

    def get_likes(self, obj) -> int:
        likes = LikePostModel.objects.filter(
            post_id=obj.post_id,
            created_at=obj.created_at
        ).count()
        return likes

