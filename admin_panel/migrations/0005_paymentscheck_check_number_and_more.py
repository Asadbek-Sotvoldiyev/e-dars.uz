# Generated by Django 5.0.4 on 2024-05-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_paymentscheck_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentscheck',
            name='check_number',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='paymentscheck',
            name='check_img',
            field=models.ImageField(upload_to='checks/'),
        ),
    ]
