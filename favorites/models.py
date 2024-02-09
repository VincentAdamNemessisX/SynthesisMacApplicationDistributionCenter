from django.db import models


# Create your models here.
class Favorites(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE, null=True)
    correlation_type = models.IntegerField(default=1, choices=((1, '文章'), (2, '软件')))
    correlation_article = models.ForeignKey('commentswitharticles.Article', on_delete=models.CASCADE, null=True, blank=True)
    correlation_software = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'correlation_software'), ('user', 'correlation_article'))

    def __str__(self):
        return str(self.id)
