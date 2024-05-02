from django.views.generic import ListView, View, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import StudentProfileForm, PaymentsCheckForm
from admin_panel.models import STUDENT, WAIT
from .mixins import IsStudentMixin
from admin_panel.models import Lesson, Course, Payments, PaymentsCheck
import random


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
        payments = Payments.objects.filter(student__id=request.user.id)
        return render(request, 'student_panel/payments.html', {'payments': payments, 'title' : 'To\'lovlar'})


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
        lessons = Lesson.objects.filter(course_id=course_id)
        return lessons  # faqat lessons ro'yxatini qaytarish kerak

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        video_id = self.kwargs['video_id']
        lessons = Lesson.objects.filter(course_id=course_id)
        video = lessons[0]
        if not video_id == 0:
            video = lessons.get(id=video_id)
        context['title'] = "Videolar"
        context['video'] = video
        return context



class StudentProfileView(IsStudentMixin, View):
    def get(self, request):
        form = StudentProfileForm(instance=request.user)
        return render(request, 'student_panel/profile.html', {'form' : form, 'title' : 'Profilim'})
    def post(self, request):
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('student_panel:profile')
        return render(request, 'student_panel/profile.html', {'form' : form, 'title' : 'Profilim'})


class StudentCheck(IsStudentMixin, View):
    def get(self, request):
        payments = Payments.objects.filter(student=request.user)
        form = PaymentsCheckForm(request.POST, request.FILES, instance=request.user)
        return render(request, 'student_panel/send_check.html', {'form' : form, 'title' : 'To\'lov qilish', 'payments' : payments})
    
    def post(self, request):
        payments = Payments.objects.filter(student=request.user)  
        form = PaymentsCheckForm(request.POST, request.FILES)
        if form.is_valid():
            check_img = request.FILES.get('check_img')
            amount = request.POST.get('amount')
            if check_img:
                payment = Payments.objects.create(
                    amount = amount,
                    check_number = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)]),
                    student=request.user,
                    check_img=check_img,
                    status=WAIT
                )
                payment.save()
                return redirect(reverse_lazy('student_panel:payments'))
            else:
                form.add_error('check_img', 'Iltimos, tasdiqlovchi rasmni yuklang')
        return render(request, 'student_panel/send_check.html', {'form' : form, 'title' : 'Cheklar', 'payments' : payments})





class Http404View(View):
    def get(self, request):
        return render(request, 'page_404.html')
