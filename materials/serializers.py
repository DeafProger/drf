from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from materials.validators import url_validator
from materials.models import Course, Lesson
from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonDetailSerializer(serializers.ModelSerializer):
    """Cериализатор урока"""
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)

    @staticmethod
    def get_quantity_lessons(obj):
        quantity_lessons = obj.course.all().count()

        if not quantity_lessons:
            return None
        else:
            return quantity_lessons

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор курсa, включая поля кол-ва уроков и списка уроков"""
    lessons_count = SerializerMethodField()
    lessons_list = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def user_(self):
        """Получаем текущего пользователя"""
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_is_subscribed(self, course):
        return course.subscription_set.filter(user=self.user_()).exists()

    @staticmethod
    def get_lessons_count(course):
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_list(course):
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

    class Meta:
        model = Course
        fields = '__all__'

    class LessonDetailSerializer(serializers.ModelSerializer):
        """Cериализатор информации об уроке, где для курса выводится его наименование"""
        course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

        class Meta:
            model = Lesson
            fields = '__all__'
