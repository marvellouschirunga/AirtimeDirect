from django.contrib import admin
from .models import AirtimeRequest, User

# Register your models here.
admin.site.register(User)
admin.site.register(AirtimeRequest)

