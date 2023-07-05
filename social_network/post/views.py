from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist

from .serializers import PostSerializer, CreatePostSerializer
from .models import PostModel


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        return super().get_serializer_class()

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
