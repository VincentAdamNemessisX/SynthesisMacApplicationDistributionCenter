# Generated by Django 3.2.23 on 2024-02-24 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0003_alter_frontenduser_head_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontenduser',
            name='role',
            field=models.CharField(default='普通用户', max_length=50),
        ),
    ]