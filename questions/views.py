# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django_router import router

from general.init_cache import get_all_questions as g_a_q


@router.path(pattern='api/get/all/question/', name='get_all_questions')
@require_POST
def get_all_questions(request):
    if request.method == 'POST':
        # if request.method == 'GET':
        # start_time = time.time()
        questions = g_a_q()
        questions = [
            {
                'question_id': question.id,
                'question': question.question,
                'question_state': question.question_state,
                'publisher': {
                    'username': question.publisher.username,
                    'email': question.publisher.email,
                },
                'created_time': question.created_time,
                'updated_time': question.updated_time,
                'answers': [
                    {
                        'answer_id': answer.id,
                        'content': answer.content,
                        'respondent': answer.respondent.username,
                        'created_time': answer.created_time,
                    }
                    for answer in question.answer_set.all()
                ]
            }
            for question in questions
        ]
        # print('get_all_questions used time: ', time.time() - start_time)
        if questions:
            if len(questions) > 0:
                return JsonResponse({'code': 200, 'msg': 'succeed', 'data': questions})
            else:
                return JsonResponse({'code': 404, 'msg': 'failed with no data'})
        else:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid data'})
    else:
        return JsonResponse({'code': 405, 'msg': 'failed with invalid request action'})


@router.path(pattern='api/get/specific/user/question/', name='get_specific_user_questions')
# @require_POST
def get_all_questions(request):
    # if request.method == 'POST':
    if request.method == 'GET':
        # start_time = time.time()
        # username = request.POST.get('username')
        try:
            username = str(request.GET.get('username'))
        except ValueError:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid params'})
        except TypeError:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid params'})
        questions = g_a_q()
        questions = [quest for quest in questions if quest.publisher.username == username]
        questions = [
            {
                'question_id': question.id,
                'question': question.question,
                'question_state': question.question_state,
                'publisher': {
                    'username': question.publisher.username,
                    'email': question.publisher.email,
                },
                'created_time': question.created_time,
                'updated_time': question.updated_time,
                'answers': [
                    {
                        'answer_id': answer.id,
                        'content': answer.content,
                        'respondent': answer.respondent.username,
                        'created_time': answer.created_time,
                    }
                    for answer in question.answer_set.all()
                ]
            }
            for question in questions
        ]
        # print('get_all_questions used time: ', time.time() - start_time)
        if questions:
            if len(questions) > 0:
                return JsonResponse({'code': 200, 'msg': 'succeed', 'data': questions})
            else:
                return JsonResponse({'code': 404, 'msg': 'failed with no data'})
        else:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid data'})
    else:
        return JsonResponse({'code': 405, 'msg': 'failed with invalid request action'})


@router.path(pattern='api/get/single/question/', name='get_specific_question')
@require_POST
def get_specific_question(request):
    if request.method == 'POST':
        # if request.method == 'GET':
        question_id = request.POST.get('question_id')
        # question_id = request.GET.get('question_id')
        if question_id:
            try:
                question_id = int(question_id)
                if question_id < 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({'code': 402, 'msg': 'failed with invalid params'})
            except TypeError:
                return JsonResponse({'code': 402, 'msg': 'failed with invalid params'})
        else:
            return JsonResponse({'code': 405, 'msg': 'failed with invalid request action'})
        questions = g_a_q()
        if questions and len(questions) > 0:
            question = [quest for quest in questions if quest.id == question_id]
            if question and len(question) > 0:
                question = question[0]
                question = {
                    'question_id': question.id,
                    'question': question.question,
                    'question_state': question.question_state,
                    'publisher': {
                        'username': question.publisher.username,
                        'email': question.publisher.email,
                    },
                    'created_time': question.created_time,
                    'updated_time': question.updated_time,
                    'answers': [
                        {
                            'answer_id': answer.id,
                            'content': answer.content,
                            'respondent': answer.respondent.username,
                            'created_time': answer.created_time,
                        }
                        for answer in question.answer_set.all()
                    ]
                }
                return JsonResponse({'code': 200, 'msg': 'succeed', 'data': question})
            else:
                return JsonResponse({'code': 404, 'msg': 'failed with no data'})
        else:
            return JsonResponse({'code': 402, 'msg': 'failed with invalid data'})
    else:
        return JsonResponse({'code': 405, 'msg': 'failed with invalid request action'})


@require_GET
def question(request):
    return render(request, 'question.html')
