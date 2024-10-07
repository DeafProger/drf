from users.models import User, Payment, Subscription
from django.contrib import admin


# Register your models here.
admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(User)
