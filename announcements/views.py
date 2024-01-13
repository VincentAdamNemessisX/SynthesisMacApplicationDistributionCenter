# Create your views here.
from django.core import serializers
from django.http import JsonResponse

from announcements.models import Announcements


def get_notice_to_all(request):
    if request.method == 'GET':
        notices = Announcements.objects.filter(type=0).order_by('-date')[:1]
        notices = [
            {
                'id': notice.id,
                'title': notice.title,
                'content': notice.content,
                'date': notice.date,
                'author': notice.author.username,
                'type': notice.type,
                'app': notice.app.name if notice.app else None
            }
            for notice in notices
        ]
        if notices:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notices})
        else:
            return JsonResponse({'code': 400, 'msg': '获取失败'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})