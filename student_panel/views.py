from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import StudentProfileForm
from admin_panel.models import STUDENT
from .mixins import IsStudentMixin
from admin_panel.models import Lesson, Course


class StudentDashboardView(IsStudentMixin, View):
    def get(self, request):
        return render(request, 'student_panel/index.html')


class StudentKurslarView(IsStudentMixin, View):
    def get(self, request):
        courses = Course.objects.filter(students__id=request.user.id)
        tr = {}
        i = 1
        for course in courses:
            tr[course.id] = i
            i += 1
        data = {
            'courses': courses,
            'tr': tr
        }
        return render(request, 'student_panel/kurslar.html', context=data)


class StudentPaymentsView(IsStudentMixin, View):
    def get(self, request):
        return render(request, 'student_panel/payments.html')


class StudentReytingView(IsStudentMixin, View):
    def get(self, request):
        return render(request, 'student_panel/reyting.html', {'title': "Reyting", 'son': range(1,11)})


class StudentMessageView(IsStudentMixin, View):
    def get(self, request):
        return render(request, 'student_panel/message.html', {'title': "Xabar yuborish"})


class StudentDarsView(IsStudentMixin, ListView):
    model = Lesson
    template_name = 'student_panel/dars.html'
    context_object_name = 'lessons'
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)

    extra_context = {'title': "Videolar"}


class StudentProfileView(IsStudentMixin, View):
    def get(self, request):
        form = StudentProfileForm(instance=request.user)
        return render(request, 'student_panel/profile.html', {'form': form, 'title': 'Profilim'})
    def post(self, request):
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('student_panel:profile')
        return render(request, 'student_panel/profile.html', {'form': form, 'title': 'Profilim'})


class Http404View(View):
    def get(self, request):
        return render(request, 'page_404.html')
