from django.db import models
import bs4

# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)
    content = models.TextField()
    correlation_article = models.ForeignKey('Article', on_delete=models.CASCADE, null=True, blank=True)
    correlation_software = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)
    state = models.IntegerField(default=1, choices=((1, '待审核'), (2, '正常'), (3, '拒绝')))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def short_content(self):
        max_length = 20
        if len(self.content) > max_length:
            return f"{self.content[:max_length]}..."
        return self.content

    class Meta:
        ordering = ['-created_time']
        verbose_name = '评论审核中心'
        verbose_name_plural = verbose_name
        unique_together = ('correlation_article', 'correlation_software')

    def __str__(self):
        return self.content


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.ImageField(upload_to='article', default='article/default.png')
    correlation_software = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)
    state = models.IntegerField(default=1, choices=((1, '待审核'), (2, '正常'), (3, '拒绝')))
    view_volume = models.BigIntegerField(default=0)
    thumbs_volume = models.BigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def short_title(self):
        max_length = 15
        if len(self.title) > max_length:
            return f"{self.title[:max_length]}..."
        return self.title

    def plain_content(self):
        soup = bs4.BeautifulSoup(self.content, 'html.parser')
        return soup.get_text()

    def short_content(self):
        max_length = 20
        if len(self.plain_content()) > max_length:
            return f"{self.plain_content()[:max_length]}..."
        return self.plain_content()

    class Meta:
        ordering = ['-updated_time']
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name
        unique_together = ('title', 'correlation_software')

    def __str__(self):
        return self.title
