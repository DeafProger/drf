from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование курса')
    preview = models.ImageField(upload_to='materials/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тема урока')
    preview = models.ImageField(upload_to='materials/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course')

    def __str__(self):
        return f'{self.name}, курс {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
