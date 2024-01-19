import re

async def validate_name(name):
    return bool(re.match(r'^[A-Za-zА-Яа-я\s]+$', name, re.UNICODE))


async def validate_phone_number(phone_number):
    # Уберем все нецифровые символы и проверим, что остались только цифры
    phone_digits = re.sub(r'\D', '', phone_number)

    # Проверим, что номер содержит 10 или 11 цифр
    if re.match(r'^\+?[78]\d{10}$', phone_digits) or re.match(r'^\+?\d{11}$', phone_digits):
        return True
    else:
        return False