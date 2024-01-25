# Create your views here.
# from general.init_cache import get_favorite_article, get_favorite_software
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django_router import router

from .models import FrontEndUser


@router.path(pattern='api/get/favorite/articles/')
# @require_POST
def get_favorite_article(request):
    # user = FrontEndUser.objects.get(username=request.user.username)
    return JsonResponse({'code': 200, 'msg': 'success', 'data': []})
