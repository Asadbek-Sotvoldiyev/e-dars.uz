from django.urls import path
from .views import *


app_name = 'teacher_panel'
urlpatterns = [
    path('', TeacherDashboard.as_view(), name='dashboard'),
    path('kurslar/', TeacherCourses.as_view(), name='kurslar'),
    path('profile/', TeacherProfileView.as_view(), name='profile'),
    path('lesson/<int:course_id>/', TeacherLesson.as_view(), name='lesson'),
    path('add-lesson/<int:course_id>/', AddLessonView.as_view(), name='add_lesson'),
]
