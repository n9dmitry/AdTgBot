import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
API_TOKEN2 = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
GROUP_ID = '@autoxyibot1'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN2)
dp = Dispatcher(bot)

user_data = {}
# Пример работы с user_data
# async def handle_location(message: types.Message):
#     location = message.text
#     user_data[message.chat.id]['location'] = location

# Клавиатура с быстрыми ссылками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Разместить объявление")],
    ],
    resize_keyboard=True
)

# ===Названия переменных===
# car_brand
# car_model
# car_year
# car_body_type  (кузов)
# car_engine_type (тип двигателя)
# car_engine_volume (объём)
# car_power (мощность)
# car_transmission_type
# car_color
# car_mileage (пробег)
# car_document_status
# car_owners
# car_customs_cleared (растаможка)
# car_photo
# car_description
# car_price
# car_location
# seller_name
# seller_phone

# Список моделей автомобилей
car_models = {
    'Другая': ['Ввести модель'],
    'Audi': ['Ввести марку', 'A3', 'A4', 'Q5', 'Q7'],
    'BMW': ['Ввести марку', '3 Series', '5 Series', 'X3', 'X5'],
    'Mercedes-Benz': ['Ввести марку', 'C-Class', 'E-Class', 'GLC', 'GLE'],
    'Chevrolet': ['Ввести марку', 'Cruze', 'Malibu', 'Equinox', 'Tahoe'],
    'Ford': ['Ввести марку', 'Focus', 'Fusion', 'Escape', 'Explorer'],
    'Honda': ['Ввести марку', 'Civic', 'Accord', 'CR-V', 'Pilot'],
    'Hyundai': ['Ввести марку', 'Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Ввести марку', 'Optima', 'Sorento', 'Sportage', 'Telluride'],
    'Nissan': ['Ввести марку', 'Altima', 'Maxima', 'Rogue', 'Pathfinder'],
    'Toyota': ['Ввести марку', 'Camry', 'Corolla', 'Rav4', 'Highlander'],
    'Volkswagen': ['Ввести марку', 'Golf', 'Jetta', 'Tiguan', 'Atlas'],
    'Volvo': ['Ввести марку', 'S60', 'S90', 'XC60', 'XC90'],
    'Ferrari': ['Ввести марку', '488', 'F8 Tributo', 'Portofino', 'SF90 Stradale'],
    'Porsche': ['Ввести марку', '911', 'Cayenne', 'Panamera', 'Macan'],
    'Tesla': ['Ввести марку', 'Model S', 'Model 3', 'Model X', 'Model Y'],
    'Lamborghini': ['Ввести марку', 'Huracan', 'Aventador', 'Urus'],
    'Jaguar': ['Ввести марку', 'XE', 'XF', 'F-Pace', 'I-Pace'],
    'Land Rover': ['Ввести марку', 'Discovery', 'Range Rover Evoque', 'Range Rover Sport', 'Defender'],
    'Mazda': ['Ввести марку', 'Mazda3', 'Mazda6', 'CX-5', 'CX-9'],
    'Subaru': ['Ввести марку', 'Impreza', 'Outback', 'Forester', 'Ascent'],
    'LADA': ['Ввести марку', 'Vesta', 'Granta', 'XRAY', '4x4'],
    'УАЗ': ['Ввести марку', 'Patriot', 'Hunter', 'Bukhanka'],
    'ГАЗ': ['Ввести марку', 'Sobol', 'Next', 'Gazelle'],
    'КАМАЗ': ['Ввести марку', '5490', '6520', '43118'],
    'АвтоВАЗ': ['Ввести марку', 'LADA 4x4', 'LADA Kalina', 'LADA Priora', 'LADA XRAY']
}
    # Добавьте другие бренды

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Нажми на кнопку 'Разместить объявление', чтобы начать.", reply_markup=main_keyboard)

# Обработчик кнопки "Разместить объявление"
@dp.message_handler(lambda message: message.text == "Разместить объявление")
async def place_ad(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    brands = list(car_models.keys())
    buttons = [InlineKeyboardButton(brand, callback_data=f"brand_{brand}") for brand in brands]
    markup.add(*buttons)

    await message.answer("Введите марку автомобиля или выберите из списка:", reply_markup=markup)

# Обработчик нажатия кнопки с маркой автомобиля
@dp.callback_query_handler(lambda c: c.data.startswith('brand_'))
async def process_brand(callback_query: types.CallbackQuery):
    brand = callback_query.data.split('_')[1]
    if brand == "Ввести свою марку":
        # Если выбран вариант "Ввести свою марку", предлагаем ввести марку
        await bot.send_message(callback_query.from_user.id, "Введите свою марку автомобиля:")
    else:
        # Иначе предлагаем выбрать модель из списка
        models = car_models.get(brand, [])
        markup = InlineKeyboardMarkup(row_width=2)
        buttons = [InlineKeyboardButton(model, callback_data=f"model_{model}") for model in models]
        markup.add(*buttons)
        await bot.send_message(callback_query.from_user.id, "Выберите модель автомобиля:", reply_markup=markup)


# Обработчик нажатия кнопки с моделью автомобиля
@dp.callback_query_handler(lambda c: c.data.startswith('model_'))
async def process_model(callback_query: types.CallbackQuery):
    model = callback_query.data.split('_')[1]
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали модель {model}. Теперь можно ввести другую информацию.")





if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
