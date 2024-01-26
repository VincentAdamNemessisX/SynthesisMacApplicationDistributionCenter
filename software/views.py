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
            user=user, name=name, state=1,
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
@require_POST
def get_software_details(request):
    if request.method == "POST":
        try:
            software_id = int(request.POST.get('software_id'))
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
        if software_id:
            matched_software = get_software(software_id)
            if matched_software:
                software = matched_software[0]
            else:
                software = None
        else:
            return JsonResponse({
                'code': 401,
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
                    },
                    'screenshots': [{
                        'id': screenshot.id,
                        'image': screenshot.image.url,
                    } for screenshot in software.softwarescreenshots_set.all()],
                }
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 401,
            'msg': '请求方式错误'
        })
