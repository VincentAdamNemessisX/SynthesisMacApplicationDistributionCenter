# Generated by Django 3.2.23 on 2024-02-22 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentswitharticles', '0003_auto_20240208_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover',
            field=models.ImageField(default='article/default.jpg', upload_to='article'),
        ),
    ]
