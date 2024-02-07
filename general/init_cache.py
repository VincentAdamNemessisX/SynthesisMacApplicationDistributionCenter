from django.core.cache import cache

from announcements.models import Announcements
from category.models import Category
from commentsWithArticles.models import Comment, Article
from favorites.models import Favorites
from questions.models import Questions
from software.models import SoftWare
from .common_compute import get_hot_volume_of_article, get_hot_volume_of_software


def get_notices():
    notices = cache.get('notices')
    if notices is None:
        notices = list(Announcements.objects.filter().order_by('-created_time'))
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


def get_matched_articles_by_article_id(article_id=None):
    matched_articles = cache.get('article')
    if matched_articles is None:
        if article_id is None:
            cache.set('article', None, 1)
        else:
            matched_articles = list(Article.objects.filter(id=int(article_id), state=2)
                                    .select_related('user'))
            cache.set('article', matched_articles, 1)
    elif article_id and len(matched_articles) > 0 and matched_articles[0].id != int(article_id):
        matched_articles = list(Article.objects.filter(id=int(article_id), state=2)
                                .select_related('user'))
        cache.set('article', matched_articles, 1)
    return cache.get('article')


def get_specific_user_articles_by_username(username=None):
    specific_user_articles = cache.get('specific_user_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_articles', None, 1)
        else:
            specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                          .select_related('user', 'correlation_software')
                                          .order_by('-updated_time'))
            cache.set('specific_user_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                      .select_related('user', 'correlation_software')
                                      .order_by('-updated_time'))
        cache.set('specific_user_articles', specific_user_articles, 1)
    return cache.get('specific_user_articles')


def get_specific_user_favorite_articles_by_username(username=None):
    specific_user_articles = cache.get('specific_user_favorite_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_favorite_articles', None, 1)
        else:
            specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                          .select_related('user', 'correlation_article').filter(
                correlation_article__state=2)
                                          .order_by('-created_time'))
            cache.set('specific_user_favorite_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                      .select_related('user', 'correlation_article').filter(
            correlation_article__state=2)
                                      .order_by('-created_time'))
        cache.set('specific_user_favorite_articles', specific_user_articles, 1)
    return cache.get('specific_user_favorite_articles')


def get_all_favorite_articles():
    favorite_articles = cache.get('favorite_articles')
    if favorite_articles is None:
        favorite_articles = list(Favorites.objects.filter(correlation_type=1, correlation_article__state=2)
                                 .select_related('user', 'correlation_article')
                                 .order_by('-created_time'))
        cache.set('favorite_articles', favorite_articles, 45)
    return cache.get('favorite_articles')


def get_all_articles():
    all_articles = cache.get('all_articles')
    if all_articles is None:
        all_articles = list(Article.objects.filter(state=2)
                            .select_related('user')
                            .order_by('-updated_time'))
        cache.set('all_articles', all_articles, 45)
    return cache.get('all_articles')


def get_software_by_software_id(software_id=None):
    software = cache.get('software')
    if software is None:
        if software_id is None:
            cache.set('software', None, 2)
        else:
            software = list(SoftWare.objects.filter(id=int(software_id), state=2)
                            .select_related('user', 'category')
                            .prefetch_related('softwarescreenshots_set', 'article_set'))
            cache.set('software', software, 2)
    elif software_id and len(software) > 0 and software[0].id != int(software_id):
        software = list(SoftWare.objects.filter(id=int(software_id), state=2)
                        .select_related('user', 'category')
                        .prefetch_related('softwarescreenshots_set', 'article_set'))
        cache.set('software', software, 2)
    return cache.get('software')


def get_all_software():
    all_software = cache.get('all_software')
    if all_software is None:
        all_software = list(SoftWare.objects.filter(state=2)
                            .select_related('user', 'category')
                            .prefetch_related('softwarescreenshots_set')
                            .order_by('-updated_time'))
        cache.set('all_software', all_software, 180)
    return cache.get('all_software')


def get_specific_user_software_by_username(username=None):
    specific_user_software = cache.get('specific_user_software')
    if specific_user_software is None:
        if username is None:
            cache.set('specific_user_software', None, 1)
        else:
            specific_user_software = list(SoftWare.objects.filter(user__username=username, state=2)
                                          .select_related('user', 'category').prefetch_related('article_set')
                                          .order_by('-updated_time'))
            cache.set('specific_user_software', specific_user_software, 1)
    elif username and len(specific_user_software) > 0 and specific_user_software[0].user.username != username:
        specific_user_software = list(SoftWare.objects.filter(user__username=username, state=2)
                                      .select_related('user', 'category').prefetch_related('article_set')
                                      .order_by('-updated_time'))
        cache.set('specific_user_software', specific_user_software, 1)
    return cache.get('specific_user_software')


def get_specific_user_favorite_software_by_username(username=None):
    """
    @param username: 用户名
    @return: 用户收藏的软件
    """
    specific_user_software = cache.get('specific_user_favorite_software')
    if specific_user_software is None:
        if username is None:
            cache.set('specific_user_software', None, 1)
        else:
            specific_user_software = list(Favorites.objects.filter(user__username=username, state=2)
                                          .select_related('user', 'category', 'correlation_software')
                                          .prefetch_related('article_set')
                                          .order_by('-updated_time'))
            cache.set('specific_user_favorite_software', specific_user_software, 1)
    elif username and len(specific_user_software) > 0 and specific_user_software[0].user.username != username:
        specific_user_software = list(Favorites.objects.filter(user__username=username, state=2)
                                      .select_related('user', 'category', 'correlation_software')
                                      .prefetch_related('article_set')
                                      .order_by('-updated_time'))
        cache.set('specific_user_favorite_software', specific_user_software, 1)
    return cache.get('specific_user_favorite_software')


def get_all_favorite_software():
    all_favorite_software = cache.get('favorite_software')
    if all_favorite_software is None:
        all_favorite_software = list(Favorites.objects.filter(correlation_type=2, correlation_software__state=2)
                                     .select_related('user', 'correlation_software')
                                     .order_by('-created_time'))
        cache.set('favorite_software', all_favorite_software, 45)
    return cache.get('favorite_software')


def get_all_questions():
    all_questions = cache.get('all_questions')
    if all_questions is None:
        all_questions = list(Questions.objects.all()
                             .select_related('publisher')
                             .order_by('updated_time')
                             )
        cache.set('all_questions', all_questions, 45)
    return cache.get('all_questions')


def get_all_category():
    categories = cache.get('categories')
    if categories is None:
        categories = list(Category.objects.filter(state=2).order_by('id').prefetch_related('software_set'))
        cache.set('categories', categories, 180)
    return cache.get('categories')


def get_hot_articles_and_software():
    hot_articles = cache.get('hot_articles')
    hot_software = cache.get('hot_software')
    if hot_articles is None:
        hot_articles = list(Article.objects.filter(state=2))
        for article in hot_articles:
            article.hot_volume = get_hot_volume_of_article(article.id)
        hot_articles.sort(key=lambda x: x.hot_volume, reverse=True)
        cache.set('hot_articles', hot_articles[:10], 1)
    if hot_software is None:
        hot_software = list(SoftWare.objects.filter(state=2))
        for software in hot_software:
            software.hot_volume = get_hot_volume_of_software(software.id)
        hot_software.sort(key=lambda x: x.hot_volume, reverse=True)
        cache.set('hot_software', hot_software[:10], 1)
    return cache.get('hot_articles'), cache.get('hot_software')

