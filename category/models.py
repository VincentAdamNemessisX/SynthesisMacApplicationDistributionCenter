from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=True)
    icon = models.ImageField(upload_to='category/icons/', null=True)
    description = models.TextField(blank=True, null=True)
    state = models.IntegerField(default=2, choices=((1, '停用'), (2, '正常')), db_index=True)

    def short_name(self):
        max_length = 15
        if len(self.name) > max_length:
            return f"{self.name[:max_length]}..."
        return self.name

    def short_description(self):
        max_length = 20
        if len(self.description) > max_length:
            return f"{self.description[:max_length]}..."
        return self.description

    class Meta:
        verbose_name = '软件分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
