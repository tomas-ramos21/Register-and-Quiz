from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import User
from login.models import Employee, Student

admin.site.register(Employee)
admin.site.register(Student)
