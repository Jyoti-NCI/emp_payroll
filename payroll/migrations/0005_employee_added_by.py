# Generated by Django 4.2.20 on 2025-03-18 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payroll', '0004_alter_employee_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
