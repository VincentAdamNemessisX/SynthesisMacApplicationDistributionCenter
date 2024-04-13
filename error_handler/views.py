from django.shortcuts import render
from django_router import router


# Create your views here.
@router.path(pattern='404/')
def custom_404_view(request, exception):
    # def custom_404_view(request):
    return render(request, '404.html', {
        'code': 404,
        'err': exception
        # 'err': 'not found'
    })


@router.path(pattern='500/')
def custom_500_view(request):
    return render(request, '500.html', {
        'code': 500,
        'err': '服务器异常'
    })
