from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('student_panel.urls')),
    path('superadmin/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('student/', include('student_panel.urls'), name='student_panel'),
    path('teacher/', include('teacher_panel.urls'), name='teacher_panel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
