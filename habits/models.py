from django.db import models

from config import settings


class Habit(models.Model):
    CHOICES_PERIOD = [
        ("minutes", "минуты"),
        ("hours", "часы"),
        ("days", "дни"),
    ]
    name = models.CharField(
        max_length=100, verbose_name='название привычки',
        blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец привычки",
        blank=True, null=True,
    )
    place = models.CharField(max_length=75, verbose_name='Место привычки')
    time = models.TimeField(verbose_name='Время дня привычки')
    action = models.CharField(max_length=75, verbose_name='Действие привычки')
    is_nice_habit = models.BooleanField(verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Связанная привычка"
    )

    frequency_number = models.PositiveIntegerField(verbose_name="Количество раз")

    frequency_unit = models.CharField(
        max_length=10,
        choices=CHOICES_PERIOD,
        default="days",
        verbose_name="Единицы измерения",
    )

    reward = models.CharField(
        max_length=200, verbose_name="Вознаграждение",
        blank=True, null=True
    )

    duration = models.DurationField(verbose_name="Длительность действия")
    is_public = models.BooleanField(default=True, verbose_name="Публичная")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
