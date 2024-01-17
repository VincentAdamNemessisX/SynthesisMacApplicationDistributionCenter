from django.db import models


# Create your models here.
class SoftWare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=200, null=True)
    platform = models.CharField(max_length=200, null=True)
    run_os_version = models.CharField(max_length=200, null=True)
    description = models.TextField()
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, null=True)
    official_link = models.URLField(null=True, blank=True)
    link_adrive = models.URLField(null=True, blank=True)
    link_baidu = models.URLField(null=True, blank=True)
    link_direct = models.URLField(null=True, blank=True)
    link_123 = models.URLField(null=True, blank=True)
    icon = models.ImageField(upload_to='software')
    status = models.IntegerField(default=1, choices=((1, '未审核'), (2, '已审核'), (3, '已下架')))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class SoftwareScreenShots(models.Model):
        id = models.AutoField(primary_key=True)
        software = models.ForeignKey('SoftWare', on_delete=models.CASCADE)
        image = models.ImageField(upload_to='software/screenshots')

        class Meta:
            verbose_name = '软件截图管理'
            verbose_name_plural = verbose_name

        def __str__(self):
            return self.software.name

    class Meta:
        ordering = ['-update_date']
        verbose_name = '软件管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
