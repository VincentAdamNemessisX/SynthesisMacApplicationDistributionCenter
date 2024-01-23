# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods
from django_router import router

from commentsWithArticles.models import Article
from general.init_cache import get_comments


@router.path(pattern='api/get/init/comments/')
@require_http_methods('POST')
def get_init_comments(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            comments = comments[:10]
            # filter anything, just like specifc article or software
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


@router.path(pattern='api/load/more/comments/')
@require_POST
def load_more_comments(request):
    comments = get_comments()
    if request.method == "POST":
        try:
            page_num = int(request.POST.get('page_num'))
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
        if comments:
            comments = comments[int(page_num * 10):int((page_num + 1) * 10)]
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
