from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
from django.db import models


# Create your models here.
class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=35, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)
    role = models.CharField(max_length=15, verbose_name='роль', choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', blank=True, null=True)
    amount_payment = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='сумма оплаты')
    type_payment = models.CharField(max_length=50,  verbose_name='способ оплаты',
                                    choices=[
                                            ('CASH', 'Оплата наличными'),
                                            ('CARD', 'Оплата картой')
                                            ]
                                    )

    class Meta:
        verbose_name = 'Оплата'
        ordering = ('-payment_date',)
 