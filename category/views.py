# Create your views here.
from django.shortcuts import render


def category(request):
    if request.method == 'GET':
        return render(request, 'category.html')
    else:
        return render(request, 'category.html')
