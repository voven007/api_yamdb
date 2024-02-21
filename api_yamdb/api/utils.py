from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.models import MyUser


def send_confirmation_code_on_email(username, email):
    user = get_object_or_404(MyUser, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Confirmation code for YaMDb',
              message=f'Ваш код {confirmation_code}',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[email])