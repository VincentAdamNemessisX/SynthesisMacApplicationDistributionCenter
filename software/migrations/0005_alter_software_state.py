# Generated by Django 3.2.24 on 2024-05-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0004_alter_software_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='state',
            field=models.IntegerField(choices=[(1, '未审核'), (2, '已上架'), (3, '已下架'), (4, '不展示')], default=1),
        ),
    ]
