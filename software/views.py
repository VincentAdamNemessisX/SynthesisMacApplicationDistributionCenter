# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

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


# @require_POST
def software_details(request):
    # if request.method == 'POST'
    if request.method == 'GET':
        return render(request, 'frontenduser/software_details.html')