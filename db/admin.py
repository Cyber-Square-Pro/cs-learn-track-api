from django.contrib import admin
from .models.admin import AdminData
from .models.batch import Batch, Session
from .models.user import StudentData, Teacher, UserProfile

admin.site.register(AdminData)
admin.site.register(Batch)
admin.site.register(Session)
admin.site.register(StudentData)
admin.site.register(Teacher)
admin.site.register(UserProfile)
