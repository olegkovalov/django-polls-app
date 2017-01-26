from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from polls.models import Poll
from project.celery_app import app as celery_app


@celery_app.task
def send_email_about_new_poll(poll_pk: int):
    try:
        poll = Poll.objects.get(pk=poll_pk)
    except Poll.DoesNotExist:
        pass
    else:
        send_mail(
            'New poll',
            render_to_string('polls/new_poll_email.txt', {'poll': poll}),
            settings.POLLS_FROM_EMAIL,
            list(get_user_model().objects.exclude(pk=poll.author.pk).values_list('email', flat=True)),
            fail_silently=False,
        )
