from materials.models import Course, Lesson
from django.contrib import admin


# Register your models here.
admin.site.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'owner')

admin.site.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'owner')
