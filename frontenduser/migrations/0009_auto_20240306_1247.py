# Generated by Django 3.2.23 on 2024-03-06 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontenduser', '0008_frontenduser_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frontenduser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='frontenduser',
            name='password',
        ),
        migrations.AddField(
            model_name='frontenduser',
            name='django_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]