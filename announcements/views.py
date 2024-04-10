# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django_router import router
from general.init_cache import get_notices
from general.encrypt import encrypt, decrypt


@router.path(pattern='api/notice/to/all/')
@require_POST
def get_notice_to_all(request):
    if request.method == 'POST':
    # if request.method == 'GET':
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
@require_POST
def get_specific_app_notice(request):
    if request.method == 'POST':
    # if request.method == 'GET':
        # software_id = request.GET.get('software_id')
        software_id = request.POST.get('software_id') if request.POST.get('software_id') else ''
        if software_id == '':
            return JsonResponse({'code': 402, 'msg': '获取软件ID失败'})
        try:
            software_id = decrypt(software_id.replace(' ', '+'))
            software_id = int(software_id)
        except ValueError:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid params'})
        except TypeError:
            return JsonResponse({'code': 401, 'msg': 'failed with wrong params'})
        notices = get_notices()
        notice = [notice for notice in notices if notice.type == 2 and notice.app.id == software_id]
        notice = [
            {
                'id': str(encrypt(str(n.id))),
                'title': n.title,
                'content': n.content,
                'created_time': n.created_time,
                'image': n.image.url if n.image else None,
                'app': n.app.name if n.app else None
            }
            for n in notice
        ]
        if notices:
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': notice})
        else:
            return JsonResponse({'code': 202, 'msg': '请求成功，但是没有数据'})
    else:
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})
