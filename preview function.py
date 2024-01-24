from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from config import *
from states import *
from validation import *
import json

# Загрузка JSON в начале скрипта
with open('dicts.json', 'r', encoding='utf-8') as file:
    dicts = json.load(file)

dict_car_brands_and_models = dicts.get("dict_car_brands_and_models", {})
dict_car_body_types = dicts.get("dict_car_body_types", {})
dict_car_engine_types = dicts.get("dict_car_engine_types", {})
dict_car_transmission_types = dicts.get("dict_car_transmission_types", {})
dict_car_colors = dicts.get("dict_car_colors", {})
dict_car_document_statuses = dicts.get("dict_car_document_statuses", {})
dict_car_owners = dicts.get("dict_car_owners", {})
dict_car_customs_cleared = dicts.get("dict_car_customs_cleared", {})
dict_currency = dicts.get("dict_currency", {})
dict_car_conditions = dicts.get("dict_car_conditions", {})
dict_car_mileages = dicts.get("dict_car_mileages", {})
# Конец импорта json словарей


# Создание клавиатуры
def create_keyboard(button_texts, resize_keyboard=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=2)
    buttons = [KeyboardButton(text=text) for text in button_texts]
    keyboard.add(*buttons)
    return keyboard

class CarBotHandler:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.sent_message = None

# Удаление предыдущих ответов
    async def delete_previous_question(self, event):
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id - 1)

    async def delete_hello(self, event):
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id - 2)

# Начало работы бота

    async def start(self, event, state):
        await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state(STATE_CAR_BRAND)

    async def get_car_brand(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        selected_brand = event.text
        valid_brands = dict_car_brands_and_models
        if await validate_car_brand(selected_brand, valid_brands):
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await self.delete_hello(event)
            # Создаем клавиатуру
            keyboard = create_keyboard(dict_car_brands_and_models[selected_brand])
            await event.answer("Отлично! Выберите модель автомобиля:", reply_markup=keyboard)
            await state.set_state(STATE_CAR_MODEL)
        else:
            await self.delete_previous_question(event)
            await self.delete_hello(event)
            keyboard = create_keyboard(dict_car_brands_and_models.keys())
            await bot.send_message(event.from_user.id, "Пожалуйста, выберите бренд из предложенных вариантов или напишите нам если вашего бренда нет", reply_markup=keyboard)
            await state.set_state(STATE_CAR_BRAND)

car_bot = CarBotHandler()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
lock = asyncio.Lock()
buffered_photos = []

@dp.message_handler(commands=["start"])
async def cmd_start(event: types.Message, state: FSMContext):
    await car_bot.start(event, state)

@dp.message_handler(state=STATE_CAR_BRAND)
async def process_brand_selection(event: types.Message, state: FSMContext):
    await car_bot.get_car_brand(event, state)