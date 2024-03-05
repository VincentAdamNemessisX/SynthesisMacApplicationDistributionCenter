from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django_router import router

from general.data_handler import handle_uploaded_image, unload_image_from_server


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