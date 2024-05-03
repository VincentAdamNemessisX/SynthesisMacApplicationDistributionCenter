# Create your views here.
import json

from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from frontenduser.models import FrontEndUser
from general.data_handler import handle_uploaded_image
from general.encrypt import decrypt
from general.init_cache import (get_specific_user_articles_by_username, get_all_user,
                                get_specific_user_software_by_username)


# @router.path(pattern='api/get/specific/user/favorite/articles/')
# @require_POST
# def get_specific_user_favorite_articles(request):
#     if request.method == 'POST':
#         try:
#             username = str(request.POST.get('username'))
#             # username = str(request.GET.get('username'))
#             matched_favorite_articles = get_specific_user_favorite_articles_by_username(username=username)
#         except ValueError:
#             return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
#         except TypeError:
#             return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params'})
#         if len(matched_favorite_articles) > 0:
#             matched_favorite_articles = [
#                 {
#                     'favorite_id': favorite.id,
#                     'favorite_article': {
#                         'article_id': favorite.correlation_article.id,
#                         'article_title': favorite.correlation_article.title,
#                         'article_content': favorite.correlation_article.content,
#                         'article_created_time': favorite.correlation_article.created_time,
#                         'article_updated_time': favorite.correlation_article.updated_time,
#                         'article_correlation_app': favorite.correlation_article.correlation_software,
#                         'article_user': favorite.correlation_article.user.username,
#                     },
#                     'favorite_user': {
#                         'user_id': favorite.user.id,
#                         'user_username': favorite.user.username,
#                         'user_email': favorite.user.email,
#                     },
#                     'favorite_created_time': favorite.created_time,
#                 }
#                 for favorite in matched_favorite_articles
#             ]
#             return JsonResponse({'code': 200, 'msg': 'success', 'data': matched_favorite_articles})
#         return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched articles'})
#     return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


# @router.path(pattern='api/get/all/favorite/articles/')
# @require_POST
# def get_all_favorite_articles(request):
#     if request.method == 'POST':
#         try:
#             matched_favorite_articles = g_a_f_a()
#         except ValueError:
#             return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
#         except TypeError:
#             return JsonResponse({'code': 402, 'msg': 'failed with wrong user or invalid params'})
#         if matched_favorite_articles and len(matched_favorite_articles) > 0:
#             matched_favorite_articles = [
#                 {
#                     'favorite_id': favorite.id,
#                     'favorite_article': {
#                         'article_id': favorite.correlation_article.id,
#                         'article_title': favorite.correlation_article.title,
#                         'article_content': favorite.correlation_article.content,
#                         'article_created_time': favorite.correlation_article.created_time,
#                         'article_updated_time': favorite.correlation_article.updated_time,
#                         'article_correlation_app': favorite.correlation_article.correlation_software,
#                         'article_user': favorite.correlation_article.user.username,
#                     },
#                     'favorite_user': {
#                         'user_id': favorite.user.id,
#                         'user_username': favorite.user.username,
#                         'user_email': favorite.user.email,
#                     },
#                     'favorite_created_time': favorite.created_time,
#                 }
#                 for favorite in matched_favorite_articles
#             ]
#             return JsonResponse({'code': 200, 'msg': 'success', 'data': matched_favorite_articles})
#         return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched articles'})
#     return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


@router.path(pattern='api/get/specific/user/articles/')
@require_POST
def get_specific_user_articles(request):
    if request.method == 'POST':
        # if request.method == 'GET':
        try:
            # username = str(request.GET.get('username'))
            username = str(request.POST.get('username'))
            articles = get_specific_user_articles_by_username(username=username)
        except ValueError:
            return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
        except TypeError:
            return JsonResponse({'code': 402, 'msg': 'failed with wrong user or invalid params'})
        if articles and len(articles) > 0:
            articles = [
                {
                    'article_id': article.id,
                    'article_title': article.title,
                    'article_content': article.content,
                    'article_created_time': article.created_time,
                    'article_updated_time': article.updated_time,
                    'article_correlation_software':
                        {
                            'software_id': article.correlation_software.id,
                            'software_name': article.correlation_software.name,
                            'software_created_time': article.correlation_software.created_time,
                            'software_updated_time': article.correlation_software.updated_time,
                        }
                        if article.correlation_software else None,
                    'article_user': {
                        'user_id': article.user.id,
                        'user_username': article.user.username,
                        'user_email': article.user.email,
                    },
                }
                for article in articles
            ]
            return JsonResponse({'code': 200, 'msg': 'success', 'data': articles})
        else:
            return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched articles'})
    else:
        return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


@router.path(pattern='api/get/specific/user/favorite/software/')
# @require_POST
def get_specific_user_favorite_software(request):
    # if request.method == 'POST':
    if request.method == 'GET':
        try:
            username = str(request.GET.get('username'))
            # username = str(request.POST.get('username'))
            software = get_specific_user_software_by_username(username=username)
        except ValueError:
            return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
        except TypeError:
            return JsonResponse({'code': 402, 'msg': 'failed with wrong user or invalid params'})
        if software and len(software) > 0:
            software = [
                {
                    'software_id': soft_ware.id,
                    'software_name': soft_ware.name,
                    'software_created_time': soft_ware.created_time,
                    'software_updated_time': soft_ware.updated_time,
                    'software_correlation_article':
                        [
                            {
                                'article_id': article.id,
                                'article_title': article.title,
                                'user': {
                                    'user_id': article.user.id,
                                    'user_username': article.user.username,
                                    'user_email': article.user.email,
                                },
                                'article_created_time': article.created_time,
                                'article_updated_time': article.updated_time,
                            }
                            for article in soft_ware.article_set.all().filter(state=2)],
                    'software_user': {
                        'user_id': soft_ware.user.id,
                        'user_username': soft_ware.user.username,
                        'user_email': soft_ware.user.email,
                    },
                }
                for soft_ware in software
            ]
            return JsonResponse({'code': 200, 'msg': 'success', 'data': software})
        else:
            return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched software'})
    else:
        return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


@router.path(pattern='api/get/specific/user/software/')
@require_POST
def get_specific_user_favorite_software(request):
    # if request.method == 'GET':
    if request.method == 'POST':
        try:
            # username = request.GET.get('username')
            username = request.POST.get('username')
            if username is None:
                raise ValueError
            matched_software = get_specific_user_software_by_username(username=username)
        except ValueError:
            return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
        except TypeError:
            return JsonResponse({'code': 402, 'msg': 'failed with wrong user or invalid params'})
        if matched_software and len(matched_software) > 0:
            matched_software = [
                {
                    'software_id': software.id,
                    'software_name': software.name,
                    'software_created_time': software.created_time,
                    'software_updated_time': software.updated_time,
                    'software_correlation_article': [
                        {
                            'article_id': article.id,
                            'article_title': article.title,
                            'article_created_time': article.created_time,
                            'article_updated_time': article.updated_time,
                            'article_user': {
                                'user_id': article.user.id,
                                'user_username': article.user.username,
                                'user_email': article.user.email,
                            }
                        }
                        for article in software.article_set.all().filter(state=2)
                    ],
                    'software_user': {
                        'user_id': software.user.id,
                        'user_username': software.user.username,
                        'user_email': software.user.email,
                    },
                }
                for software in matched_software
            ]
            return JsonResponse({'code': 200, 'msg': 'success', 'data': matched_software})
        return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched software'})
    return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


# @router.path(pattern='api/get/all/favorite/software/')
# # @require_POST
# def get_all_favorite_software(request):
#     if request.method == 'GET':
#         try:
#             matched_favorite_software = g_a_f_s()
#         except ValueError:
#             return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params value'})
#         except TypeError:
#             return JsonResponse({'code': 402, 'msg': 'failed with wrong user or invalid params'})
#         if matched_favorite_software and len(matched_favorite_software) > 0:
#             matched_favorite_software = [
#                 {
#                     'favorite_id': favorite.id,
#                     'favorite_software': {
#                         'software_id': favorite.correlation_software.id,
#                         'software_name': favorite.correlation_software.name,
#                         'software_created_time': favorite.correlation_software.created_time,
#                         'software_updated_time': favorite.correlation_software.updated_time,
#                         'software_correlation_article': [
#                             {
#                                 'article_id': article.id,
#                                 'article_title': article.title,
#                                 'article_created_time': article.created_time,
#                                 'article_updated_time': article.updated_time,
#                                 'article_user': {
#                                     'user_id': article.user.id,
#                                     'user_username': article.user.username,
#                                     'user_email': article.user.email,
#                                 }
#                             }
#                             for article in favorite.correlation_software.article_set.all().filter(state=2)
#                         ],
#                         'software_user': {
#                             'user_id': favorite.correlation_software.user.id,
#                             'user_username': favorite.correlation_software.user.username,
#                             'user_email': favorite.correlation_software.user.email,
#                         },
#                     },
#                     'favorite_user': {
#                         'user_id': favorite.user.id,
#                         'user_username': favorite.user.username,
#                         'user_email': favorite.user.email,
#                     },
#                     'favorite_created_time': favorite.created_time,
#                 }
#                 for favorite in matched_favorite_software
#             ]
#             return JsonResponse({'code': 200, 'msg': 'success', 'data': matched_favorite_software})
#         return JsonResponse({'code': 404, 'msg': 'request succeed, failed with no matched articles'})
#     return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'})


@require_GET
def login(request):
    if request.method == 'GET':
        return render(request, 'login&register.html')
    return render(request, '404.html')


@require_GET
@login_required
def logout(request):
    if request.method == 'GET':
        redirect_to = request.GET.get('redirect_to', '/')
        if request.session.get('logon_user'):
            del request.session['logon_user']
            django_logout(request)
        return redirect(redirect_to)
    return render(request, '404.html')


@router.path('api/login/')
@require_POST
def login_handler(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        username = post_data.get('username')
        password = post_data.get('password')
        if username and password:
            username, password = decrypt(username), decrypt(password)
            user = [x for x in get_all_user() if x.username == username
                    and check_password(password, x.django_user.password)]
            if len(user) > 1:
                return JsonResponse({'code': 401, 'msg': 'failed with wrong user or invalid params'}, status=401)
            if len(user) <= 0:
                return JsonResponse({'code': 404, 'msg': 'failed with no matched user or wrong password'}, status=401)
            if len(user) == 1:
                django_login(request, user[0].django_user)
                request.session['logon_user'] = user[0]
                return JsonResponse({'code': 200, 'msg': 'success'}, status=200)
        return JsonResponse({'code': 401, 'msg': 'failed with invalid params'}, status=401)
    return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'}, status=400)


@router.path(pattern='api/register/')
@require_POST
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname') if request.POST.get('nickname') else None
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('password_repeat')
        if username and password and email and repeat_password:
            if len(FrontEndUser.objects.filter(username=username)) > 0:
                return JsonResponse({'code': 401, 'msg': 'failed with existed user'})
            if password != repeat_password:
                return JsonResponse({'code': 401, 'msg': 'failed with different password'})
            try:
                User(username=username, email=email, password=make_password(password)).save()
                user = FrontEndUser(username=username, nickname=nickname,
                                    django_user=User.objects.get(username=username, email=email),
                                    state=2, role='普通用户')
                user.save()
            except Exception as e:
                return JsonResponse({'code': 401, 'msg': str(e)}, status=401)
            created_user = FrontEndUser.objects.get(username=username)
            head_icon_path = handle_uploaded_image(request.FILES.get('head_icon'), 'user/head_icon/')
            created_user.head_icon = head_icon_path
            created_user.save()
            return JsonResponse({'code': 200, 'msg': 'success'}, status=200)
        return JsonResponse({'code': 401, 'msg': 'failed with invalid params'}, status=401)
    return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'}, status=400)


@router.path(pattern='api/update/')
@login_required
@require_POST
def update_user(request):
    if request.method == 'POST':
        username = request.POST['username'] or None
        nickname = request.POST.get('nickname') or None
        email = request.POST['email'] or None
        description = request.POST.get('description') or None
        head_icon = request.FILES['head_icon'] if request.FILES.get('head_icon') else None
        user_center_cover = request.FILES['user_center_cover'] if request.FILES.get('user_center_cover') else None
        if username and email:
            if len(FrontEndUser.objects.filter(username=username)) == 1:
                try:
                    django_user = User.objects.get(username=username)
                    django_user.email = email if django_user.email != email else django_user.email
                    django_user.save()
                    user = FrontEndUser.objects.filter(username=username)[0] \
                        if FrontEndUser.objects.filter(username=username).count() == 1 else None
                    user.username = username if user.username != username else user.username
                    user.nickname = nickname if user.nickname != nickname else user.nickname
                    user.description = description if user.description != description else user.description
                    user.save()
                except Exception as e:
                    return JsonResponse({'code': 401, 'msg': str(e)}, status=401)
                updated_user = FrontEndUser.objects.get(username=username)
                head_icon_path = handle_uploaded_image(head_icon, 'user/head_icon/') if head_icon else None
                user_center_cover_path = handle_uploaded_image(user_center_cover, 'user/user_center_cover/') if user_center_cover else None
                if head_icon_path:
                    updated_user.head_icon = head_icon_path
                    updated_user.save()
                if user_center_cover_path:
                    updated_user.user_center_cover = user_center_cover_path
                    updated_user.save()
            return JsonResponse({'code': 200, 'msg': 'success'}, status=200)
        else:
            return JsonResponse({'code': 401, 'msg': 'failed with invalid params'}, status=401)
    return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'}, status=400)


@router.path(pattern='api/delete/')
@login_required
@require_POST
def cancel_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        if user_id:
            if len(FrontEndUser.objects.filter(id=user_id)) == 1:
                try:
                    # user = FrontEndUser.objects.get(id=user_id)
                    if request.session.get('logon_user'):
                        del request.session['logon_user']
                        django_logout(request)
                    user = User.objects.get(id=FrontEndUser.objects.get(id=user_id).django_user_id)
                    user.delete()
                except Exception as e:
                    return JsonResponse({'code': 401, 'msg': str(e)}, status=401)
            return JsonResponse({'code': 200, 'msg': 'success'}, status=200)
        else:
            return JsonResponse({'code': 401, 'msg': 'failed with invalid params'}, status=401)
    return JsonResponse({'code': 400, 'msg': 'failed with wrong request action'}, status=400)


@require_GET
def user_details(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            user_id = int(decrypt(user_id))
        except ValueError:
            return render(request, '404.html', {
                'code': 401,
                'msg': 'failed with wrong user or invalid params value'
            })
        except TypeError:
            return render(request, '404.html', {
                'code': 402,
                'msg': 'failed with wrong user or invalid params'
            })
        except Exception as e:
            return render(request, '404.html', {
                'code': 403,
                'msg': str(e)
            })
        if user_id:
            user = [x for x in get_all_user() if x.id == user_id]
            if len(user) == 1:
                published_articles_count = len(user[0].article_set.all())
                published_software_count = len([x for x in
                                                get_specific_user_software_by_username(user[0].username)])
                published_comments_count = len(user[0].comment_set.all())
                recent_browsing_count = len(user[0].recentbrowsing_set.all())
                current_software_set = [x for x in
                                        get_specific_user_software_by_username(user[0].username)]
                return render(request, 'user_details.html', {
                    'user': user[0],
                    'published_articles_count': published_articles_count,
                    'published_software_count': published_software_count,
                    'published_comments_count': published_comments_count,
                    'recent_browsing_count': recent_browsing_count,
                    'current_software_set': current_software_set
                })
            return render(request, '404.html', {
                'code': 404,
                'msg': 'request succeed, failed with no matched user'
            })
        return render(request, '404.html', {
            'code': 400,
            'msg': 'failed with wrong request action'
        })
    return render(request, '404.html', {
        'code': 400,
        'msg': 'failed with wrong request action'
    })
