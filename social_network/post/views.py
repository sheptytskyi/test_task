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


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()

    def create(self, request, *args, **kwargs):
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
        try:
            post = PostModel.objects.get(uuid=kwargs['pk'])
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            data = self.get_serializer(instance=post).data
            return Response(data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=404)

    @action(methods=['PATCH'], detail=True)
    def dislike(self, request, *args, **kwargs):
        try:
            post = PostModel.objects.get(uuid=kwargs['pk'])
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            data = self.get_serializer(instance=post).data
            return Response(data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=404)


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
