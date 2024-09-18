from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Payment


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
