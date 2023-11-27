from django.db import models


# Create your models here.
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question
