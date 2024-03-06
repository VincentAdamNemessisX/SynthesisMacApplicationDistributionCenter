# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django_router import router

from commentswitharticles.models import Article
from frontenduser.models import FrontEndUser
from general.common_compute import get_context_articles, compute_similarity
from general.data_handler import get_image_urls_from_md_str
from general.encrypt import decrypt, encrypt
from general.init_cache import (get_comments,
                                get_matched_articles_by_article_id as g_a,
                                get_all_articles as g_as, get_all_software as g_a_s)
from software.models import SoftWare

not_in_init_comments_parent = set()


@router.path(pattern='api/get/init/comments/')
@require_http_methods('POST')
def get_init_comments(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            # filter specifc article or software
            try:
                post_data = json.loads(request.body)
                query_id = decrypt(post_data['query_id'].replace(' ', '+'))
                type = post_data['type']
            except ValueError:
                return JsonResponse({
                    'code': 402,
                    'msg': 'failed with invalid params'
                })
            except TypeError:
                return JsonResponse({
                    'code': 407,
                    'msg': 'failed with wrong params'
                })
            except AttributeError:
                return JsonResponse({
                    'code': 401,
                    'msg': 'failed with bad request body'
                })
            if type == 'article':
                comments = [comment for comment in comments
                            if comment.correlation_article and comment.correlation_article.id == int(query_id)]
            if type == 'software':
                comments = [comment for comment in comments
                            if comment.correlation_software and comment.correlation_software.id == int(query_id)]
            comments = comments[:10]
            if len(comments) <= 0:
                return JsonResponse({
                    'code': 404,
                    'msg': 'failed with no data'
                })
            comments = [
                {
                    'comment_id': encrypt(str(comment.id)).decode('utf-8'),
                    'user': {
                        'user_id': encrypt(str(comment.user.id)).decode('utf-8'),
                        'username': comment.user.nickname if comment.user.nickname else comment.user.username,
                        'head_icon': comment.user.head_icon.url,
                        'role': comment.user.role,
                    },
                    'content': comment.content,
                    'correlation_article': comment.correlation_article.title if comment.correlation_article else '',
                    'correlation_software': comment.correlation_software.name if comment.correlation_software else '',
                    'created_time': comment.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'parent_id': encrypt(str(comment.parent.id)).decode('utf-8') if comment.parent else encrypt(
                        str(0)).decode('utf-8')
                }
                for comment in comments
            ]
            comments_id_list = [j['comment_id'] for j in comments]
            comments_id_list.append(encrypt(str(0)).decode('utf-8'))
            for i in comments:
                if i['parent_id'] not in comments_id_list:
                    not_in_init_comments_parent.add(i['parent_id'])
            for i in not_in_init_comments_parent:
                if type == 'article':
                    t = [t for t in get_comments() if
                         i == encrypt(str(t.id)).decode('utf8') and t.correlation_article.id == int(query_id)][0]
                if type == 'software':
                    t = [t for t in get_comments() if
                         i == encrypt(str(t.id)).decode('utf8') and t.correlation_software.id == int(query_id)][0]
                t = {
                    'comment_id': encrypt(str(t.id)).decode('utf-8'),
                    'user': {
                        'user_id': encrypt(str(t.user.id)).decode('utf-8'),
                        'username': t.user.nickname if t.user.nickname else t.user.username,
                        'head_icon': t.user.head_icon.url,
                        'role': t.user.role,
                    },
                    'content': t.content,
                    'correlation_article': t.correlation_article.title if t.correlation_article else '',
                    'correlation_software': t.correlation_software.name if t.correlation_software else '',
                    'created_time': t.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'parent_id': encrypt(str(t.parent.id)).decode('utf-8') if t.parent else encrypt(str(0)).decode(
                        'utf-8')
                }
                comments.append(t)
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'comments': comments
                }
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data',
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@router.path(pattern='api/load/more/comments/')
@require_POST
def load_more_comments(request):
    comments = [t for t in get_comments() if encrypt(str(t.id)).decode('utf8')
                not in not_in_init_comments_parent]
    if request.method == "POST":
        if comments:
            # filter anything, just like specifc article or software
            try:
                post_data = json.loads(request.body)
                query_id = decrypt(post_data['query_id'].encode())
                type = post_data['type']
            except ValueError:
                return JsonResponse({
                    'code': 402,
                    'msg': 'failed with invalid params'
                })
            except TypeError:
                return JsonResponse({
                    'code': 407,
                    'msg': 'failed with wrong params'
                })
            except AttributeError:
                return JsonResponse({
                    'code': 401,
                    'msg': 'failed with bad request body'
                })
            if type == 'article':
                comments = [comment for comment in comments
                            if comment.correlation_article and comment.correlation_article.id == int(query_id)]
            if type == 'software':
                comments = [comment for comment in comments
                            if comment.correlation_software and comment.correlation_software.id == int(query_id)]
            if len(comments) < 10:
                comments = None
            else:
                comments = comments[10:]
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if comments:
            if comments:
                comments = [
                    {
                        'comment_id': encrypt(str(comment.id)).decode('utf-8'),
                        'user': {
                            'user_id': encrypt(str(comment.user.id)).decode('utf-8'),
                            'username': comment.user.nickname if comment.user.nickname else comment.user.username,
                            'head_icon': comment.user.head_icon.url,
                            'role': comment.user.role,
                        },
                        'content': comment.content,
                        'correlation_article': comment.correlation_article.title if comment.correlation_article else '',
                        'correlation_software': comment.correlation_software.name if comment.correlation_software else '',
                        'created_time': comment.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'parent_id': encrypt(str(comment.parent.id)).decode('utf-8') if comment.parent else encrypt(
                            str(0)).decode('utf-8')
                    }
                    for comment in comments
                ]
                return JsonResponse({
                    'code': 200,
                    'msg': 'success',
                    'data': {
                        'comments': comments
                    }
                })
            else:
                return JsonResponse({
                    'code': 404,
                    'msg': 'failed with no data'
                })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@login_required
@require_POST
@router.path('api/publish/comment/')
def leave_comment(request):
    if request.method == 'POST':
        try:
            user = FrontEndUser.objects.get(username='vincent')
            content = request.POST.get('comment')
            correlation_article_id = int(decrypt(request.POST.get('article_id').encode('utf-8')))
            correlation_software_id = int(decrypt(request.POST.get('software_id').encode('utf-8')))
            parent_id = int(decrypt(request.POST.get('comment_parent').encode('utf-8')))
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
        except AttributeError:
            return JsonResponse({
                'code': 406,
                'msg': 'failed with wrong request body'
            })
        if correlation_article_id:
            correlation_article = Article.objects.get(id=correlation_article_id)
        else:
            correlation_article = None
        if correlation_software_id:
            correlation_software = SoftWare.objects.get(id=correlation_software_id)
        else:
            correlation_software = None
        if parent_id:
            parent = user.comment_set.get(id=parent_id).filter(state=2)
        else:
            parent = None
        comment = user.comment_set.create(content=content,
                                          correlation_article=correlation_article,
                                          correlation_software=correlation_software,
                                          parent=parent)
        if comment:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'comment_id': encrypt(str(comment.id)).decode('utf-8')
                }
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': 'failed when inserting data to database'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with invalid request action'
        })


@router.path(pattern='api/get/articles/')
# @require_POST
def get_articles(request):
    articles = g_as()
    # if request.method == "POST":
    if request.method == "GET":
        try:
            if request.GET.get('page_num'):
                # if request.POST.get('page_num'):
                page_num = int(request.GET.get('page_num'))
            elif request.POST.get('page_num') is None:
                page_num = 1
            else:
                page_num = -1
        except ValueError:
            return JsonResponse({
                'code': 402,
                'msg': 'failed with invalid params'
            })
        if page_num and page_num > 0:
            page_num = page_num - 1
        else:
            return JsonResponse({
                'code': 401,
                'msg': 'failed with wrong params'
            })
        if articles:
            articles = articles[int(page_num * 7):int((page_num + 1) * 7)]
            if len(articles) > 0:
                articles = [
                    {
                        'id': article.id,
                        'user': {
                            'user_id': article.user.id,
                            'username': article.user.username,
                            'email': article.user.email,
                        },
                        'title': article.title,
                        'content': article.content,
                        'correlation_software': article.correlation_software,
                        'created_time': article.created_time,
                        'updated_time': article.updated_time
                    }
                    for article in articles
                ]
                return JsonResponse({
                    'code': 200,
                    'msg': 'success',
                    'data': articles
                })
            else:
                return JsonResponse({
                    'code': 404,
                    'msg': 'failed with no data'
                })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })


@router.path('publish/')
def publish_article_and_software_page(request):
    if request.method == "GET":
        all_software = g_a_s()
        try:
            type = request.GET.get('type')
            if int(type) == 1:
                return render(request, 'frontenduser/publish_article.html', {
                    'all_software': all_software
                })
            elif int(type) == 2:
                return render(request, 'frontenduser/publish_software.html', {
                })
            else:
                return render(request, '500.html', {
                    'error': '请求参数错误'
                })
        except ValueError:
            return render(request, '500.html', {
                'error': '请求参数错误'
            })
        except TypeError:
            return render(request, '500.html', {
                'error': '请求参数错误'
            })


@require_GET
def articles_list(request):
    if request.method == "GET":
        articles = g_as()
        articles_count = len(articles)
        return render(request, 'articles_list.html',
                      {
                          'articles': articles[:6],
                          'articles_count': articles_count
                      })
    return render(request, '500.html', {
        'code': 405,
        'error': 'requested with wrong method'
    })


@require_POST
@router.path(pattern='api/load/left/articles/')
def load_left_articles(request):
    if request.method == 'POST':
        articles = g_as()[6:]
        articles = [{
            'id': article.id,
            'title': article.title,
            'content': article.plain_content()[:200],
            'cover': article.cover.url,
            'correlation_software': article.correlation_software,
            'created_time': article.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_time': article.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
            'user': {
                'id': article.user.id,
                'username': article.user.nickname if article.user.nickname else article.user.username,
                'email': article.user.email,
            }
        } for article in articles]
        if len(articles):
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': articles
            })
        else:
            return JsonResponse({
                'code': 404,
                'msg': 'failed with no data'
            })
    else:
        return JsonResponse({
            'code': 405,
            'msg': 'failed with wrong request action'
        })


@require_GET
def article_details(request):
    if request.method == 'GET':
        articles = g_as()
        try:
            article_id = request.GET.get('article_id')
            if article_id is None:
                raise ValueError
            else:
                article_id = article_id.replace(' ', '+')
                article_id = int(decrypt(article_id))
        except ValueError:
            return render(request, 'article_details.html', {
                'error': 'Invalid params',
                'code': 402
            })
        except TypeError:
            return render(request, 'article_details.html', {
                'error': 'Invalid params',
                'code': 401
            })
        matched_articles = [article for article in articles if article.id == article_id]
        if len(matched_articles) > 0:
            article = matched_articles[0]
        else:
            article = None
        if article:
            related_articles = [article for article in articles if article.id != article_id]
            related_articles = sorted(related_articles,
                                      key=lambda x: compute_similarity(article.plain_content(), x.plain_content()),
                                      reverse=True)[:6]
            related_software = [article.correlation_software for article in articles
                                if article.id == article_id and article.correlation_software]
            related_articles_count = len(related_articles)
            related_software_count = len(related_software)
            context_articles = get_context_articles(articles, article_id)
        else:
            return render(request, 'article_details.html', {
                'error': 'Not found article',
                'code': 404
            })
        return render(request, 'article_details.html', {
            'article': article,
            'context_articles': context_articles,
            'related_articles': related_articles,
            'related_articles_count': related_articles_count,
            'related_software': related_software,
            'related_software_count': related_software_count,
            'respond_comment': 'article'
        })
    else:
        return render(request, 'article_details.html', {
            'error': 'Not allowed request action',
            'code': 405
        })


@router.path(pattern='api/thumb/article/')
@require_POST
def thumb(request):
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            thumb_type = post_data['thumb_type']
            article_id = post_data['article_id']
            article_id = str(article_id.replace(' ', '+'))
            article_id = decrypt(article_id)
            article = Article.objects.get(id=article_id)
            if thumb_type == 'thumb':
                if article:
                    article.thumbs_volume += 1
                    article.save()
                    return JsonResponse({
                        'code': 200
                    })
                else:
                    return JsonResponse({
                        'code': 404,
                        'error': 'Error with not found article'
                    })
            elif thumb_type == 'de_thumb':
                if article:
                    article.thumbs_volume -= 1
                    article.save()
                    return JsonResponse({
                        'code': 200
                    })
                else:
                    return JsonResponse({
                        'code': 404,
                        'error': 'Error with not found article'
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


@router.path(pattern='api/publish/article/')
@require_POST
def publish_article(request):
    if request.method == 'POST':
        try:
            user = FrontEndUser.objects.get(username='vincent')
            title = request.POST.get('title')
            content = request.POST.get('content')
            cover = get_image_urls_from_md_str(content)
            if cover is None or len(cover) <= 0:
                cover = None
            else:
                cover = [c for c in cover if c.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']]
                if len(cover) > 0:
                    cover = cover[0].replace('/media/', '')
                else:
                    cover = None
            correlation_software_id = request.POST.get('correlation_software_id')
            if correlation_software_id:
                correlation_software = SoftWare.objects.get(id=correlation_software_id)
            else:
                correlation_software = None
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
        except AttributeError:
            return JsonResponse({
                'code': 400,
                'msg': 'failed with bad request body'
            })
        if cover:
            article = Article.objects.create(user=user, title=title, content=content,
                                             cover=cover, correlation_software=correlation_software)
        else:
            article = Article.objects.create(user=user, title=title, content=content,
                                             correlation_software=correlation_software)
        if article:
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': {
                    'article_id': article.id
                }
            })
        else:
            return JsonResponse({
                'code': 400,
                'msg': 'failed when inserting data to database'
            })
    else:
        return JsonResponse({
            'code': 301,
            'msg': 'failed with wrong request action'
        })
