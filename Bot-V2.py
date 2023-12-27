from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
CHANNEL_ID = '@autoxyibot1'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Состояния пользователя
STATE_CAR_BRAND = 'state_car_brand'
STATE_CAR_MODEL = 'state_car_model'
STATE_CAR_YEAR = 'state_car_year'


# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")

    # Инициализируем user_data в FSMContext
    await state.update_data(user_data={"user_id": user_id})

    # Задаем первый вопрос
    await event.answer("Напишите бренд автомобиля.:")

    # Устанавливаем состояние пользователя в STATE_CAR_BRAND
    await state.set_state(STATE_CAR_BRAND)


@dp.message_handler(state=STATE_CAR_BRAND)
async def get_car_brand(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    car_brand = event.text

    # Получаем текущие данные из FSMContext
    data = await state.get_data()
    user_data = data.get("user_data", {})

    # Добавляем новые данные
    user_data["car_brand"] = car_brand

    # Обновляем данные в FSMContext
    await state.update_data(user_data=user_data)

    # Дополнительная логика обработки ответа, если необходимо
    # Например, задать следующий вопрос или выполнить другие действия

    # Задаем второй вопрос
    await event.answer("Хорошо! Укажите модель автомобиля:")

    # Устанавливаем состояние пользователя в STATE_CAR_MODEL
    await state.set_state(STATE_CAR_MODEL)


@dp.message_handler(state=STATE_CAR_MODEL)
async def get_car_model(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    car_model = event.text

    # Получаем текущие данные из FSMContext
    data = await state.get_data()
    user_data = data.get("user_data", {})

    # Добавляем новые данные
    user_data["car_model"] = car_model

    # Обновляем данные в FSMContext
    await state.update_data(user_data=user_data)

    # Дополнительная логика обработки ответа, если необходимо
    # Например, задать третий вопрос или выполнить другие действия

    # Задаем третий вопрос
    await event.answer("Отлично! Какой год выпуска у автомобиля?:")

    # Устанавливаем состояние пользователя в STATE_CAR_YEAR
    await state.set_state(STATE_CAR_YEAR)


@dp.message_handler(state=STATE_CAR_YEAR)
async def get_car_year(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    car_year = event.text

    # Получаем текущие данные из FSMContext
    data = await state.get_data()
    user_data = data.get("user_data", {})

    # Добавляем новые данные
    user_data["car_year"] = car_year

    # Обновляем данные в FSMContext
    await state.update_data(user_data=user_data)

    # Дополнительная логика обработки ответа, если необходимо
    # Например, завершить сбор данных или выполнить другие действия

    # Выводим завершающее сообщение
    await event.answer("Отлично! Какой тип кузова у автомобиля?")

    # Сбрасываем состояние пользователя
    await state.finish()

    # Получаем окончательные данные из FSMContext
    final_data = await state.get_data()
    user_data = final_data.get("user_data", {})

    print(final_data)

if __name__ == '__main__':
    from aiogram import executor

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
