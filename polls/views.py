from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.utils import timezone

# Create your views here.

def index(request):
    latest_question_text = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {'latest_question_text': latest_question_text}
    return render(request, 'polls/index.html', context)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}  # The Dict Key Used For Template to access data
    return render(request, 'polls/detail.html', context)



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'polls/results.html', context)



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {"question":question , "error_message":"You didn't select a Choice."}
        return render(request, 'polls/detail.html', context)
    
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))