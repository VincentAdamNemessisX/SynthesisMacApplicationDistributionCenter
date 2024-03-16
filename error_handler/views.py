from django.shortcuts import render


# Create your views here.
def custom_404_view(request, exception):
    return render(request, '404.html',{
        'code': 404,
        'error': exception
    }, status=404)


def custom_500_view(request):
    return render(request, '500.html',{
        'code': 500,
        'error': '服务器异常'
    }, status=500)
