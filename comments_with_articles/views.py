# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from general.init_cache import get_comments, get_articles
from comments_with_articles.models import Comment, Article


def get_init_comments(request):
    comments = get_comments()
    if request.method == "POST":
        comments = comments[:10]
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'comments': comments
            }
        })


def load_more_comments(request):
    comments = get_comments()
    if request.method == "POST":
        page_num = request.POST.get('page_num')
        comments = comments[:page_num * 10]
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'comments': list(comments.values())
            }
        })


def publish_article_and_software_page(request):
    if request.method == "GET":
        return render(request, 'frontenduser/publish_article_and_software.html')


def publish_article(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(user=user, title=title, content=content)
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


