# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router
from general.init_cache import get_all_questions


@require_GET
def init_questions(request):
    if request.method == 'GET':
        all_question = sorted(sorted(get_all_questions(), key=lambda q: q.state, reverse=False),
                              key=lambda q: q.updated_time, reverse=True)
        all_question_count = len(all_question) if all_question else 0
        init_quests = all_question[:6]
        # write_something()
        return render(request, 'question_list.html', {
            'questions': init_quests,
            'questions_count': all_question_count
        })
    return render(request, '404.html', {
        'code': 403,
        'error': '请求方式不正确，页面未找到'
    })


@router.path('api/get/left/questions/')
@require_POST
def load_left_questions(request):
    if request.method == 'POST':
        all_question = sorted(sorted(get_all_questions(), key=lambda q: q.state, reverse=False),
                              key=lambda q: q.updated_time, reverse=True)
        left_quests = all_question[6:]
        left_quests = [
            {
                'id': q.id,
                'title': q.title(),
                'state': q.state,
                'question': q.short_question(),
                'created_day': q.created_time.day,
                'created_month': q.created_time.month,
                'created_year': q.created_time.year,
            } for q in left_quests
        ]
        return JsonResponse({'code': 200, 'questions': left_quests})
    return JsonResponse({'code': 403, 'error': '请求方式不正确，未能找到页面'})


@router.path('question/details/')
@require_GET
def question_details(request):
    if request.method == 'GET':
        return render(request, 'question.html')
    return render(request, '404.html', {
        'code': 403,
        'error': '请求方式不正确，未能找到页面'
    })
