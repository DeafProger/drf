from materials.models import Course, Lesson
from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):
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
