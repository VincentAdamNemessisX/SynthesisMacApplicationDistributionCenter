from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'frontenduser/index.html')


def generic(request):
    return render(request, 'frontenduser/generic.html')


def help(request):
    return render(request, 'frontenduser/help.html')


def elements(request):
    return render(request, 'frontenduser/elements.html')
