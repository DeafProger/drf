from habits.views import (HabitsListAPIView, HabitsCreateAPIView,
                          HabitsPublicListAPIView, HabitsRetrieveAPIView,
                          HabitsUpdateAPIView, HabitsDestroyAPIView)
from habits.apps import HabitsConfig
from django.urls import path


app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitsListAPIView.as_view(), name='habits_list'),
    path('habits/<int:pk>/delete/', HabitsDestroyAPIView.as_view(),
         name='habits_delete'),
    path('habits/<int:pk>/update/', HabitsUpdateAPIView.as_view(),
         name='habits_update'),
    path('public/', HabitsPublicListAPIView.as_view(),
         name='habits_public_list'),
    path('habits/create/', HabitsCreateAPIView.as_view(),
         name='habits_create'),
    path('habits/<int:pk>/', HabitsRetrieveAPIView.as_view(),
         name='habits_detail'),
]
