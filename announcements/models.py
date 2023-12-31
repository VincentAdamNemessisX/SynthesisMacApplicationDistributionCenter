from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Announcements(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # author = models.CharField(max_length=100)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title
