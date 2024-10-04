from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import PaymentListView, UserUpdateView, SubscriptionView,\
    UserListView, UserCreateView, UserDetailView, UserDeleteView, PaymentCreateView
from users.apps  import UsersConfig
from django.urls import path


app_name = UsersConfig.name

urlpatterns = [
                path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
                path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
                path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
                path('user/create/', UserCreateView.as_view(), name='user_create'),
                path('user/', UserListView.as_view(), name='user_list'),

                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('token/', TokenObtainPairView.as_view(), name='login'),

                path('subscr/<int:pk>/', SubscriptionView.as_view(), name='subscr_switch'),

                path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
                path('payment/', PaymentListView.as_view(), name='payment_list'),
              ]
