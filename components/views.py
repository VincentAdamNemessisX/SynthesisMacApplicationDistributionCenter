from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from general.data_handler import handle_uploaded_image, unload_image_from_server
from general.init_cache import get_all_software, get_all_articles, get_all_user


# Create your views here.


@router.path(pattern='api/upload/article/image/')
@require_POST
def upload_article_image(request):
    if request.method == 'POST':
        image = request.FILES.get('upload')
        if image:
            try:
                image_url = handle_uploaded_image(image, 'article/content/')
                if image_url:
                    return JsonResponse({'url': "/media/" + image_url})
                else:
                    return JsonResponse({'error': {'message': 'Failed to upload image'}})
            except Exception as e:
                return JsonResponse({'error': {'message': str(e)}})
        else:
            return JsonResponse({'error': {'message': 'No image found'}})
    else:
        return JsonResponse({'error': {'message': 'Invalid request method'}})


@router.path(pattern='api/upload/profile/image/')
@require_POST
def upload_profile_image(request):
    if request.method == 'POST':
        image = request.FILES.get('upload')
        if image:
            try:
                image_url = handle_uploaded_image(image, 'profile/')
                if image_url:
                    return JsonResponse({'url': "/media/" + image_url})
                else:
                    return JsonResponse({'error': {'message': 'Failed to upload image'}})
            except Exception as e:
                return JsonResponse({'error': {'message': str(e)}})
        else:
            return JsonResponse({'error': {'message': 'No image found'}})
    else:
        return JsonResponse({'error': {'message': 'Invalid request method'}})


@router.path(pattern='api/unload/image/')
@require_POST
def unload_image(request):
    if request.method == 'POST':
        image_url = request.POST.get('url')
        if image_url:
            try:
                unload_image_from_server(image_url)
                return JsonResponse({'message': 'Image unloaded successfully'})
            except Exception as e:
                return JsonResponse({'error': {'message': str(e)}})
        else:
            return JsonResponse({'error': {'message': 'No image found'}})
    else:
        return JsonResponse({'error': {'message': 'Invalid request method'}})


@require_GET
def search_result(request):
    if request.method == 'GET':
        search_str = request.GET.get('s')
        matched_software = []
        if search_str:
            try:
                matched_software = [
                    x for x in get_all_software()
                    if (search_str in x.name or
                        search_str in x.description or
                        search_str in x.tags)
                ]
            except TypeError:
                matched_software = [
                    x for x in get_all_software()
                    if (search_str in x.name or
                        search_str in x.description)
                ]
            matched_articles = [x for x in get_all_articles() if search_str in x.title
                                or search_str in x.content]
            matched_user = [x for x in get_all_user() if search_str in x.username
                            or search_str in x.nickname]
            matched_software_count = len(matched_software)
            matched_articles_count = len(matched_articles)
            matched_user_count = len(matched_user)
            return render(request, 'front/search_result.html', {
                'search_str': search_str,
                'matched_software': matched_software,
                'matched_software_count': matched_software_count,
                'matched_articles': matched_articles,
                'matched_articles_count': matched_articles_count,
                'matched_user': matched_user,
                'matched_user_count': matched_user_count,
            })
        else:
            return render(request, 'front/search_result.html', {
                'error': 'invalid params',
                'code': 402
            })
    else:
        return render(request, 'front/search_result.html', {
            'error': 'invalid request action',
            'code': 403
        })


@require_GET
def home(request):
    if request.method == 'GET':
        all_software = get_all_software()
        all_articles = get_all_articles()
        latest_articles = sorted(all_articles, key=lambda x: x.created_time, reverse=True)[:10]
        latest_articles_count = len(latest_articles)
        for cat in request.categories:
            cat.software = [sof for sof in all_software if sof.category.id == cat.id][:20]
            cat.software_count = len(cat.software)
        return render(request, 'home.html', {
            'latest_articles': latest_articles,
            'latest_articles_count': latest_articles_count,
        })
