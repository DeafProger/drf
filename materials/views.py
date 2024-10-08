from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, LessonDetailSerializer
from materials.paginators import MaterialsPaginator
from users.permissions import IsModerator, IsOwner
from rest_framework import viewsets, generics
from materials.models import Course, Lesson

from materials.tasks import send_update_info_task


class CourseViewSet(viewsets.ModelViewSet):
    default_serializer = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator
    serializers_choice = {
        'retrieve': CourseDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers_choice.get(self.action, self.default_serializer)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        """Отправляем уведомление всем подписанным пользователям"""
        updated_course = serializer.save()
        subject = f'Обновление курса {updated_course.name}'
        message = 'По Вашей подписке есть обновление'
        send_update_info_task.delay(updated_course.id, subject, message)
        updated_course.save()


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]
    pagination_class = MaterialsPaginator


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]
