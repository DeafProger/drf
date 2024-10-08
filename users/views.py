from users.serializers import UserSerializer, PaymentSerializer, \
    UserDetailSerializer, SubscriptionSerializer, PaymentCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import generics, status
from users.models import User, Payment, Subscription
from rest_framework.views import APIView
from materials.models import Course

from services import get_session
from config import settings
import stripe


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'type_payment',)
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionView(APIView):
    """Контроллер управления подпиской пользователя на курс"""
    serializer_class = SubscriptionSerializer

    @staticmethod
    def post(request, pk):
        course = get_object_or_404(Course, pk=pk)
        subs_item = Subscription.objects.filter(course=course, user=request.user)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=request.user, course=course)
            message = 'Подписка добавлена'
        return Response({"message": message})


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_payment = serializer.save()
        stripe.api_key = settings.STRIPE_API_KEY
        response = get_session()
        new_payment.session_id = response['id']
        new_payment.payment_url = response['url']
        new_payment.payment_status = response['payment_status']
        new_payment.payment_amount = response['amount_total']
        new_payment.save()
        return super().perform_create(serializer)
