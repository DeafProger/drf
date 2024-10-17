from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import UserSerializer
from users.permissions import IsOwner
from rest_framework import generics
from django.shortcuts import redirect
from users.models import User


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)  # сделали польз-ля активным
        user.set_password(user.password)  # хешируется пароль
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


def login(request):
    return redirect('login/')
