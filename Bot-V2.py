from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
CHANNEL_ID = '@autoxyibot1'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния пользователя
STATE_CAR_BRAND = 'state_car_brand'
STATE_CAR_MODEL = 'state_car_model'
STATE_CAR_YEAR = 'state_car_year'

# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(f"Привет, {message.from_user.first_name}! Я бот для сбора данных. Давай начнем.")

    # Задаем первый вопрос
    await message.answer("Напишите бренд автомобиля.:")

    # Устанавливаем состояние пользователя в STATE_CAR_BRAND
    await state.set_state(STATE_CAR_BRAND)

@dp.message_handler(state=STATE_CAR_BRAND)
async def get_car_brand(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    car_brand = message.text

    user_data = {"user_id": user_id, "car_brand": car_brand}

    # Дополнительная логика обработки ответа, если необходимо
    # Например, задать следующий вопрос или выполнить другие действия

    # Задаем второй вопрос
    await message.answer("Хорошо! Укажите модель автомобиля:")

    # Устанавливаем состояние пользователя в STATE_CAR_MODEL
    await state.set_state(STATE_CAR_MODEL)

@dp.message_handler(state=STATE_CAR_MODEL)
async def get_car_model(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    car_model = message.text

    user_data = {"user_id": user_id, "car_model": car_model}

    # Дополнительная логика обработки ответа, если необходимо
    # Например, задать третий вопрос или выполнить другие действия

    # Задаем третий вопрос
    await message.answer("Отлично! Какой год выпуска у автомобиля?:")

    # Устанавливаем состояние пользователя в STATE_CAR_YEAR
    await state.set_state(STATE_CAR_YEAR)

@dp.message_handler(state=STATE_CAR_YEAR)
async def get_car_year(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    car_year = message.text

    user_data = {"user_id": user_id, "car_year": car_year}

    # Дополнительная логика обработки ответа, если необходимо
    # Например, завершить сбор данных или выполнить другие действия

    # Выводим завершающее сообщение
    await message.answer("Отлично! Какой тип кузова у автомобиля?")

    # Сбрасываем состояние пользователя
    await state.finish()

    print(user_data)

if __name__ == '__main__':
    from aiogram import executor

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)