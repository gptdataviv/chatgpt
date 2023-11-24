from django.http import HttpResponse,JsonResponse
from .apis.prompt import prompt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db import connection
from gptapis.models import RequestsData
import tiktoken

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
@csrf_exempt
def get_answer(request):
    try:
        question_text = request.GET.get('question_text')
        
        # Validate the question text
        if len(question_text) < 10:
            # Raise an error if the question text is too short
            status_code = 101
            raise ValueError("Question text is too short")

        if len(question_text) > 500:
            # Raise an error if the question text is too long
            status_code = 102
            raise ValueError("Question text is too long")
        
        answer_text = prompt.gptprompt(question_text)

        # Create an instance of RequestsData
        new_request = RequestsData(
            request_data=question_text,
            response_data=answer_text
        )
        
        # Save to the database
        new_request.save()

        status_code = 100
        response = {
            "error_code":status_code,
            "status":"success",
            "message":f"Response fetched",
            "data":str(answer_text)
        }
    
    except Exception as e:
        print(e)
        response = {
            "error_code":'status_code',
            "status":"Error occured",
            "message":str(e)
        }
    return JsonResponse(response, safe=False)

def process_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        answer_text = prompt.gptprompt(question_text)
        return HttpResponse(answer_text)
    else:
        return render(request, 'index.html')