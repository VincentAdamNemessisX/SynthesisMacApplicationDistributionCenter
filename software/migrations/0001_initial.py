# Generated by Django 3.2.15 on 2024-01-30 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('frontenduser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftWare',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200, null=True)),
                ('language', models.CharField(max_length=200, null=True)),
                ('platform', models.CharField(max_length=200, null=True)),
                ('run_os_version', models.CharField(max_length=200, null=True)),
                ('description', models.TextField()),
                ('official_link', models.URLField(blank=True, null=True)),
                ('link_adrive', models.URLField(blank=True, null=True)),
                ('link_baidu', models.URLField(blank=True, null=True)),
                ('link_direct', models.URLField(blank=True, null=True)),
                ('link_123', models.URLField(blank=True, null=True)),
                ('icon', models.ImageField(upload_to='software')),
                ('state', models.IntegerField(choices=[(1, '未审核'), (2, '已审核'), (3, '已下架')], default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontenduser.FrontEndUser')),
            ],
            options={
                'verbose_name': '软件管理',
                'verbose_name_plural': '软件管理',
                'ordering': ['-updated_time'],
            },
        ),
        migrations.CreateModel(
            name='SoftwareScreenShots',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='software/screenshots')),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.software')),
            ],
            options={
                'verbose_name': '软件截图管理',
                'verbose_name_plural': '软件截图管理',
            },
        ),
    ]