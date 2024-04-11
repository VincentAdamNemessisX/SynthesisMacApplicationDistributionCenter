# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from general.encrypt import decrypt
from general.init_cache import get_all_questions, get_all_answer


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
        try:
            question_id = request.GET.get('question_id').replace(' ', '+')
            question_id = int(decrypt(question_id))
        except Exception as e:
            return render(request, '500.html', {
                'code': 500,
                'error': '参数异常，' + str(e)
            })
        question = None
        if question_id:
            try:
                question = [q for q in get_all_questions() if q.id == question_id]
                if len(question) == 1:
                    question = question[0]
                else:
                    question = None
            except Exception as e:
                return render(request, '500.html', {
                    'code': 500,
                    'error': '参数异常，' + str(e)
                })
        if question:
            answer = [a for a in get_all_answer() if a.question_id == question.id]
            return render(request, 'question.html', {
                'question': question,
                'answer': answer
            })
        return render('404.html', {
            'code': 404,
            'error': '未找到相关问题，可能已被删除'
        })
    return render(request, '404.html', {
        'code': 403,
        'error': '请求方式不正确，未能找到页面'
    })


@require_POST
@login_required
@router.path('api/adopt/answer/')
def adopt_answer(request):
    if request.method == 'POST':
        try:
            question_id = int(request.POST.get('question_id'))
            answer_id = int(request.POST.get('answer_id'))
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': '参数异常，' + str(e)})
        question = [q for q in get_all_questions() if q.id == question_id]
        question_answer = [a for a in get_all_answer() if a.question_id == question_id and a.is_adopt == 1]
        if len(question_answer) > 0:
            for a in question_answer:
                a.is_adopt = 0
                a.save()
        answer = [a for a in get_all_answer() if a.id == answer_id]
        if len(question) == 1 and len(answer) == 1:
            question, answer = question[0], answer[0]
            if request.session.get('logon_user').id != question.publisher.id:
                return JsonResponse({'code': 402, 'msg': '越权操作，非楼主采纳回复'})
            question.state, answer.is_adopt = 1, 1
            question.save(), answer.save()
            return JsonResponse({'code': 200, 'msg': '已采纳'})
    else:
        return JsonResponse({'code': 404, 'msg': '参数异常，未找到问题或回复'})
    return JsonResponse({'code': 403, 'msg': '不允许的请求方式'})


@require_POST
@login_required
@router.path('api/publish/answer/')
def publish_answer(request):
    pass


@require_POST
@login_required
@router.path('api/publish/question/')
def publish_question(request):
    pass
