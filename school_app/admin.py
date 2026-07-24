from django.contrib import admin

from school_app.models import LoginData, Teacher, Student

# Register your models here.
admin.site.register(LoginData)
admin.site.register(Teacher)
admin.site.register(Student)
