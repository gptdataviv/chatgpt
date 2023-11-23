from django.http import HttpResponse
from .apis.prompt import prompt
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def process_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        answer_text = prompt.gptprompt(question_text)
        return HttpResponse(answer_text)
    else:
        return render(request, 'index.html')