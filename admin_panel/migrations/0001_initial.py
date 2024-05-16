# Generated by Django 5.0.4 on 2024-05-16 04:35

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='user_images/')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('user_role', models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('admin', 'admin')], max_length=31)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('lesson_day', models.CharField(choices=[('Du-Chor-Ju', 'Du-Chor-Ju'), ('Se-Pay-Shan', 'Se-Pay-Shan')], max_length=15)),
                ('lesson_time', models.CharField(choices=[('8:00 - 10:00', '8:00 - 10:00'), ('13:00 - 15:00', '13:00 - 15:00'), ('16:00 - 18:00', '16:00 - 18:00')], max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('duration', models.CharField(choices=[('5 oy', '5 oy'), ('8 oy', '8 oy'), ('6 oy', '6 oy')], max_length=10)),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='admin_panel.coursecategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('video', models.FileField(blank=True, null=True, upload_to='lesson_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'wmv'])])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='admin_panel.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('check_number', models.CharField(blank=True, max_length=4, null=True)),
                ('amount', models.FloatField()),
                ('payment_type', models.CharField(choices=[('Naqd pul', 'Naqd pul'), ('Kartadan', 'Kartadan')], default='Kartadan', max_length=50)),
                ('check_img', models.ImageField(blank=True, null=True, upload_to='checks/')),
                ('status', models.CharField(choices=[('Kutayotgan', 'Kutayotgan'), ('Qaytarilgan', 'Qaytarilgan'), ('Tasdiqlangan', 'Tasdiqlangan')], default='Kutayotgan', max_length=14)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentsCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('check_number', models.CharField(blank=True, max_length=4, null=True)),
                ('check_img', models.ImageField(upload_to='checks/')),
                ('status', models.CharField(choices=[('Kutayotgan', 'Kutayotgan'), ('Tasdiqlangan', 'Tasdiqlangan')], default='Kutayotgan', max_length=16)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentsCheck', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
