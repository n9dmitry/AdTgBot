from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from dicts import dict_car_brands_and_models

class Car_Post:
    def __init__(self, api_token):
        self.api_token = api_token
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.lock = asyncio.Lock()
        self.buffered_photos = []

    @staticmethod
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

    async def process_brand_callback(query: types.CallbackQuery, state: FSMContext):
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

# Использование класса
API_TOKEN = "6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M"
car_post = Car_Post(API_TOKEN, dp=car_post.dp)

@car_post.dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    await car_post.start(event, state)

@car_post.dp.callback_query_handler(lambda c: c.data.startswith('brand_'), state='state_car_brand')
async def process_brand_callback(query: types.CallbackQuery, state: FSMContext):
    await car_post.process_brand_callback(query, state)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)