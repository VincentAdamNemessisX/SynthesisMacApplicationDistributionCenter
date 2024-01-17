# Create your views here.
from django.shortcuts import render


def software_details(request):
    return render(request, 'frontenduser/software_details.html')
