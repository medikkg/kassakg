from django.db.models import TextChoices

class ClientTypeChoice(TextChoices):
    INDIVIDUAL = 'Физ.лицо'
    ENTITY = 'Юр.лицо'
