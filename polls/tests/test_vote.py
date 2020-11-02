from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models import Question
from django.contrib.auth.models import User
import datetime

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    Question that be created by this method has period 5 seconds.
    """
    start_date = timezone.now() + datetime.timedelta(days=days)
    end_date = timezone.now() + datetime.timedelta(seconds=5) + + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=start_date, end_date=end_date)

class VoteTest(TestCase):
        
    def test_authenticated_vote(self):
        user = User.objects.create_user(username='username', password='1101', email='mails@gmail.com')
        response = self.client.post(reverse('login'), {'username': 'username', 'password': '1101'}, follow=True)
        question = create_question(question_text='tester', days=1)
        choice = question.choice_set.create(choice_text="choice")
        question.vote_set.create(user=user, question=question, choice=choice)
        self.assertEqual(response.status_code, 200)

    def test_non_authenticated_vote(self):
        user = User.objects.create_user(username='username', password='1101', email='mails@gmail.com')
        question = create_question(question_text='tester', days=1)
        choice = question.choice_set.create(choice_text="choice")
        question.vote_set.create(user=user, question=question, choice=choice)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)