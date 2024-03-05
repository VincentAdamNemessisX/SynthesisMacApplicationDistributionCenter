from django.db import models


# Create your models here.
class FrontEndUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    head_icon = models.ImageField(upload_to='user', default='user/default_head_icon.ico')
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    state = models.IntegerField(default=1, choices=((1, '正常'), (2, '封禁')))
    role = models.CharField(max_length=50, default='普通用户', choices=(('普通用户', '普通用户'),
                                                                        ('管理员', '管理员'), ('写手', '写手'),
                                                                        ('开发者','开发者'), ('站长', '站长')))

    class Meta:
        db_table = 'front_end_user'
        verbose_name = '前台用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
