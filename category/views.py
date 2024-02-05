# Create your views here.
from django.shortcuts import render
from django_router import router


@router.path(pattern='')
def category(request):
    if request.method == 'GET':
        return render(request, 'category.html')
    else:
        return render(request, 'category.html')
