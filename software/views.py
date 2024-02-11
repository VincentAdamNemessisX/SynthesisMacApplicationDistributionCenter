# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router
from general.encrypt import decrypt
from general.init_cache import get_software_by_software_id, get_all_software
from .models import SoftWare


@router.path('api/publish/software/')
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


@router.path('api/get/single/software/')
@require_POST
def get_software_details(request):
    # if request.method == "GET":
    if request.method == "POST":
        try:
            # software_id = int(request.GET.get('software_id'))
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
            matched_software = get_software_by_software_id(software_id)
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
                    'created_time': software.created_time,
                    'updated_time': software.updated_time,
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
                        'email': software.user.email,
                    },
                    'correlation_articles': [
                        {
                            'id': article.id,
                            'title': article.title,
                            'content': article.content,
                            'created_time': article.created_time,
                            'updated_time': article.updated_time,
                        } for article in software.article_set.all()
                    ],
                    'screenshots': [
                        {
                            'id': screenshot.id,
                            'image': screenshot.image.url,
                        } for screenshot in software.softwarescreenshots_set.all()
                    ],
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
            'msg': 'failed with invalid request action'
        })


@router.path('api/get/software/')
@require_POST
def get_some_software(request):
    # if request.method == 'GET':
    if request.method == "POST":
        try:
            # page_num = request.GET.get('page_num')
            page_num = request.POST.get('page_num')
            if page_num is None:
                page_num = 1
            page_num = int(page_num)
            if page_num < 1:
                raise ValueError
            matched_software = get_all_software()[page_num * 10 - 10: page_num * 10]
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
        if matched_software and len(matched_software) > 0:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': [
                    {
                        'software_id': software.id,
                        'name': software.name,
                        'description': software.description,
                        'created_time': software.created_time,
                        'updated_time': software.updated_time,
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
                            'email': software.user.email,
                        },
                        'correlation_articles': [
                            {
                                'id': article.id,
                                'title': article.title,
                                'content': article.content,
                                'created_time': article.created_time,
                                'updated_time': article.updated_time,
                            } for article in software.article_set.all()
                        ],
                        'screenshots': [
                            {
                                'id': screenshot.id,
                                'image': screenshot.image.url,
                            } for screenshot in software.softwarescreenshots_set.all()
                        ],
                    } for software in matched_software
                ]
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 403,
            'msg': 'failed with request action'
        })


@require_GET
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')


@require_GET
def software_details(request):
    if request.method == 'GET':
        software_id = request.GET.get('software_id')
        try:
            software_id = str(software_id.replace(' ', '+'))
            software_id = decrypt(software_id)
        except ValueError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'invalid params', 'code': 402})
        except TypeError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'wrong params', 'code': 401})
        software = get_software_by_software_id(software_id)
        return render(request, 'frontenduser/software_details.html', {
            'software_id': software_id,
            'software': software
        })


@require_GET
def search_result(request):
    if request.method == 'GET':
        search_str = request.GET.get('s')
        if search_str:
            matched_software = SoftWare.objects.filter(name__contains=search_str, state=2)
            return render(request, 'frontenduser/search_result.html', {
                'search_str': search_str,
                'matched_software': matched_software
            })
        else:
            return render(request, 'frontenduser/search_result.html', {
                'error': 'invalid params',
                'code': 402
            })
    else:
        return render(request, 'frontenduser/search_result.html', {
            'error': 'invalid request action',
            'code': 403
        })


@router.path(pattern='api/thumb/')
@require_POST
def thumb(request):
    if request.method == 'POST':
        try:
            thumb_type = request.POST.get('thumb_type')
            software_id = request.POST.get('software_id')
            software_id = str(software_id.replace(' ', '+'))
            software_id = decrypt(software_id)
            software = SoftWare.objects.get(id=software_id)
            print(thumb_type)
            if thumb_type == 'thumb':
                if software:
                    software.thumbs_volume += 1
                    software.save()
                    return JsonResponse({
                        'code': 200
                    })
                else:
                    return JsonResponse({
                        'code': 404,
                        'error': 'Error with not found software'
                    })
            elif thumb_type == 'de_thumb':
                if software:
                    software.thumbs_volume -= 1
                    software.save()
                    return JsonResponse({
                        'code': 200
                    })
                else:
                    return JsonResponse({
                        'code': 404,
                        'error': 'Error with not found software'
                    })
        except ValueError:
            return JsonResponse({
                'code': 401,
                'error': 'Error with invalid params'
            })
        except TypeError:
            return JsonResponse({
                'code': 402,
                'error': 'Error with wrong params'
            })
        except AttributeError:
            return JsonResponse({
                'code': 400,
                'error': 'Error with bad params'
            })
        else:
            return JsonResponse({
                'code': 406,
                'error': 'Error with bad request headers'
            })
    else:
        return JsonResponse({
            'code': 405,
            'error': 'Error with bad request action'
        })