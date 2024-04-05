from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from board.models import Announcement, Response, News
from project import settings
from accounts.models import User


def send_notifications(text, pk, template_name, subject, email):
    announcement_link = f'http://127.0.0.1:8000/bb/{pk}'
    html_content = render_to_string(
        template_name,
        {
            'link': announcement_link,
            'text': text
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def new_resp(sender, instance, created, **kwargs):
    if created and not instance.accepted:
        announcement_author_email = instance.announcement.user.email
        send_notifications(instance.text, instance.announcement.pk, 'user_responsed.html', 'Новый отклик',
                           [announcement_author_email])
    else:
        response_author_email = instance.user.email
        send_notifications(instance.text, instance.announcement.pk, 'response_accepted.html', 'Ваш отклик приняли',
                           [response_author_email])


@receiver(post_save, sender=News)
def send_news_email(sender, instance, **kwargs):
    subject = instance.heading
    message = instance.text
    from_email = settings.DEFAULT_FROM_EMAIL
    users_emails = [user.email for user in User.objects.all()]
    html_content = render_to_string(
        'news_send.html',
        {
            'text': message
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=from_email,
        to=users_emails
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

