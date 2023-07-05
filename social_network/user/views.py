from rest_framework.generics import CreateAPIView
from .models import CustomUserModel
from .serializers import UserSerializer


class RegisterView(CreateAPIView):
    queryset = CustomUserModel.objects.all()
    serializer_class = UserSerializer
