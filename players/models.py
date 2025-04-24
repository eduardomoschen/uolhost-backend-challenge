from django.db import models
from django.core.validators import RegexValidator


class Group(models.TextChoices):
    JUSTICE_LEAGUE = 'JL', 'Liga da Justiça',
    AVENGERS = 'A', 'Os Vingadores'


class Player(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
            message='Invalid phone number. Use the format (99) 99999-9999.',
        )]
    )
    alias = models.CharField(max_length=255)
    group = models.CharField(
        max_length=255,
        choices=Group.choices,
        default=Group.JUSTICE_LEAGUE
    )
    reference = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f'{self.name} - {self.alias} - {self.get_group_display()}'
