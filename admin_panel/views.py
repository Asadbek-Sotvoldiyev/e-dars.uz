from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView
from .models import Course, User, TEACHER, STUDENT, ADMIN, Payments, PAID, UNCORFIRMED, Lesson
from .forms import AdminProfileForm, LoginForm, UserForm, PaymentsForm, AddStudentToCourseForm
from django.contrib.auth import authenticate, login, logout
from .mixins import IsAdminMixin
import random


class AdminDashboardView(IsAdminMixin, View):
    course_count = Course.objects.all()
    student_count = User.objects.filter(user_role=STUDENT)
    teacher_count = User.objects.filter(user_role=TEACHER)
    data = {
        'course_count': course_count,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'title': "Bosh sahifa",
    }

    def get(self, request):
        return render(request, 'admin_panel/index.html', {'title': "Bosh sahifa"} )


class AdminReytingView(IsAdminMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/reyting.html', {'title': "Reyting", 'son' : range(1,11)})


class AdminMoliyaView(IsAdminMixin, View):
    def get(self, request):
        payments = Payments.objects.all()
        return render(request, 'admin_panel/moliya.html', {'title' : "Moliya", 'payments': payments})


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


class AddTeacherView(IsAdminMixin, View):
    def get(self, reqeust):
        form = UserForm()
        return render(reqeust, 'admin_panel/add_teacher.html', {'form': form, 'title': "O'qituvchi qo'shish"})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']

            teacher = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                user_role=TEACHER,
                phone=phone,
                gender=gender
            )
            teacher.set_password(phone[1:])
            teacher.save()
            return redirect(reverse_lazy('admin_panel:teachers'))

        return render(request, 'admin_panel/add_teacher.html', {'form': form, 'title': "O'qituvchi qo'shish"})


class AddStudentView(IsAdminMixin, View):
    def get(self, reqeust):
        form = UserForm()
        return render(reqeust, 'admin_panel/add_student.html', {'form': form, 'title': "O'quvchi qo'shish"})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']

            teacher = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                user_role=STUDENT,
                phone=phone,
                gender=gender
            )
            teacher.set_password(phone[1:])
            teacher.save()
            return redirect(reverse_lazy('admin_panel:students'))

        return render(request, 'admin_panel/add_student.html', {'form': form, 'title': "O'quvchi qo'shish"})


class StudentPayments(IsAdminMixin, View):
    def get(self, request):
        payments = Payments.objects.all()
        form = PaymentsForm(request.POST, request.FILES, instance=request.user)
        return render(request, 'admin_panel/send_check.html', {'form' : form, 'title' : 'To\'lov qilish', 'payments' : payments})
    
    def post(self, request):
        payments = Payments.objects.all() 
        form = PaymentsForm(request.POST, request.FILES)
        if form.is_valid():
            check_img = request.FILES.get('check_img')
            student = request.POST.get('student')
            student = User.objects.get(id=student)
            amount = request.POST.get('amount')
            if check_img:
                payment = Payments.objects.create(
                    amount = amount,
                    check_number = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)]),
                    student = student,
                    check_img=check_img,
                    status=PAID
                )
                payment.save()
                return redirect(reverse_lazy('admin_panel:moliya'))
            else:
                form.add_error('check_img', 'Iltimos, tasdiqlovchi rasmni yuklang')
        return render(request, 'admin_panel/send_check.html', {'form' : form, 'title' : 'Cheklar', 'payments' : payments})


class PaymentConfirm(IsAdminMixin, View):
    def get(self, request, check_number):
        try:
            payment = Payments.objects.get(check_number=check_number)
        except Payments.DoesNotExist:
            return redirect('admin_panel:moliya')  
        
        payment.status = PAID
        payment.save()

        return redirect('admin_panel:moliya')
   
   
class PaymentUnconfirm(IsAdminMixin, View):
    def get(self,request,check_number):
        try:
            payment = Payments.objects.get(check_number=check_number)
        except Payments.DoesNotExist:
            return redirect('admin_panel:moliya')  
        
        payment.status = UNCORFIRMED
        payment.save()

        return redirect('admin_panel:moliya')     
        

def lesson_detail_video(request):
    return render(request, 'admin_panel/lesson_detail_video.html', {'title': 'Lesson Details Video', 'son': range(0,10 )})


def lesson_detail_students(request):
    return render(request, 'admin_panel/lesson_detail_students.html', {'title': 'Lesson Details Students', 'son': range(0,10 )})


class AdminDarsView(IsAdminMixin, ListView):
    model = Lesson
    template_name = 'admin_panel/lesson_detail_video.html'
    context_object_name = 'lessons'
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        lessons = Lesson.objects.filter(course_id=course_id)
            
        return lessons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['title'] = "Videolar"
        context['course_id'] = course_id
        return context
    
    
class AdminStudentsView(IsAdminMixin, ListView):
    model = Course
    template_name = 'admin_panel/lesson_detail_students.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.prefetch_related('students').get(id=course_id)
        students = course.students.all().prefetch_related()
        
        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['title'] = "O'quvchilar"
        context['course_id'] = course_id
        return context
    


class AddStudentToCourse(IsAdminMixin, View):
    def get(self, request):
        form = AddStudentToCourseForm()
        return render(request, 'admin_panel/addStudentToCourse.html',{'form': form})
    



def logout_user(request):
    logout(request)
    return redirect('admin_panel:login')
