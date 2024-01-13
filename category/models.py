from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = '软件分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
