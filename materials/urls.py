from rest_framework.routers import DefaultRouter
from materials.apps import MaterialsConfig
from django.urls import path
from materials.views import LessonDestroyView, LessonCreateApiView, \
    CourseViewSet, LessonListView, LessonRetrieveView, LessonUpdateView
    

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
app_name = MaterialsConfig.name

urlpatterns = [
                  path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
                  path('lesson/list/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
                  path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_update'),
              ] + router.urls
