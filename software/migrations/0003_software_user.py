# Generated by Django 3.2.15 on 2024-01-21 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0001_initial'),
        ('software', '0002_rename_status_software_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='frontenduser.frontenduser'),
            preserve_default=False,
        ),
    ]