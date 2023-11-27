from django.db import models


# Create your models here.
class SoftWare(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='software')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Software'
        verbose_name_plural = 'Softwares'

    def __str__(self):
        return self.name
