from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import update_last_login
from .models import CustomUserModel
from .serializers import UserSerializer, UserActivitySerializer
from .exceptions import MaxNumberOfUserException
from .services import is_free_place_for_new_user
from bot.config import SocialNetworkConfigRules


class RegisterView(CreateAPIView):
    queryset = CustomUserModel.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        config = SocialNetworkConfigRules.get_config()
        if not is_free_place_for_new_user(config.number_of_users):
            raise MaxNumberOfUserException(f'You can not register, server limited '
                                           f'to {config.number_of_users} users')
        user = CustomUserModel.objects.create_user(**request.data)
        data = self.get_serializer(instance=user).data
        return Response(data, status=status.HTTP_201_CREATED)


class UserActivityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = UserActivitySerializer(instance=request.user).data
        return Response(data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Implementation of TokenObtainPairView with last_login update"""

    def post(self, request, *args, **kwargs):
        result = super(TokenObtainPairView, self).post(request, *args, **kwargs)
        try:
            username = request.__dict__['_data']['username']
            user = CustomUserModel.objects.get(username=username)
            update_last_login(None, user)
        except Exception as exc:
            return Response({'error': exc.args}, status=400)
        return result

