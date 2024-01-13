from django.db import models


# Create your models here.
class FrontEndUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        db_table = 'front_end_user'
        verbose_name = '前台用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
