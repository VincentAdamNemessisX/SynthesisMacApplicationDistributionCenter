# Generated by Django 3.2.23 on 2024-02-29 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_answer_created_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='question_state',
            new_name='state',
        ),
    ]
