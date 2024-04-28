from django.urls import path
from .views import (CourseListView, TeacherListView, StudentListView,
                    AdminProfileView,AdminLoginView, AdminReytingView, AdminMoliyaView, AdminDashboardView)

app_name = 'admin_panel'
urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('students/', StudentListView.as_view(), name='students'),
    path('profile/', AdminProfileView.as_view(), name='profile'),
    path('login/', AdminLoginView.as_view(), name='login'),
    path('reyting/', AdminReytingView.as_view(), name='reyting'),
    path('moliya/', AdminMoliyaView.as_view(), name='moliya'),
]
