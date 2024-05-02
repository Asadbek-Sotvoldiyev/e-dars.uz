from django.contrib import admin
from .models import User, CourseCategory, Course, Lesson, Payments, PaymentsCheck

admin.site.register([User, CourseCategory, Course, Lesson, Payments, PaymentsCheck])
