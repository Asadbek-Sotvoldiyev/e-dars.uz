from django.urls import path
from .views import *

app_name = 'student_panel'
urlpatterns = [
    path('', StudentDashboardView.as_view(), name='dashboard'),
    path('kurslar/',  StudentKurslarView.as_view(), name='kurslar'),
    path('payments/', StudentPaymentsView.as_view(), name='payments'),
    path('reyting/',  StudentReytingView.as_view(), name='reyting'),
    path('profile/',  StudentProfileView.as_view(), name='profile'),
    path('message/',  StudentMessageView.as_view(), name='message'),
    path('video/<int:course_id>/', StudentDarsView.as_view(), name="video"),
    path('page-404/', Http404View.as_view(), name='page_404'),
]
