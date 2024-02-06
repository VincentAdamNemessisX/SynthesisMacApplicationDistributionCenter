# Create your views here.

from django.shortcuts import render
from django.views.decorators.http import require_GET
from django_router import router

from general.init_cache import get_all_category
from general.encrypt import decrypt


@require_GET
@router.path(pattern='')
def category(request):
    if request.method == 'GET':
        categories = get_all_category()
        if len(categories) <= 0:
            return render(request, 'category.html',
                          {
                              'code': 406,
                              'error': 'Cache init failed, please contact the administrator.',
                          })
        try:
            category_id = request.GET.get('category_id').replace(' ', '+')
            if category_id is None:
                return render(request, 'category.html',
                              {
                                  'code': 402,
                                  'error': 'wrong category_id',
                              })
            category_id = int(decrypt(category_id))
        # except ValueError:
        #     return render(request, 'category.html',
        #                   {
        #                       'code': 401,
        #                       'error': 'invalid category_id',
        #                   })
        except TypeError:
            return render(request, 'category.html',
                          {
                              'code': 400,
                              'error': 'wrong type of category_id',
                          })
        current_category_list = [cate for cate in categories if cate.id == category_id]
        if len(current_category_list) > 0:
            current_category = current_category_list[0]
            return render(request, 'category.html',
                          {
                              'category': current_category,
                              'software_set': current_category.software_set.all(),
                          })
        else:
            return render(request, 'category.html',
                          {
                              'code': 404,
                              'error': 'category not found',
                          })
    else:
        return render(request, 'category.html', {
            'code': 405,
            'error': 'invalid request action',
        })
