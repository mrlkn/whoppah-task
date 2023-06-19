from celery import shared_task
from django.core.mail import send_mail
from requests import ReadTimeout


@shared_task(bind=True, autoretry_for=(Exception, ConnectionError, ReadTimeout, ), retry_backoff=True, retry_kwargs={'max_retries': 10})
def send_email_task(self, recipient_email: str, subject: str, message: str) -> None:
    """
    Send an email asynchronously using Celery with automatic retries in case of failure.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        message (str): The message body of the email.

    Retries:
        The task will automatically retry for exceptions (Exception, ConnectionError, ReadTimeout)
        with an exponential backoff algorithm. It will be retried up to 10 times.
    """

    sender_email = 'info@whoppah.com'

    send_mail(
        subject,
        message,
        sender_email,
        [recipient_email],
        fail_silently=False,
    )
