from django.contrib import admin

from user_app.views import Permission
from .models import PassManager, SharingDetails
# Register your models here.

admin.site.register(PassManager)
admin.site.register(SharingDetails)
# admin.site.register(Permission)