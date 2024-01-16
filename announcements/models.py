from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Announcements(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='announcements', null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.IntegerField(default=0, choices=((0, '全站'), (1, '指定APP')))
    app = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
