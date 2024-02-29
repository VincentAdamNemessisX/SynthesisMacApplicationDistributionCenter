from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=10000)
    state = models.IntegerField(default=2, choices=((1, '已解决'), (2, '待解决')))
    publisher = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def short_question(self):
        max_length = 20
        if len(self.question) > max_length:
            return f"{self.question[:max_length]}..."
        return self.question

    class Answer(models.Model):
        id = models.AutoField(primary_key=True)
        question = models.ForeignKey('Questions', on_delete=models.CASCADE)
        content = models.TextField()
        respondent = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
        created_time = models.DateTimeField(auto_now_add=True, null=True)

        def short_content(self):
            max_length = 20
            if len(self.content) > max_length:
                return f"{self.content[:max_length]}..."
            return self.content

        class Meta:
            verbose_name = '回复中心'
            verbose_name_plural = verbose_name

        def __str__(self):
            return str(self.id)

    class Meta:
        ordering = ['-created_time']
        verbose_name = '反馈中心'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
