# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from general.init_cache import ( get_specific_user_articles_by_username,
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


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    return render(request, '404.html')