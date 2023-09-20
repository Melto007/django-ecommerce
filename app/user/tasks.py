from celery import shared_task
import pyotp
from django.core import mail
from core.models import TwoFactorAuthentication
import datetime


@shared_task
def mail_sharedTask(user_id, email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    secret = totp.secret
    with mail.get_connection() as connection:
        result = mail.EmailMessage(
            "Subject here",
            f"Your validation code is {otp}",
            "from@example.com",
            [email],
            connection=connection,
        ).send()

        if result:
            time = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
            obj = {
                'user': user_id,
                'two_factor_auth': secret,
                'expired_at': time
            }
            TwoFactorAuthentication.objects.update_or_create(
                user=user_id,
                defaults=obj
            )
        else:
            raise ValueError('Failed to send mail')
