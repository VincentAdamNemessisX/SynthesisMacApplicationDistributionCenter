# Generated by Django 3.2.23 on 2024-03-17 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_rename_question_state_questions_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='question',
            new_name='question',
        ),
    ]
