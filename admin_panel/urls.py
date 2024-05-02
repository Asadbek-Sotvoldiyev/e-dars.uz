from django.urls import path
from .views import (CourseListView, TeacherListView, StudentListView,
                    AdminProfileView, AdminLoginView, AdminReytingView,
                    AdminMoliyaView, AdminDashboardView, AddCourseView, AddTeacherView,
                    logout_user, AddStudentView, StudentPayments, PaymentConfirm,
                    PaymentUnconfirm)

app_name = 'admin_panel'
urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('students/', StudentListView.as_view(), name='students'),
    path('profile/', AdminProfileView.as_view(), name='profile'),
    path('login/', AdminLoginView.as_view(), name='login'),
    path('reyting/', AdminReytingView.as_view(), name='reyting'),
    path('payments/', AdminMoliyaView.as_view(), name='moliya'),
    path('add-course/', AddCourseView.as_view(), name='add_course'),
    path('add-teacher/', AddTeacherView.as_view(), name='add_teacher'),
    path('add-student/', AddStudentView.as_view(), name='add_student'),
    path('payments/check/', StudentPayments.as_view(), name='check'),
    path('payments/check/confirm/<int:check_number>/', PaymentConfirm.as_view(), name='check_confirm'),
    path('payments/check/unconfirm/<int:check_number>/', PaymentUnconfirm.as_view(), name='check_unconfirm'),
    path('logout/', logout_user, name='logout'),
]
