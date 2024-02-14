import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            f'Год создания ({value}) не может быть больше текущего года'
        )
    return value
