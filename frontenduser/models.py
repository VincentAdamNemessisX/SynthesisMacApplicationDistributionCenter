from django.db import models


# Create your models here.
class FrontEndUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        db_table = 'front_end_user'
        verbose_name = 'Front End User'
        verbose_name_plural = 'Front End Users'

    def __str__(self):
        return self.username
