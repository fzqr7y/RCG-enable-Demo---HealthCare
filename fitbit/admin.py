from django.contrib import admin

# Register your models here.
from .models import ApiData, IntradayData

admin.site.register(ApiData)
admin.site.register(IntradayData)
