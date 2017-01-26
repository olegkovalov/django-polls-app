from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Poll(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='author', related_name='polls')
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question


class Choice(models.Model):

    poll = models.ForeignKey(Poll, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


@receiver(post_save, sender=Poll)
def send_emails(sender, instance, created, **kwargs):
    if created:
        from polls.tasks import send_email_about_new_poll
        send_email_about_new_poll.delay(instance.pk)
