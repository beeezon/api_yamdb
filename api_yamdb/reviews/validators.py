import datetime as dt

from django.core.exceptions import ValidationError


def current_year_validator(data):
    if dt.datetime.now().year < data:
        raise ValidationError(
            '''
            Путешествия в будущее запрещены!
            Год создения произведения не может быть позже текущего!
            '''
        )
    return data
