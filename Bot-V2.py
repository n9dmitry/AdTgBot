from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
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


# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
    await state.update_data(user_data={"user_id": user_id})
    await event.answer("Напишите бренд автомобиля:")
    await state.set_state(STATE_CAR_BRAND)


@dp.message_handler(state=STATE_CAR_BRAND)
async def get_car_brand(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_brand"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Хорошо! Укажите модель автомобиля:")
    await state.set_state(STATE_CAR_MODEL)


@dp.message_handler(state=STATE_CAR_MODEL)
async def get_car_model(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_model"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой год выпуска у автомобиля?:")
    await state.set_state(STATE_CAR_YEAR)


@dp.message_handler(state=STATE_CAR_YEAR)
async def get_car_year(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_year"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой тип кузова у автомобиля?")

    # Вместо state.finish() используем state.reset_state()
    await state.reset_state(with_data=False)

    final_data = await state.get_data()
    user_data = final_data.get("user_data", {})
    print("Final Data:", final_data)
    print("User Data:", user_data)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
