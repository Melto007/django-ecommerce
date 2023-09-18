import django
django.setup()
from app.celery import app
from django.core.mail import send_mail
from core.models import TwoFactorAuth
import random
import math


def random_string():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


@app.task(queue='tasks')
def sendcode(id, email):
    try:
        random_value = random_string()
        res = send_mail(
            subject='Authentication Code',
            message=f"Authentication code for login user {random_value}",
            from_email="from@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        user = TwoFactorAuth.objects.filter(user=id).first()
        if user:
            user.delete()

        if res == 1:
            TwoFactorAuth.objects.create(
                user=id,
                token=random_value,
            )
            return res
        raise ValueError('Email not send')
    except Exception as e:
        raise ValueError('email not send', e)
