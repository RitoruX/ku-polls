import datetime

from django.test import TestCase
from django.utils import timezone
from ..models import Question

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

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_past_question_is_published(self):
        """
        Past question must be already published.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        self.assertTrue(past_question.is_published())

    def test_future_question_is_published(self):
        """
        Future question must be published yet.
        """
        future_question = create_question(question_text='Future question.', days=5)
        self.assertFalse(future_question.is_published())

    def test_now_question_is_published(self):
        """
        Question in period should already be published.
        """
        now_question = create_question(question_text='Now Question.', days=0)
        self.assertTrue(now_question.is_published())

    def test_question_in_period_can_vote(self):
        """
        Question in vote period must can be voted.
        """
        in_period_question = create_question(question_text='In Period Quesion', days=0)
        self.assertTrue(in_period_question.can_vote())

    def test_question_out_of_period_can_vote(self):
        """
        Closed question must can not be voted.
        """
        out_of_period_question = create_question(question_text='Out of Period Quesion', days=-10)
        self.assertFalse(out_of_period_question.can_vote())