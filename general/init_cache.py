from django.core.cache import cache

from announcements.models import Announcements
from commentsWithArticles.models import Comment, Article
from software.models import SoftWare


def get_notices():
    notices = cache.get('notices')
    if notices is None:
        notices = list(Announcements.objects.all().order_by('-date'))
        cache.set('notices', notices, 600)
    return cache.get('notices')


def get_comments():
    comments = cache.get('comments')
    if comments is None:
        comments = list(Comment.objects.filter(state=2).select_related('user').order_by('-created_time'))
        cache.set('comments', comments, 60)
    return cache.get('comments')


def get_articles():
    articles = cache.get('articles')
    if articles is None:
        articles = list(Article.objects.filter(state=2).select_related('user').order_by('-created_time'))
        cache.set('articles', articles, 60)
    return cache.get('articles')


def get_software(id=None):
    softwares = cache.get('softwares')
    if softwares is None:
        if id is None:
            softwares = list(SoftWare.objects.filter(state=2).select_related('category', 'user').order_by('-create_date'))
            cache.set('softwares', softwares, 180)
        else:
            softwares = list(SoftWare.objects.filter(id=int(id)).select_related('category', 'user'))
            cache.set('softwares', softwares, 60)
    return cache.get('softwares')
