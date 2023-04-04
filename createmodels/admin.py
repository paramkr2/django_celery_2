from django.contrib import admin
from .models import StoreStatus ,BusinessHours,StoreTimezone
# Register your models here.

admin.site.register(StoreStatus)
admin.site.register(BusinessHours)
admin.site.register(StoreTimezone)
