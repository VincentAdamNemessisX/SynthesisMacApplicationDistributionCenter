# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from frontenduser.models import FrontEndUser
from general.common_compute import compute_similarity
from general.data_handler import handle_uploaded_image
from general.encrypt import decrypt
from general.init_cache import get_software_by_software_id, get_all_software
from .models import SoftWare


@router.path('publish/')
@require_POST
def publish_software(request):
    if request.method == "POST":
        software = None
        screen_shots_urls = []
        try:
            user = FrontEndUser.objects.get(username='vincent')
            name = request.POST.get('name')
            version = request.POST.get('version')
            language = request.POST.get('language')
            platform = request.POST.get('platform')
            run_os_version = request.POST.get('run_os_version')
            file_size = request.POST.get('file_size')
            official_link = request.POST.get('official_link')
            description = request.POST.get('description')
            category = request.POST.get('category')
            tags = request.POST.get('tags')
            link_adrive = request.POST.get('link_adrive')
            link_baidu = request.POST.get('link_baidu')
            link_direct = request.POST.get('link_direct') \
                if request.POST.get('link_direct') else None
            link_123 = request.POST.get('link_123')
            icon_url = handle_uploaded_image(request.FILES.get('icon'),
                                             'software/icon/')
            for index in range(1, 6):
                screen_shots_urls.append(
                    handle_uploaded_image(request.FILES.get('software_screenshot_' + str(index)),
                                          'software/screenshots/')
                )
            software = SoftWare.objects.create(
                name=name,
                version=version,
                language=language,
                platform=platform,
                run_os_version=run_os_version,
                file_size=file_size,
                official_link=official_link,
                description=description,
                category_id=category,
                tags=tags,
                link_adrive=link_adrive,
                link_baidu=link_baidu,
                link_direct=link_direct,
                link_123=link_123,
                icon=icon_url,
                user=user
            )
        except KeyError:
            pass
        except ValueError:
            return render(request, '500.html', {
                'code': 401,
                'error': '参数错误'
            })
        except AttributeError:
            return render(request, '500.html', {
                'code': 400,
                'error': '参数异常'
            })
        if software:
            for url in screen_shots_urls:
                if url is None:
                    continue
                software.softwarescreenshots_set.create(software=software, image=url)
            return render(request, 'frontenduser/publish_software.html', {
                'msg': '发布成功',
                'go_to': '/commentswitharticles/publish/?type=2'
            })
        else:
            return render(request, '500.html', {
                'code': 402,
                'error': '数据库异常或未知错误'
            })
    else:
        return render(request, '500.html', {
            'code': 403,
            'error': '请求方式错误'
        })


@router.path('api/get/single/software/')
@require_POST
def get_software_details(request):
    # if request.method == "GET":
    if request.method == "POST":
        try:
            # software_id = int(request.GET.get('software_id'))
            software_id = request.POST.get('software_id')
            software_id = int(decrypt(software_id))
        except ValueError:
            return JsonResponse({
                'code': 402,
                'error': 'failed with invalid params'
            })
        except TypeError:
            return JsonResponse({
                'code': 401,
                'error': 'failed with wrong params'
            })
        except AttributeError:
            return JsonResponse({
                'code': 406,
                'error': 'failed with unexpected error'
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
                'error': 'failed with wrong params'
            })
        if software:
            return JsonResponse({
                'code': 200,
                'error': 'success',
                'data': {
                    'software_id': software.id,
                    'name': software.name,
                    'version': software.version,
                    'language': software.language,
                    'platform': software.platform,
                    'run_os_version': software.run_os_version,
                    'description': software.description,
                    'category': {
                        'id': software.category.id,
                        'name': software.category.name,
                        'slug': software.category.slug,
                        'icon': software.category.icon.url,
                        'description': software.category.description,
                    },
                    'tags': software.tags,
                    'file_size': software.file_size,
                    'official_link': software.official_link,
                    'link_adrive': software.link_adrive,
                    'link_baidu': software.link_baidu,
                    'link_direct': software.link_direct,
                    'link_123': software.link_123,
                    'icon': software.icon.url,
                    'state': software.state,
                    'user': {
                        'id': software.user.id,
                        'username': software.user.username,
                        'email': software.user.email,
                    },
                    'view_volume': software.view_volume,
                    'thumbs_volume': software.thumbs_volume,
                    'download_volume': software.download_volume,
                    'created_time': software.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_time': software.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'correlation_articles': [
                        {
                            'id': article.id,
                            'title': article.title,
                            'content': article.content,
                            'created_time': article.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_time': article.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
                        } for article in software.article_set.all().filter(state=2)
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
                'error': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 401,
            'error': 'failed with invalid request action'
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
                'error': 'failed with invalid params'
            })
        except TypeError:
            return JsonResponse({
                'code': 401,
                'error': 'failed with wrong params'
            })
        if matched_software and len(matched_software) > 0:
            return JsonResponse({
                'code': 200,
                'error': 'success',
                'data': [
                    {
                        'software_id': software.id,
                        'name': software.name,
                        'version': software.version,
                        'language': software.language,
                        'platform': software.platform,
                        'run_os_version': software.run_os_version,
                        'description': software.description,
                        'category': {
                            'id': software.category.id,
                            'name': software.category.name,
                            'slug': software.category.slug,
                            'icon': software.category.icon.url,
                            'description': software.category.description,
                        },
                        'tags': software.tags,
                        'file_size': software.file_size,
                        'official_link': software.official_link,
                        'link_adrive': software.link_adrive,
                        'link_baidu': software.link_baidu,
                        'link_direct': software.link_direct,
                        'link_123': software.link_123,
                        'icon': software.icon.url,
                        'state': software.state,
                        'user': {
                            'id': software.user.id,
                            'username': software.user.username,
                            'email': software.user.email,
                        },
                        'view_volume': software.view_volume,
                        'thumbs_volume': software.thumbs_volume,
                        'download_volume': software.download_volume,
                        'created_time': software.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_time': software.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'correlation_articles': [
                            {
                                'id': article.id,
                                'title': article.title,
                                'content': article.content,
                                'created_time': article.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'updated_time': article.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
                            } for article in software.article_set.all().filter(state=2)
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
                'error': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 403,
            'error': 'failed with request action'
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
            software_id = decrypt(software_id.encode())
            software = get_software_by_software_id(software_id)[0]
            software.screenshots_set = software.softwarescreenshots_set.all()
            software.screenshots_set.count = len(software.screenshots_set)
            software.screenshots_set.count_list = [i for i in range(software.screenshots_set.count)]
            related_software = [temp for temp in get_all_software()
                                if temp.state == 2 and temp.id != software.id]
            related_software = sorted(related_software,
                                      key=lambda x: compute_similarity(software.description, x.description),
                                      reverse=True)[:6]
            related_software_length = len(related_software)
            related_articles = software.article_set.all().filter(state=2)
            related_articles_length = len(related_articles)
        except ValueError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'invalid params', 'code': 402})
        except TypeError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'wrong params', 'code': 401})
        except AttributeError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'not found', 'code': 404})
        except IndexError:
            return render(request, 'frontenduser/software_details.html',
                          {'error': 'not found', 'code': 404})
        return render(request, 'frontenduser/software_details.html', {
            'software_id': software_id,
            'software': software,
            'related_software': related_software,
            'related_software_count': related_software_length,
            'related_articles': related_articles,
            'related_articles_count': related_articles_length,
            'respond_comment': 'software'
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
