# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django_router import router

from general.init_cache import get_software
from .models import SoftWare


@router.path('api/publish_software/')
@require_POST
def publish_software(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        software = SoftWare.objects.create(
            user=user, name=name, state=2,
        )
        if software:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'software_id': software.id
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


@router.path('api/get/software/')
# @require_POST
def get_software_details(request):
    if request.method == "GET":
        software_id = request.GET.get('software_id')
        if software_id:
            software = get_software(id=software_id)[0]
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with wrong params'
            })
        if software:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'software_id': software.id,
                    'name': software.name,
                    'description': software.description,
                    'create_date': software.create_date,
                    'update_date': software.update_date,
                    'state': software.state,
                    'category': {
                        'id': software.category.id,
                        'name': software.category.name,
                        'slug': software.category.slug,
                        'icon': software.category.icon.url,
                        'description': software.category.description,
                    },
                    'user': {
                        'id': software.user.id,
                        'username': software.user.username,
                        # 'nickname': software.user.nickname,
                        # 'avatar': software.user.avatar,
                        'email': software.user.email,
                        # 'created_time': software.user.created_time,
                        # 'updated_time': software.user.updated_time,
                        # 'state': software.user.state,
                    }
                }
            })
        else:
            return JsonResponse({
                'code': 202,
                'msg': 'success but with no data'
            })
    else:
        return JsonResponse({
            'code': 401,
            'msg': '请求方式错误'
        })
