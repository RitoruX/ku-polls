import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """
    Class for question contains question and publish date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date closed')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Method checks this question is recently published.

        Returns:
            bool: Is question recently published.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
    def is_published(self):
        return timezone.now() > self.pub_date

    def can_vote(self):
        return self.end_date > timezone.now() > self.pub_date
        
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    is_published.boolean = True
    is_published.short_description = 'Is published?'

    can_vote.boolean = True
    can_vote.short_description = 'Can vote?'

class Choice(models.Model):
    """
    Class for choice in each questions.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return self.question.vote_set.filter(choice=self).count()

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)