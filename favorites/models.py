from django.db import models


# Create your models here.
class Favorites(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=(('article', 'article'), ('app', 'app')))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return str(self.id)
