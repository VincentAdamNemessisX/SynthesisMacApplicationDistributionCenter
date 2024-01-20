# Create your views here.
from django.shortcuts import render
from django_router import router


@router.path(pattern='')
def software_details(request):
    return render(request, 'frontenduser/software_details.html')
