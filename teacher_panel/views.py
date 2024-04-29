from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView

from admin_panel.models import Lesson, Course
from .forms import *
from .mixins import IsTeacherMixin


class TeacherDashboard(IsTeacherMixin, View):
    def get(self, request):
        return render(request, 'teacher_panel/index.html')





class TeacherLesson(IsTeacherMixin, ListView):
    model = Lesson
    template_name = 'teacher_panel/lesson.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['title'] = "Videolar"
        context['course_id'] = course_id
        return context



class TeacherCourses(IsTeacherMixin, View):
    def get(self, request):
        courses = Course.objects.annotate(student_count=Count('students'))
        tr = {}
        i = 1
        for course in courses:
            tr[course.id] = i
            i += 1
        data = {
            'courses': courses,
            'tr': tr,
            'title': 'Kurslar'
        }
        return render(request, 'teacher_panel/kurslar.html', context=data)


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


class AddLessonView(IsTeacherMixin, View):
    def get(self, reqeust, course_id):
        form = LessonForm()
        return render(reqeust, 'teacher_panel/add_lesson.html', {'form': form, 'title': "Dars qo'shish", 'course_id':course_id})

    def post(self, request, course_id):
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('teacher_panel:lesson', kwargs={'course_id':course_id}))

        return render(request, 'teacher_panel/add_lesson.html', {'form': form, 'title': "Dars qo'shish", 'course_id':course_id})