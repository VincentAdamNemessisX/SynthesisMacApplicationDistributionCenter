from django.core.cache import cache

from comments_with_articles.models import *


def get_comments():
    comments = cache.get('comments')
    if comments is None:
        comments = list(Comment.objects.filter(state=2).select_related('user').order_by('-created_time'))
        cache.set('comments', comments, 60)
    return comments


def get_articles():
    articles = cache.get('articles')
    if articles is None:
        articles = list(Article.objects.filter(state=2).select_related('user').order_by('-created_time'))
        cache.set('articles', articles, 60)
    return articles
