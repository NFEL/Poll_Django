from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class Question(models.Model):
    name = models.CharField("question name", max_length=50)
    date = models.DateTimeField(auto_now=True)
    total_vote_count = models.IntegerField(
        _("total number of votes"), default=0)

    def __str__(self) -> str:
        return f'{self.name} -> {self.total_vote_count}'


class Choice(models.Model):
    name = models.CharField(_("name of choice"), max_length=50)
    question = models.ForeignKey(Question, verbose_name=_(
        "question name"), on_delete=models.CASCADE, related_name='choice')
    votes_count = models.IntegerField(_("number of votes"), default=0)

    def __str__(self) -> str:
        return f'{self.question.name} ({self.id} - {self.name}) '


class UserVote(models.Model):
    user_id = models.ForeignKey(User, verbose_name=_(
        "User votes"), on_delete=models.CASCADE)

    vote = models.ForeignKey(Choice, verbose_name=_(
        "Choice"), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_(
        "Question"), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vote', 'user_id'],
                name='one_vote_Question'),
            models.UniqueConstraint(
                fields=['user_id', 'question'],
                name='one_vote_perQuestion')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vote.votes_count += 1
        self.vote.save()
        self.vote.question.total_vote_count += 1
        self.vote.question.save()
        return

    def __str__(self) -> str:
        return f'{self.user_id.username} -> {self.vote.name} on question {self.vote.question.name}'
