# import logging
# import random
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils import executor
#
# API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
# API_TOKEN2 = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# GROUP_ID = '@autoxyibot1'
#
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=API_TOKEN2)
# dp = Dispatcher(bot)
#
# user_data = {}
# # Пример работы с user_data
# # async def handle_location(message: types.Message):
# #     location = message.text
# #     user_data[message.chat.id]['location'] = location
#
# # Клавиатура с быстрыми ссылками
# main_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton("Мои объявления")],
#         [KeyboardButton("Разместить объявление")],
#     ],
#     resize_keyboard=True
# )
#
# # ===Названия переменных===
# # car_brand
# # car_model
# # car_year
# # car_body_type  (кузов)
# # car_engine_type (тип двигателя)
# # car_engine_volume (объём)
# # car_power (мощность)
# # car_transmission_type
# # car_color
# # car_mileage (пробег)
# # car_document_status
# # car_owners
# # car_customs_cleared (растаможка)
# # car_photo
# # car_description
# # car_price
# # car_location
# # seller_name
# # seller_phone
#
# # Список моделей автомобилей
# car_models = {
#     'Ввести свою марку': [],
#     # 'Audi': ['Ввести марку', 'A3', 'A4', 'Q5', 'Q7'],
#     # 'BMW': ['Ввести марку', '3 Series', '5 Series', 'X3', 'X5'],
#     # 'Mercedes-Benz': ['Ввести марку', 'C-Class', 'E-Class', 'GLC', 'GLE'],
#     # 'Chevrolet': ['Ввести марку', 'Cruze', 'Malibu', 'Equinox', 'Tahoe'],
#     # 'Ford': ['Ввести марку', 'Focus', 'Fusion', 'Escape', 'Explorer'],
#     # 'Honda': ['Ввести марку', 'Civic', 'Accord', 'CR-V', 'Pilot'],
#     # 'Hyundai': ['Ввести марку', 'Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
#     # 'Kia': ['Ввести марку', 'Optima', 'Sorento', 'Sportage', 'Telluride'],
#     # 'Nissan': ['Ввести марку', 'Altima', 'Maxima', 'Rogue', 'Pathfinder'],
#     # 'Toyota': ['Ввести марку', 'Camry', 'Corolla', 'Rav4', 'Highlander'],
#     # 'Volkswagen': ['Ввести марку', 'Golf', 'Jetta', 'Tiguan', 'Atlas'],
#     # 'Volvo': ['Ввести марку', 'S60', 'S90', 'XC60', 'XC90'],
#     # 'Ferrari': ['Ввести марку', '488', 'F8 Tributo', 'Portofino', 'SF90 Stradale'],
#     # 'Porsche': ['Ввести марку', '911', 'Cayenne', 'Panamera', 'Macan'],
#     # 'Tesla': ['Ввести марку', 'Model S', 'Model 3', 'Model X', 'Model Y'],
#     # 'Lamborghini': ['Ввести марку', 'Huracan', 'Aventador', 'Urus'],
#     # 'Jaguar': ['Ввести марку', 'XE', 'XF', 'F-Pace', 'I-Pace'],
#     # 'Land Rover': ['Ввести марку', 'Discovery', 'Range Rover Evoque', 'Range Rover Sport', 'Defender'],
#     # 'Mazda': ['Ввести марку', 'Mazda3', 'Mazda6', 'CX-5', 'CX-9'],
#     # 'Subaru': ['Ввести марку', 'Impreza', 'Outback', 'Forester', 'Ascent'],
#     # 'LADA': ['Ввести марку', 'Vesta', 'Granta', 'XRAY', '4x4'],
#     # 'УАЗ': ['Ввести марку', 'Patriot', 'Hunter', 'Bukhanka'],
#     # 'ГАЗ': ['Ввести марку', 'Sobol', 'Next', 'Gazelle'],
#     # 'КАМАЗ': ['Ввести марку', '5490', '6520', '43118'],
#     # 'АвтоВАЗ': ['Ввести марку', 'LADA 4x4', 'LADA Kalina', 'LADA Priora', 'LADA XRAY']
# }
#     # Добавьте другие бренды
#
# # Обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Привет! Нажми на кнопку 'Разместить объявление', чтобы начать.", reply_markup=main_keyboard)
#
# # Обработчик кнопки "Разместить объявление"
# @dp.message_handler(lambda message: message.text == "Разместить объявление")
# async def place_ad(message: types.Message):
#     markup = InlineKeyboardMarkup(row_width=2)
#     brands = list(car_models.keys())
#     buttons = [InlineKeyboardButton(brand, callback_data=f"brand_{brand}") for brand in brands]
#     markup.add(*buttons)
#
#     await message.answer("Введите марку автомобиля или выберите из списка:", reply_markup=markup)
#
# @dp.message_handler(lambda message: message.text == "Мои объявления")
# async def my_ads(message: types.Message):
#     ()
#
# # Обработчик нажатия кнопки с маркой автомобиля
# #!!!! Дописать кнопочный функционал. Пока что работают только инпуты
# @dp.callback_query_handler(lambda c: c.data.startswith('brand_'))
# async def process_brand(callback_query: types.CallbackQuery):
#     brand = callback_query.data.split('_')[1]
#     if brand == "Ввести свою марку":
#         # Если выбран вариант "Ввести свою марку", предлагаем ввести марку
#         await bot.send_message(callback_query.from_user.id, "Напишите свою марку автомобиля и отправьте сообщение:")
#         @dp.message_handler(content_types=types.ContentTypes.TEXT)
#         async def process_car_brand(message: types.Message):
#             user_id = message.from_user.id
#             car_brand = message.text
#             user_data[user_id] = {"car_brand": car_brand}
#             dp.message_handlers.unregister(process_car_brand) #отмена слежки за процессом
#             print(user_data)
#             await bot.send_message(callback_query.from_user.id, "Введите модель авто (например Х-5, Priora и т д):")
#     # логика для else
#     # else:
#     #     # Иначе предлагаем выбрать модель из списка
#     #     models = car_models.get(brand, [])
#     #     markup = InlineKeyboardMarkup(row_width=2)
#     #     buttons = [InlineKeyboardButton(model, callback_data=f"model_{model}") for model in models]
#     #     markup.add(*buttons)
#     #     await bot.send_message(callback_query.from_user.id, "Выберите модель автомобиля:", reply_markup=markup)
#     #     print(user_data)
#
#
#
# # Обработчик нажатия кнопки с моделью автомобиля
# @dp.message_handler(lambda message: message.text)
# async def process_model(message: types.Message):
#     user_id = message.from_user.id
#     car_model = message.text
#     user_data[user_id] = {"car_model": car_model}
#     print(user_data)
#     bot.send_message(message.chat.id, 'Напишите год выпуска автомобиля:')
#
#
# @dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get("current_step") == "car_year")
# async def process_car_year(message: types.Message):
#     user_id = message.from_user.id
#     car_year = message.text
#     user_data[user_id]["car_year"] = car_year
#     # Здесь можно продолжить с другими шагами (например, тип кузова, цвет и т.д.)
#     await bot.send_message(user_id, "Введите тип кузова автомобиля:")
#     # Сохраняем текущий шаг в user_data
#     user_data[user_id]["current_step"] = "car_body_type"
#
#
#
# # car_body_type  (кузов)
# # car_engine_type (тип двигателя)
# # car_engine_volume (объём)
# # car_power (мощность)
# # car_transmission_type
# # car_color
# # car_mileage (пробег)
# # car_document_status
# # car_owners
# # car_customs_cleared (растаможка)
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)



# Версия 2.0
# import logging
# import random
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils import executor
#
# API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
# API_TOKEN2 = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# GROUP_ID = '@autoxyibot1'
#
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=API_TOKEN2)
# dp = Dispatcher(bot)
#
# user_data = {}
#
# main_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton("Мои объявления")],
#         [KeyboardButton("Разместить объявление")],
#     ],
#     resize_keyboard=True
# )
#
# # ===Названия переменных===
# # car_brand
# # car_model
# # car_year
# # car_body_type  (кузов)
# # car_engine_type (тип двигателя)
# # car_engine_volume (объём)
# # car_power (мощность)
# # car_transmission_type
# # car_color
# # car_mileage (пробег)
# # car_document_status
# # car_owners
# # car_customs_cleared (растаможка)
# # car_photo
# # car_description
# # car_price
# # car_location
# # seller_name
# # seller_phone
#
# # Список моделей автомобилей
# car_models = {
#     'Ввести свою марку': [],
# }
#
# # Обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Привет! Нажми на кнопку 'Разместить объявление', чтобы начать.", reply_markup=main_keyboard)
#
# # Обработчик кнопки "Разместить объявление"
# @dp.message_handler(lambda message: message.text == "Мои объявления")
# async def my_ads(message: types.Message):
#     ()
# @dp.message_handler(lambda message: message.text == "Разместить объявление")
# async def place_ad(message: types.Message):
#     user_id = message.from_user.id
#
#     # Запрос марки автомобиля
#     await bot.send_message(user_id, "Введите марку автомобиля (например, BMW, Toyota и т.д.):")
#
#     # Ожидание ответа от пользователя
#     car_brand_message = await bot.send_message(user_id, "Введите марку автомобиля (например, BMW, Toyota и т.д.):")
#     car_brand_response = await bot.wait_for('message', chat_id=user_id)
#
#     # Сохранение марки в user_data
#     user_data[user_id] = {"car_brand": car_brand_response.text}
#     print(user_data)
#
# # ...
#
# @dp.callback_query_handler(lambda c: c.data.startswith('brand_'))
# async def process_brand(callback_query: types.CallbackQuery):
#     # user_data[user_id] = {"car_brand": answer}
#     # user_data[user_id] = {"car_brand": car_brand}
#
#     await bot.send_message(user_id, "Введите модель авто (например, Х5, Priora и т д):")
#
# @dp.message_handler(lambda message: True)
# async def process_model(message: types.Message):
#     user_id = message.from_user.id
#
#     # Проверить, выбрана ли уже марка автомобиля в user_data
#     if user_id in user_data and "car_brand" in user_data[user_id]:
#         # Сохранить модель автомобиля в user_data
#         user_data[user_id]["car_model"] = message.text
#
#         # Продолжить следующим шагом (например, запрос года выпуска)
#         await bot.send_message(user_id, 'Напишите год выпуска автомобиля:')
#     else:
#         # Обработать случай, когда марка автомобиля еще не выбрана
#         await bot.send_message(user_id, "Сначала выберите марку автомобиля.")
#     print(user_data)
# # ...
#
# @dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get("current_step") == "car_year")
# async def process_car_year(message: types.Message):
#     user_id = message.from_user.id
#     car_year = message.text
#     user_data[user_id]["car_year"] = car_year
#     # Здесь можно продолжить с другими шагами (например, тип кузова, цвет и т.д.)
#     await bot.send_message(user_id, "Введите тип кузова автомобиля:")
#     # Сохраняем текущий шаг в user_data
#     user_data[user_id]["current_step"] = "car_body_type"
#     print(user_data)
#
#
# # car_body_type  (кузов)
# # car_engine_type (тип двигателя)
# # car_engine_volume (объём)
# # car_power (мощность)
# # car_transmission_type
# # car_color
# # car_mileage (пробег)
# # car_document_status
# # car_owners
# # car_customs_cleared (растаможка)
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto
import uuid
import asyncio
from aiogram.dispatcher.filters import Command

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
CHANNEL_ID = '@autoxyibot1'

logging.basicConfig(level=logging.INFO)

# Инициализация блокировки для предотвращения одновременной отправки нескольких запросов
lock = asyncio.Lock()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add_ad = types.KeyboardButton('Добавить объявление')
    markup.add(button_add_ad)

    greeting_message = (
        'Привет! Я бот для сбора данных. '
        'Чтобы добавить объявление, нажми на кнопку "Добавить объявление".'
    )

    await message.answer(greeting_message, reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'Добавить объявление')
async def add_ad(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    car_brands = ['BMW', 'Mercedes', 'Audi', 'Другая']  # Здесь можно добавить список других марок машин
    for brand in car_brands:
        button_brand = types.KeyboardButton(brand)
        markup.add(button_brand)

    select_brand_message = (
        'Выбери марку машины из списка или выбери "Другая", чтобы ввести марку вручную:'
    )

    await message.answer(select_brand_message, reply_markup=markup)


@dp.message_handler(lambda message: message.text in ['BMW', 'Mercedes', 'Audi'])
async def handle_brand(message: types.Message):
    user_data[message.chat.id] = {}  # Создаем пустой словарь для нового пользователя

    brand = message.text
    user_data[message.chat.id]['brand'] = brand
    await message.answer('Введите модель машины')


@dp.message_handler(lambda message: message.text == 'Другая')
async def handle_custom_brand(message: types.Message):
    user_data[message.chat.id] = {}  # Создаем пустой словарь для нового пользователя

    await message.answer('Введите марку машины вручную')
    await dp.register_next_step_handler(message, handle_manual_brand)


async def handle_manual_brand(message: types.Message):
    user_data[message.chat.id]['brand'] = message.text
    await message.answer('Введите модель машины')
    await dp.register_next_step_handler(message, handle_model)


async def handle_model(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['model'] = message.text
    await message.answer('Отправьте фотографии машины (от 1 до 10 штук)')
    await dp.register_next_step_handler(message, handle_photos)


@dp.message_handler(content_types=['photo'])
async def handle_photos(message: types.Message):
    user_id = message.from_user.id

    photo_uuid = str(uuid.uuid4())

    if user_id not in user_data:
        user_data[user_id] = {"sent_uuids": set(), "sent_photos": []}

    if photo_uuid not in user_data[user_id]["sent_uuids"]:
        user_data[user_id]["sent_uuids"].add(photo_uuid)

        photo_id = message.photo[-1].file_id
        caption = message.caption

        user_data[user_id]["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
        await message.reply(f"Фото добавлено")

        if len(user_data[user_id]["sent_photos"]) >= 1:
            await send_photos_to_channel(user_id)


async def send_photos_to_channel(user_id):
    if user_id in user_data and "sent_photos" in user_data[user_id]:
        photos = user_data[user_id]["sent_photos"]
        media_group = [
            types.InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", ""))
            for photo in photos
        ]

        # Отправляем медиагруппу в канал
        await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

        # Очищаем список после отправки всех фотографий
        user_data[user_id]["sent_photos"] = []
        user_data[user_id]["sent_uuids"].clear()  # Очищаем множество уникальных идентификаторов

        # Отправляем уведомление пользователю о успешной отправке
        await bot.send_message(user_id, "Фотографии отправлены в канал.")

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)