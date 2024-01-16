from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from dicts import *

STATE_CAR_BRAND = 'state_car_brand'
STATE_CAR_MODEL = 'state_car_model'
STATE_CAR_YEAR = 'state_car_year'
STATE_CAR_BODY_TYPE = 'state_car_body_type'
STATE_CAR_ENGINE_TYPE = 'state_car_engine_type'
STATE_CAR_ENGINE_VOLUME = 'state_car_engine_volume'
STATE_CAR_POWER = 'state_car_power'
STATE_CAR_TRANSMISSION_TYPE = 'state_car_transmission_type'
STATE_CAR_COLOR = 'state_car_color'
STATE_CAR_MILEAGE = 'state_car_mileage'
STATE_CAR_DOCUMENT_STATUS = 'state_car_document_status'
STATE_CAR_OWNERS = 'state_car_owners'
STATE_CAR_CUSTOMS_CLEARED = 'state_car_customs_cleared'
STATE_CAR_PHOTO = 'state_car_photo'
STATE_CAR_DESCRIPTION = 'state_car_description'
STATE_CAR_PRICE = 'state_car_price'
STATE_CAR_LOCATION = 'state_car_location'
STATE_SELLER_NAME = 'state_seller_name'
STATE_SELLER_PHONE = 'state_seller_phone'
STATE_SEND = 'state_send'

class CarBotHandler:
    def __init__(self, ):
        self.lock = asyncio.Lock()
        self.buffered_photos = []

    async def start(self, event, state):
        user_id = event.from_user.id
        user_data = await state.get_data() or {}
        user_data["user_id"] = user_id
        await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")

        keyboard = InlineKeyboardMarkup(row_width=2)
        brands = list(dict_car_brands_and_models.keys())
        buttons = [InlineKeyboardButton(text=brand, callback_data=f"brand_{brand}") for brand in brands]
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(text='Ввести свою марку', callback_data='brand_custom'))

        await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state('state_car_brand')
        # Другие методы...


    async def process_brand_callback(self, query, state):
        user_data = (await state.get_data()).get("user_data", {})
        selected_brand = query.data.split('_')[1]

        if selected_brand == 'custom':
            await query.message.answer("Введите свою марку автомобиля:")
            await state.set_state('state_car_model')
        else:
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)

            # Создаем инлайн-клавиатуру с моделями выбранного бренда
            keyboard = InlineKeyboardMarkup(row_width=2)
            models = dict_car_brands_and_models[selected_brand]
            buttons = [InlineKeyboardButton(text=model, callback_data=f"model_{model}") for model in models]
            keyboard.add(*buttons)

            await query.message.answer("Выберите модель автомобиля:", reply_markup=keyboard)
            await state.set_state('state_car_model')

        await query.answer()

    async def process_model_callback(self, query, state):
        user_data = (await state.get_data()).get("user_data", {})
        selected_model = query.data.split('_')[1]
        user_data["car_model"] = selected_model
        await state.update_data(user_data=user_data)
        await query.message.answer("Отлично! Какой год выпуска у автомобиля?")
        await state.set_state('state_car_year')
        await query.answer()

    async def get_car_year(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_year"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой тип кузова у автомобиля?")
        await state.set_state(STATE_CAR_BODY_TYPE)

    async def get_car_body_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_body_type"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой тип двигателя у автомобиля?")
        await state.set_state(STATE_CAR_ENGINE_TYPE)

    async def get_car_engine_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_engine_type"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Хорошо! Какой объем двигателя у автомобиля?")
        await state.set_state(STATE_CAR_ENGINE_VOLUME)




# Использование класса
api_token = "6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M"
car_bot = CarBotHandler()
bot = Bot(token=api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    await car_bot.start(event, state)

@dp.callback_query_handler(lambda c: c.data.startswith('brand_'), state='state_car_brand')
async def process_brand_callback(query: types.CallbackQuery, state: FSMContext):
    await car_bot.process_brand_callback(query, state)

@dp.callback_query_handler(lambda c: c.data.startswith('model_'), state='state_car_model')
async def process_model_callback(query: types.CallbackQuery, state: FSMContext):
    await car_bot.process_model_callback(query, state)

@dp.message_handler(state=STATE_CAR_YEAR)
async def get_car_year(event: types.Message, state: FSMContext):
    await car_bot.get_car_year(event, state)

@dp.message_handler(state=STATE_CAR_BODY_TYPE)
async def get_car_body_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_body_type(event, state)

@dp.message_handler(state=STATE_CAR_ENGINE_TYPE)
async def get_car_engine_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_engine_type(event, state)




# старт бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)