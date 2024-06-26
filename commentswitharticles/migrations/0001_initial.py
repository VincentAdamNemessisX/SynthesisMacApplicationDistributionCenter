# Generated by Django 3.2.15 on 2024-01-30 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('state', models.IntegerField(choices=[(1, '待审核'), (2, '正常'), (3, '拒绝')], default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
                'ordering': ['-updated_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('state', models.IntegerField(choices=[(1, '待审核'), (2, '正常'), (3, '拒绝')], default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('correlation_article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commentswitharticles.article')),
            ],
            options={
                'verbose_name': '评论审核中心',
                'verbose_name_plural': '评论审核中心',
                'ordering': ['-created_time'],
            },
        ),
    ]
