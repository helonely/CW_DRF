from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )

    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='аватар',
        blank=True, null=True)

    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Телеграм chat-id",
        blank=True, null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
