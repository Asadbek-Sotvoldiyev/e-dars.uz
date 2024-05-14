from django.contrib.auth.mixins import UserPassesTestMixin
from admin_panel.models import ADMIN, STUDENT, TEACHER
from django.urls import reverse_lazy
from django.shortcuts import redirect
from admin_panel.models import  User


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == ADMIN

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("admin_panel:login"))
        else:
            if self.request.user.user_role == STUDENT:
                return redirect(reverse_lazy('student_panel:dashboard'))
            else:
                return redirect(reverse_lazy('teacher_panel:dashboard'))
