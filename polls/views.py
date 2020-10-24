from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """Class show Index page preview."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]
<<<<<<< HEAD

=======
>>>>>>> 3f01680f97fabf245a06a804d510d161b1cdc329

class DetailView(generic.DetailView):
    """Class show Detail page preview."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class show Result page preview."""

    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """Check selected vote choice and update vote score."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def vote_for_poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f"This poll isn't in vote period.")
        return redirect('polls:index')
<<<<<<< HEAD
    return render(request, 'polls/detail.html', {'question': question})
=======
    return render(request, 'polls/detail.html', {
            'question': question})
>>>>>>> 3f01680f97fabf245a06a804d510d161b1cdc329
