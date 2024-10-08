from users.models import Payment, User, Subscription
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    payment_list = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Базовый cериализатор для модели подписки"""
    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Cериализатор для создания платежа"""

    class Meta:
        model = Payment
        fields = ('payment_url')
