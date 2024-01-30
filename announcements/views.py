# Create your views here.
from django.http import JsonResponse
from django_router import router
from general.init_cache import get_notices


@router.path(pattern='api/notice/to/all/')
def get_notice_to_all(request):
    if request.method == 'GET':
        notices = get_notices()
        notices = [notice for notice in notices if notice.type == 1]
        notices = [
            {
                'id': notice.id,
                'title': notice.title,
                'content': notice.content,
                'created_time': notice.created_time,
                'image': notice.image.url if notice.image else None
            }
            for notice in notices
        ]
        if notices:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notices})
        else:
            return JsonResponse({'code': 202, 'msg': '请求成功，但是没有数据'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})


@router.path(pattern='api/notice/to/specific/software/')
def get_specific_app_notice(request):
    if request.method == 'GET':
        notices = get_notices()
        notice = [notice for notice in notices
                   if notice.type == 2 and
                   notice.app.id == request.GET.get('software_id')]
        notice = [
            {
                'id': notice.id,
                'title': notice.title,
                'content': notice.content,
                'created_time': notice.created_time,
                'image': notice.image.url if notice.image else None,
                'app': notice.app.name if notice.app else None
            }
            for notice in notice
        ]
        if notices:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notice})
        else:
            return JsonResponse({'code': 202, 'msg': '请求成功，但是没有数据'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})
