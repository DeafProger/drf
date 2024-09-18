from users.views import PaymentListView, UserUpdateView, UserDetailView
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from django.urls import path


app_name = UsersConfig.name

urlpatterns = [
                  path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
                  path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
                  path('payment/', PaymentListView.as_view(), name='payment_list'),
              ]