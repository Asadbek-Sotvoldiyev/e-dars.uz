from django.urls import path
from .views import (CourseListView, TeacherListView, StudentListView,
                    AdminProfileView, AdminLoginView, AdminReytingView,
                    AdminMoliyaView, AdminDashboardView, AddCourseView, AddTeacherView,
                    logout_user, AddStudentView, StudentPayments, PaymentConfirm,
                    PaymentUnconfirm, lesson_detail_students, AdminStudentsView,
                    AdminDarsView, AddStudentToCourse)

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
    path('payments/detail-students/<int:course_id>/', AdminStudentsView.as_view(), name='detail_students'),
    path('courses/detail-video/<int:course_id>/', AdminDarsView.as_view(), name='detail_video'), #
    #path('courses/detail-video/', lesson_detail_video, name='detail_video'), #
    #path('courses/detail-students/', lesson_detail_students, name='detail_students'), #
    path('payments/check/confirm/<int:check_number>/', PaymentConfirm.as_view(), name='check_confirm'),
    path('payments/check/unconfirm/<int:check_number>/', PaymentUnconfirm.as_view(), name='check_unconfirm'),
    path('add-student-to-course/', AddStudentToCourse.as_view(), name='add_student_to_course'),
    path('logout/', logout_user, name='logout'),
]
