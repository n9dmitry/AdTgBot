from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *
import json
#
#
# # Загрузка JSON в начале скрипта
# with open('dicts.json', 'r', encoding='utf-8') as file:
#     dicts = json.load(file)
#
# dict_start_brands = dicts.get("dict_start_brands", {})
# dict_car_brands_and_models = dicts.get("dict_car_brands_and_models", {})
# dict_car_body_types = dicts.get("dict_car_body_types", {})
# dict_car_engine_types = dicts.get("dict_car_engine_types", {})
# dict_car_transmission_types = dicts.get("dict_car_transmission_types", {})
# dict_car_colors = dicts.get("dict_car_colors", {})
# dict_car_document_statuses = dicts.get("dict_car_document_statuses", {})
# dict_car_owners = dicts.get("dict_car_owners", {})
# dict_car_customs_cleared = dicts.get("dict_car_customs_cleared", {})
# dict_currency = dicts.get("dict_currency", {})
# dict_car_conditions = dicts.get("dict_car_conditions", {})
# dict_car_mileages = dicts.get("dict_car_mileages", {})
# dict_edit_buttons = dicts.get("dict_edit_buttons", {})
# # Конец импорта json словарей

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Auto", callback_data="auto"),
        InlineKeyboardButton("Estate", callback_data="estate"),
        InlineKeyboardButton("HR", callback_data="hr")
    )
    await message.answer("Welcome! Выбери категорию:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ['auto', 'estate', 'hr'])
async def process_callback(callback_query: types.CallbackQuery):
    category = callback_query.data
    await callback_query.answer()
    if category == 'auto':
        await callback_query.message.answer("You have selected the 'Auto' category.")
        # Перенаправляем пользователя на сценарий sc1.py
        process_scenario_1(callback_query.message)
    elif category == 'estate':
        await callback_query.message.answer("You have selected the 'Estate' category.")
        # Перенаправляем пользователя на сценарий sc2.py
        process_scenario_2(callback_query.message)
    elif category == 'hr':
        await callback_query.message.answer("You have selected the 'HR' category.")
        # Перенаправляем пользователя на сценарий sc3.py
        process_scenario_3(callback_query.message)

async def process_scenario_1(message: types.Message):
    await message.answer("х1")

async def process_scenario_2(message: types.Message):
    await message.answer("х2")

async def process_scenario_3(message: types.Message):
    await message.answer("х3")

# старт бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)