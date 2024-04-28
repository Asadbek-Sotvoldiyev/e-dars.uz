from django.contrib.auth.mixins import UserPassesTestMixin
from admin_panel.models import STUDENT
from django.urls import reverse_lazy
from django.shortcuts import redirect


class IsStudentMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == STUDENT

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("admin_panel:login"))
        else:
            return redirect(reverse_lazy('student_panel:page_404'))
