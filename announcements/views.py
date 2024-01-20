# Create your views here.
from django.http import JsonResponse
from django_router import router

from announcements.models import Announcements


@router.path(pattern='api/notice/to/all/')
def get_notice_to_all(request):
    if request.method == 'GET':
        notices = Announcements.objects.filter(type=0).order_by('-date')[:1]
        notices = [
            {
                'id': notice.id,
                'title': notice.title,
                'content': notice.content,
                'date': notice.date,
                'image': notice.image.url if notice.image else None
            }
            for notice in notices
        ]
        if notices:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notices})
        else:
            return JsonResponse({'code': 400, 'msg': '获取失败'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})


@router.path(pattern='api/notice/to/specific/app/')
def get_specific_app_notice(request):
    if request.method == 'GET':
        notice = Announcements.objects.filter(type=1, app__id=request.GET.get('app_id')).order_by('-date')[:1]
        notices = [
            {
                'id': notice.id,
                'title': notice.title,
                'content': notice.content,
                'date': notice.date,
                'image': notice.image.url if notice.image else None,
                'app': notice.app.name if notice.app else None
            }
            for notice in notice
        ]
        if notice:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notices})
        else:
            return JsonResponse({'code': 404, 'msg': '获取失败'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})
