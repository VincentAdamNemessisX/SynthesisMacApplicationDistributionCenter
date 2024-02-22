from django.shortcuts import render
from django_router import router

# Create your views here.
@router.path(pattern='test/')
def test_modal(request):
    return render(request, 'frontenduser/test_for_download_modal.html')