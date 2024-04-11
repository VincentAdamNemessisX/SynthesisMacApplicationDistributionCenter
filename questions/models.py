import jieba
from django.db import models
from frontenduser.models import FrontEndUser


# Create your models here.
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    state = models.IntegerField(default=2, choices=((1, '已解决'), (2, '待解决')))
    publisher = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def title(self):
        t = jieba.cut(self.question, cut_all=False)
        try:
            t1 = next(t) + next(t) + next(t)
        except StopIteration:
            t1 = self.question[:5]
        return t1

    def short_question(self):
        max_length = 40
        if len(self.question) > max_length:
            return f"{self.question[:max_length]}..."
        return self.question

    class Answer(models.Model):
        id = models.AutoField(primary_key=True)
        question = models.ForeignKey('Questions', on_delete=models.CASCADE)
        content = models.TextField()
        respondent = models.ForeignKey(FrontEndUser, on_delete=models.CASCADE)
        is_adopt = models.IntegerField(default=0, choices=((0, '未采纳'), (1, '已采纳')))
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
        return self.title()
