# Generated by Django 3.2.23 on 2024-03-17 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0013_alter_frontenduser_django_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontenduser',
            name='user_center_cover',
            field=models.ImageField(default='/static/user_center/img/thumbnail-lg.svg', upload_to='user'),
        ),
    ]
