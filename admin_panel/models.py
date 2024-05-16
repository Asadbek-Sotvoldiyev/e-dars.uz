from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

STUDENT, TEACHER, ADMIN = ('student', 'teacher', 'admin')
MALE, FEMALE = ('male', 'female')
ODD_DAYS, EVEN_DAYS = ('Du-Chor-Ju', 'Se-Pay-Shan')
MORNING, AFTERNOON, EVENING = ('8:00 - 10:00', '13:00 - 15:00', '16:00 - 18:00')
FOUNDATION, STANDART, RESULT = ('5 oy', '8 oy', '6 oy')
WAIT,  UNCORFIRMED, PAID = ('Kutayotgan', 'Qaytarilgan', 'Tasdiqlangan')
CASHE, CARD = ('Naqd pul', 'Kartadan')


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    USER_ROLES = (
        (STUDENT, STUDENT),
        (TEACHER, TEACHER),
        (ADMIN, ADMIN)
    )
    GENDERS = (
        (MALE, MALE),
        (FEMALE, FEMALE)
    )

    image = models.ImageField(upload_to='user_images/', default='default.jpg', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
    user_role = models.CharField(max_length=31, choices=USER_ROLES)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDERS)


class CourseCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(BaseModel):
    DAYS = (
        (ODD_DAYS, ODD_DAYS),
        (EVEN_DAYS, EVEN_DAYS)
    )
    TIMES = (
        (MORNING, MORNING),
        (AFTERNOON, AFTERNOON),
        (EVENING, EVENING)
    )
    DURATION = (
        (FOUNDATION, FOUNDATION),
        (STANDART, STANDART),
        (RESULT, RESULT),
    )

    name = models.CharField(max_length=50)
    lesson_day = models.CharField(max_length=15, choices=DAYS)
    lesson_time = models.CharField(max_length=30, choices=TIMES)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(User)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    duration = models.CharField(max_length=10, choices=DURATION)

    def __str__(self):
        return f"Course: {self.name}, Teacher: {self.teacher}"


class Lesson(BaseModel):
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='lesson_videos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=["mp4", 'wmv'])])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.name


class Payments(BaseModel):
    TYPE = (
        (CASHE, CASHE),
        (CARD, CARD),
    )
    STATUS = (
        (WAIT, WAIT),
        (UNCORFIRMED, UNCORFIRMED),
        (PAID, PAID),
    )
    check_number = models.CharField(max_length=4, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField(null=False, blank=False)
    payment_type = models.CharField(max_length=50, null=False, blank=False, choices=TYPE, default=CARD)
    check_img = models.ImageField(upload_to='checks/', blank=True, null=True)

    status = models.CharField(max_length=14, null=False, blank=False, choices=STATUS, default=WAIT)
    
    def __str__(self):
        return f"Id: {self.id}; Student: {self.student.first_name} {self.student.last_name}"
    
    
class PaymentsCheck(BaseModel, models.Model):
    STATUS = (
        (WAIT, WAIT),
        (PAID, PAID),
    )
    check_number = models.CharField(max_length=4, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paymentsCheck')
    check_img = models.ImageField(upload_to='checks/', blank=False, null=False)
    status = models.CharField(max_length=16, blank=False, null=False, choices=STATUS, default=WAIT)

    def __str__(self):
        return f"{self.id}: {self.student.first_name} {self.student.last_name} ({self.status})"