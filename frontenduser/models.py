from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class FrontEndUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    head_icon = models.ImageField(upload_to='user', default='user/default_head_icon.ico')
    user_center_cover = models.ImageField(upload_to='user/user_center', default='user/user_center/default.svg')
    description = models.TextField(null=True, blank=True)
    django_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    state = models.IntegerField(default=1, choices=((1, '封禁'), (2, '正常')))
    role = models.CharField(max_length=50, default='普通用户', choices=(('普通用户', '普通用户'),
                                                                        ('管理员', '管理员'), ('写手', '写手'),
                                                                        ('开发者', '开发者'), ('站长', '站长')))

    def short_description(self):
        if self.description:
            if len(self.description) > 30:
                return self.description[:30] + '...'
            else:
                return self.description
        else:
            return '无'

    class RecentBrowsing(models.Model):
        id = models.AutoField(primary_key=True)
        user = models.ForeignKey('FrontEndUser', on_delete=models.CASCADE)
        article = models.ForeignKey('commentswitharticles.Article', on_delete=models.CASCADE, null=True, blank=True)
        software = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)
        browsing_time = models.DateTimeField(auto_now=True)

        class Meta:
            db_table = 'recent_browsing'
            verbose_name = '最近浏览'
            verbose_name_plural = verbose_name

    class Meta:
        db_table = 'front_end_user'
        verbose_name = '前台用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
