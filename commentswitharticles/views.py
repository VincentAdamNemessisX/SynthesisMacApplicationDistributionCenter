# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django_router import router
from general.encrypt import decrypt, encrypt
from commentswitharticles.models import Article
from general.init_cache import (get_comments,
                                get_matched_articles_by_article_id as g_a,
                                get_all_articles as g_as, get_hot_articles_and_software)


@router.path(pattern='api/get/init/comments/')
@require_http_methods('POST')
def get_init_comments(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            # filter specifc article or software
            try:
                post_data = json.loads(request.body)
                query_id = decrypt(post_data['query_id'].replace(' ', '+'))
                type = post_data['type']
            except ValueError:
                return JsonResponse({
                    'code': 402,
                    'msg': 'failed with invalid params'
                })
            except TypeError:
                return JsonResponse({
                    'code': 407,
                    'msg': 'failed with wrong params'
                })
            except AttributeError:
                return JsonResponse({
                    'code': 401,
                    'msg': 'failed with bad request body'
                })
            if type == 'article':
                comments = [comment for comment in comments if comment.correlation_article.id == int(query_id)]
            if type == 'software':
                comments = [comment for comment in comments if comment.correlation_software.id == int(query_id)]
            comments = comments[:10]
            comments = [
                {
                    'comment_id': encrypt(str(comment.id)).decode('utf-8'),
                    'user': {
                        'user_id': encrypt(str(comment.user.id)).decode('utf-8'),
                        'username': comment.user.nickname if comment.user.nickname else comment.user.username,
                        'head_icon': comment.user.head_icon.url,
                        'role': comment.user.role,
                    },
                    'content': comment.content,
                    'correlation_article': comment.correlation_article.title if comment.correlation_article else '',
                    'correlation_software': comment.correlation_software.name if comment.correlation_software else '',
                    'created_time': comment.created_time.strftime("%a, %d %b %Y %I:%M:%S%z"),
                    'parent_id': encrypt(str(comment.parent.id)).decode('utf-8') if comment.parent else encrypt(str(0)).decode('utf-8')
                }
                for comment in comments
            ]
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'comments': comments
                }
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data',
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@login_required
@router.path(pattern='api/load/more/comments/')
@require_POST
def load_more_comments(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            # filter anything, just like specifc article or software
            try:
                post_data = json.loads(request.body)
                query_id = decrypt(post_data['query_id'].encode())
                type = post_data['type']
            except ValueError:
                return JsonResponse({
                    'code': 402,
                    'msg': 'failed with invalid params'
                })
            except TypeError:
                return JsonResponse({
                    'code': 407,
                    'msg': 'failed with wrong params'
                })
            except AttributeError:
                return JsonResponse({
                    'code': 401,
                    'msg': 'failed with bad request body'
                })
            if type == 'article':
                comments = [comment for comment in comments if comment.correlation_article.id == int(query_id)]
            if type == 'software':
                comments = [comment for comment in comments if comment.correlation_software.id == int(query_id)]
            if len(comments) < 10:
                comments = None
            else:
                comments = comments[10:]
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if comments:
            if comments:
                comments = [
                    {
                        'id': comment.id,
                        'user': comment.user.username,
                        'content': comment.content,
                        'correlation_model': comment.correlation_model,
                        'correlation_article': comment.correlation_article,
                        'correlation_software': comment.correlation_software,
                        'created_time': comment.created_time,
                        'parent': comment.parent
                    }
                    for comment in comments
                ]
                return JsonResponse({
                    'code': 200,
                    'msg': 'success',
                    'data': comments
                })
            else:
                return JsonResponse({
                    'code': 404,
                    'msg': 'failed with no data'
                })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@router.path('api/leave/comment/')
def leave_comment(request):
    pass


@router.path('api/reply/comment/')
def reply_comment(request):
    pass


@router.path(pattern='api/get/article/')
@require_POST
def get_article_details(request):
    if request.method == "POST":
        # if request.method == "GET":
        try:
            article_id = int(request.POST.get('article_id'))
            # article_id = int(request.GET.get('article_id'))
        except ValueError:
            return JsonResponse({
                'code': 402,
                'msg': 'failed with invalid params'
            })
        except TypeError:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if article_id:
            articles = g_a(article_id)
            if articles:
                article = articles[0]
            else:
                article = None
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if article:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'article_id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'user': {
                        'user_id': article.user.id,
                        'username': article.user.username,
                        'email': article.user.email,
                    },
                    'correlation_software': article.correlation_software,
                    'created_time': article.created_time,
                    'updated_time': article.updated_time
                }
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@router.path(pattern='api/get/articles/')
# @require_POST
def get_articles(request):
    articles = g_as()
    # if request.method == "POST":
    if request.method == "GET":
        try:
            if request.GET.get('page_num'):
                # if request.POST.get('page_num'):
                page_num = int(request.GET.get('page_num'))
            elif request.POST.get('page_num') is None:
                page_num = 1
            else:
                page_num = -1
        except ValueError:
            return JsonResponse({
                'code': 402,
                'msg': 'failed with invalid params'
            })
        if page_num and page_num > 0:
            page_num = page_num - 1
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if articles:
            articles = articles[int(page_num * 7):int((page_num + 1) * 7)]
            if len(articles) > 0:
                articles = [
                    {
                        'id': article.id,
                        'user': {
                            'user_id': article.user.id,
                            'username': article.user.username,
                            'email': article.user.email,
                        },
                        'title': article.title,
                        'content': article.content,
                        'correlation_software': article.correlation_software,
                        'created_time': article.created_time,
                        'updated_time': article.updated_time
                    }
                    for article in articles
                ]
                return JsonResponse({
                    'code': 200,
                    'msg': 'success',
                    'data': articles
                })
            else:
                return JsonResponse({
                    'code': 404,
                    'msg': 'failed with no data'
                })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@router.path('publish/')
def publish_article_and_software_page(request):
    if request.method == "GET":
        return render(request, 'frontenduser/publish_article_and_software.html')


@router.path('api/publish/article/')
@require_POST
def publish_article(request):
    if request.method == "POST":
        try:
            user = request.user
            title = str(request.POST.get('title'))
            content = str(request.POST.get('content'))
        except ValueError:
            return JsonResponse({
                'code': 402,
                'msg': 'failed with invalid params'
            })
        article = Article.objects.create(user=user, title=title, content=content, state=2)
        if article:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'article_id': article.id
                }
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': '发布失败'
            })
    else:
        return JsonResponse({
            'code': 401,
            'msg': '请求方式错误'
        })


@require_GET
def articles_list(request):
    if request.method == "GET":
        return render(request, 'articles_list.html')
    return JsonResponse({
        'code': 405,
        'error': 'requested with wrong method'
    })


@require_GET
def article_details(request):
    if request.method == 'GET':
        articles = g_as()
        try:
            article_id = request.GET.get('article_id')
            if article_id is None:
                raise ValueError
            else:
                article_id = article_id.replace(' ', '+')
                article_id = int(decrypt(article_id))
        except ValueError:
            return render(request, 'article_details.html', {
                'error': 'Invalid params',
                'code': 402
            })
        except TypeError:
            return render(request, 'article_details.html', {
                'error': 'Invalid params',
                'code': 401
            })
        matched_articles = [article for article in articles if article.id == article_id]
        if len(matched_articles) > 0:
            article = matched_articles[0]
        else:
            article = None
        return render(request, 'article_details.html', {
            'article': article
        })
    else:
        return render(request, 'article_details.html', {
            'error': 'Not allowed request action',
            'code': 405
        })
