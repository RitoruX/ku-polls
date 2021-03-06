from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_out, user_logged_in, user_login_failed
from django.dispatch import receiver
# from django.utils.decorators import method_decorator
# from django.contrib.auth.forms import UserCreationForm

from mysite.settings import LOGGING
import logging.config

from .models import Choice, Question, Vote

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("polls")

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

@login_required
def vote(request, question_id):
    """Check selected vote choice and update vote score."""
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=user).exists():
            selected_vote = question.vote_set.get(user=user)
            selected_vote.choice = selected_choice
            selected_vote.save()
        else:
            Vote.objects.update_or_create(question=question, choice=selected_choice, user=request.user)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def vote_for_poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f"This poll isn't in vote period.")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def logged_in_logging(sender, request, user, **kwargs):
    logger.info(f"{user.username} has logged in to {get_client_ip(request)}")


@receiver(user_logged_out)
def logged_out_logging(sender, request, user, **kwargs):
    logger.info(f"{user.username} has logged out from {get_client_ip(request)} ")


@receiver(user_login_failed)
def logged_in_failed_logging(sender, request, credentials, **kwargs):
    logger.warning(f"{request.POST['username']} has login failed with {get_client_ip(request)}")

# def signup(request):
#     form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})
