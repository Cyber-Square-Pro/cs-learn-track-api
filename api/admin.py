from django.contrib import admin
from api.models import AdminData
from api.models import StudentData

# Register your models here.
admin.site.register(AdminData)
admin.site.register(StudentData)