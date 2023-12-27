import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
GROUP_ID = '@autoxyibot1'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

class Form(StatesGroup):
    car_brand = State()
    car_model = State()
    car_year = State()
    car_body_type = State()
    car_engine_type = State()
    car_engine_volume = State()
    car_power = State()
    car_transmission_type = State()
    car_color = State()
    car_mileage = State()
    car_document_status = State()
    car_owners = State()
    car_customs_cleared = State()
    car_photo = State()
    car_description = State()
    car_price = State()
    car_location = State()
    seller_name = State()
    seller_phone = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Давайте соберем информацию о вашей машине.")
    await Form.car_brand.set()

@dp.message_handler(state=Form.car_brand)
async def process_car_brand(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['car_brand'] = message.text
    await Form.car_model.set()
    await message.answer("Введите модель машины:")

# Добавьте обработчики для остальных состояний

@dp.message_handler(state=Form.car_price)
async def process_car_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['car_price'] = message.text
    await state.finish()

    # В этом месте вы можете обработать данные, например, отправить их в группу
    await message.answer("Спасибо! Вот информация, которую вы предоставили:")
    await message.answer('\n'.join([f"{key}: {value}" for key, value in data.items()]), parse_mode=ParseMode.MARKDOWN)

    # Отправить данные в группу
    await bot.send_message(chat_id=GROUP_ID, text='\n'.join([f"{key}: {value}" for key, value in data.items()]), parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
