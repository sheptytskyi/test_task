import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from .serializers import PostSerializer, PostAnalyticSerializer
from .models import PostModel, LikePostModel
from bot.config import SocialNetworkConfigRules
from .exceptions import MaxPostsPerUserException, MaxLikesPerUserException
from .services import is_user_has_posts, is_user_has_likes


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()

    def create(self, request, *args, **kwargs):
        config = SocialNetworkConfigRules.get_config()

        if not is_user_has_posts(request.user.id, config.max_posts_per_user):
            raise MaxPostsPerUserException(f'You have possibility to publish '
                                           f'only {config.max_posts_per_user} posts')

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_post = serializer.create(serializer.validated_data)
            new_post.author_id = request.user.id
            new_post.save()

            data = self.get_serializer(instance=new_post).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=True)
    def like(self, request, *args, **kwargs):
        config = SocialNetworkConfigRules.get_config()

        if not is_user_has_likes(request.user.id, config.max_likes_per_user):
            raise MaxLikesPerUserException(f'You have possibility to like '
                                           f'only {config.max_likes_per_user} times')
        try:
            post = PostModel.objects.get(uuid=kwargs['pk'])
        except PostModel.DoesNotExist:
            return Response(status=404)

        post.dislikes.remove(request.user)
        post.likes.add(request.user)
        data = self.get_serializer(instance=post).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True)
    def dislike(self, request, *args, **kwargs):
        try:
            post = PostModel.objects.get(uuid=kwargs['pk'])
        except PostModel.DoesNotExist:
            return Response(status=404)

        post.likes.remove(request.user)
        post.dislikes.add(request.user)
        data = self.get_serializer(instance=post).data
        return Response(data, status=status.HTTP_200_OK)


class PostAnalyticsView(APIView):
    def get(self, request, *args, **kwargs):
        date_from = datetime.datetime.strptime(request.GET.get('date_from'), "%Y/%m/%d").date()
        date_to = datetime.datetime.strptime(request.GET.get('date_to'), "%Y/%m/%d").date()
        likes = LikePostModel.objects.filter(
            created_at__gte=date_from,
            created_at__lte=date_to
        ).distinct('created_at', 'post_id')
        data = PostAnalyticSerializer(likes, many=True).data
        return Response(data)
