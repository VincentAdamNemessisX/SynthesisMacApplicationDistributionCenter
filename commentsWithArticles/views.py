# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET, require_safe, require_http_methods
from django_router import router
from commentsWithArticles.models import Article
from general.init_cache import get_comments
from software.models import SoftWare


@router.path(pattern='api/get/init/comments/')
@require_http_methods('POST')
def get_init_comments(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            comments = comments[:10]
            comments = [
                {
                    'id': comment.id,
                    'user': comment.user.username,
                    'content': comment.content,
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
                'code': 202,
                'msg': 'success but with no data',
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
            page_num = request.POST.get('page_num')
        except TypeError:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with wrong params'
            })
        comments = comments[:int(page_num * 10)]
        if comments:
            comments = [
                {
                    'id': comment.id,
                    'user': comment.user.username,
                    'content': comment.content,
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
                'code': 202,
                'msg': 'success but with no data'
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


@router.path('api/publish_article/')
@require_POST
def publish_article(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
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
