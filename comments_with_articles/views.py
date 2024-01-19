# Create your views here.
from django.http import JsonResponse

from comments_with_articles.models import Comment


def get_init_comments(request):
    if request.method == "POST":
        comments = Comment.objects.filter(parent=None, state=2)[:10]
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'comments': list(comments.values())
            }
        })


def load_more_comments(request):
    if request.method == "POST":
        page_num = request.POST.get('page_num')
        comments = Comment.objects.filter(None, state=2)[:page_num * 10]
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'comments': list(comments.values())
            }
        })