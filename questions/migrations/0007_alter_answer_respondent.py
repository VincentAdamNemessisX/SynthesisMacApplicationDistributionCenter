# Generated by Django 3.2.23 on 2024-04-11 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0016_recentbrowsing'),
        ('questions', '0006_rename_init_questions_questions_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontenduser.frontenduser'),
        ),
    ]
