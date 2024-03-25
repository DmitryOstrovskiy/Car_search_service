from django.core.exceptions import ValidationError
import string

def validate_unique_number(value):
    if not (1000 <= int(value[:-1]) <= 9999) or not (value[-1].isupper() and value[-1] in string.ascii_uppercase):
        raise ValidationError('Уникальный номер должен быть в формате "1234A"')