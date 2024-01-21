from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Announcements(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='announcements', null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.IntegerField(default=1, choices=((1, '全站'), (2, '指定APP')))
    app = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # 如果没有指定 author，就使用当前登录的后台用户
        if not self.author:
            self.author = kwargs.pop('request').user
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
