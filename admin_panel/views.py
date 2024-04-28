from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View, CreateView
from .models import Course, User, TEACHER, STUDENT, ADMIN
from .forms import AdminProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .mixins import IsAdminMixin


class AdminDashboardView(IsAdminMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/index.html', {'title': "Bosh sahifa"})


class AdminReytingView(IsAdminMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/reyting.html', {'title': "Reyting", 'son' : range(1,11)})


class AdminMoliyaView(IsAdminMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/moliya.html', {'title' : "Moliya"})


class CourseListView(IsAdminMixin, ListView):
    queryset = Course.objects.all()
    template_name = 'admin_panel/courses.html'
    context_object_name = 'courses'

    extra_context = {'title': "Kurslar"}


class TeacherListView(IsAdminMixin, ListView):
    queryset = User.objects.filter(user_role=TEACHER)
    template_name = 'admin_panel/teachers.html'
    context_object_name = 'teachers'

    extra_context = {'title': "O'qituvchilar"}
   
    
class StudentListView(IsAdminMixin, ListView):
    queryset = User.objects.filter(user_role=STUDENT)
    template_name = 'admin_panel/students.html'
    context_object_name = 'students'

    extra_context = {'title': "O'quvchilar"}


class AdminProfileView(IsAdminMixin, View):
    def get(self, request):
        form = AdminProfileForm(instance=request.user)
        return render(request, 'admin_panel/profile.html', {'form': form, 'title': 'Profilim'})
    def post(self, request):
        form = AdminProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:profile')
        return render(request, 'admin_panel/profile.html', {'form': form, 'title': 'Profilim'})


class AdminLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'admin_panel/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_role == STUDENT:
                    return redirect('student_panel:dashboard')
                elif user.user_role == ADMIN:
                    return redirect('admin_panel:dashboard')
                elif user.user_role == TEACHER:
                    return redirect('teacher_panel:dashboard')
        return render(request, 'admin_panel/login.html', {'form': form})


class AddCourseView(CreateView):
    model = Course
    template_name = 'admin_panel/add_course.html'
    success_url = reverse_lazy('admin_panel:courses')
    fields = ('name', 'lesson_day', 'lesson_time', 'category', 'teacher', 'students', 'price', 'duration')

    extra_context = {
        'title': "Kurs qo'shish"
    }


class AddTeacherView(CreateView):
    model = User
    template_name = 'admin_panel/add_teacher.html'
    success_url = reverse_lazy('admin_panel:teachers')
    fields = ('first_name', 'last_name', 'username', 'image', 'phone', 'user_role', 'birthday', 'gender')

    extra_context = {
        'title': "O'qituvchi qo'shish"
    }
