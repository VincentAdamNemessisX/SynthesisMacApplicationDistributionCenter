# Generated by Django 3.2.23 on 2024-01-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_alter_answer_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
