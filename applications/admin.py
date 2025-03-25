from django.contrib import admin
from .models import Application, ApplicationHistory, ApplicationDocument
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Application)
admin.site.register(ApplicationHistory)
admin.site.register(ApplicationDocument)
