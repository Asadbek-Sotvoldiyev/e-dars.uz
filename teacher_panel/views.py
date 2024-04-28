from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .mixins import IsTeacherMixin


class TeacherDashboard(IsTeacherMixin, View):
    def get(self, request):
        return render(request, 'teacher_panel/index.html')


class TeacherCourses(IsTeacherMixin, View):
    def get(self, request):
        return render(request, 'teacher_panel/kurslar.html')


class TeacherProfileView(IsTeacherMixin, View):
    def get(self, request):
        form = TeacherProfileForm(instance=request.user)
        return render(request, 'teacher_panel/profile.html', {'form': form, 'title': 'Profilim'})

    def post(self, request):
        form = TeacherProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel:profile')
        return render(request, 'teacher_panel/profile.html', {'form': form, 'title': 'Profilim'})