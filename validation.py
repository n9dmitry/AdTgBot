import re

# Функция полиморфная


async def validate_button_input(event_text, options):
    return event_text in options
# Используется для:
# car_body_type
# car_engine_type
# car_transmission_type
# car_color
# car_document_status
# car_owners
# car_customs_cleared
# car_condition
# select_currency
# Конец функции


async def validate_car_brand(car_brand, valid_brands):
    return car_brand in valid_brands


async def validate_car_model(selected_model, valid_models):
    return selected_model.lower() in [model.lower() for model in valid_models]


async def validate_year(year):
    return bool(re.match(r'^(19|20)\d{2}$', year)) and int(year) <= 2024


# get_car_body_type - КНОПКИ
# get_car_engine_type - КНОПКИ

async def validate_engine_volume(volume):
    try:
        volume = float(volume)
        return 0.2 <= volume <= 10.0
    except ValueError:
        return False



async def validate_car_power(power):
    if power.isdigit():
        power_int = int(power)
        return 50 <= power_int <= 1000

# get_car_transmission_type - КНОПКИ
# get_car_color - КНОПКИ


async def validate_car_mileage(mileage):
    return mileage.lower() == 'новый' or (mileage.isdigit() and 0 < int(mileage))


async def validate_car_description(description):
    return not description.isdigit()


async def validate_car_price(price):
    return price.isdigit() and int(price) > 0


async def validate_car_location(location):
    return not location.isdigit()


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

async def validate_length_text(event):
    return len(event.text) <= 400

async def validate_final_length(event, state, user_data):
    caption_length = 350
    max_caption_length = 1024

    user_data_length = sum(len(str(value)) for value in user_data.values())
    print(user_data_length, (user_data_length + caption_length), max_caption_length)
    return (user_data_length + caption_length) <= max_caption_length


