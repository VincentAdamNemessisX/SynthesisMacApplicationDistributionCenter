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
        comments = list(Comment.objects.filter(state=2)
                        .select_related('user', 'correlation_article', 'correlation_software')
                        .order_by('-created_time'))
        cache.set('comments', comments, 60)
    return cache.get('comments')


def get_article():
    articles = cache.get('articles')
    if articles is None:
        articles = list(Article.objects.filter(state=2).select_related('user').order_by('-created_time'))
        cache.set('articles', articles, 60)
    return cache.get('articles')


def get_software(id=None):
    software = cache.get('software')
    if software is None:
        if id is None:
            cache.set('software', None, 2)
        else:
            software = list(SoftWare.objects.filter(id=int(id), state=2)
                            .select_related('user', 'category')
                            .prefetch_related('softwarescreenshots_set'))
            cache.set('software', software, 2)
    elif id and len(software) > 0 and software[0].id != int(id):
        software = list(SoftWare.objects.filter(id=int(id), state=2)
                        .select_related('user', 'category')
                        .prefetch_related('softwarescreenshots_set'))
        cache.set('software', software, 2)
    return cache.get('software')


def get_softwares():
    softwares = cache.get('softwares')
    if softwares is None:
        softwares = list(SoftWare.objects.filter(state=2)
                         .select_related('user', 'category')
                         .prefetch_related('softwarescreenshots_set')
                         .order_by('-update_date'))
        cache.set('softwares', softwares, 180)
    return cache.get('softwares')
