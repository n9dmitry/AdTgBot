from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio

API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
CHANNEL_ID = '@autoxyibot1'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
lock = asyncio.Lock()

buffered_photos = []  # Глобальная переменная для буфера фотографий

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
STATE_SEND = 'state_send'

@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    user_data = await state.get_data() or {}
    await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
    user_data["user_id"] = user_id
    await state.set_data(user_data)
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
    await state.set_state(STATE_CAR_BODY_TYPE)

@dp.message_handler(state=STATE_CAR_BODY_TYPE)
async def get_car_body_type(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_body_type"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой тип двигателя у автомобиля?")
    await state.set_state(STATE_CAR_ENGINE_TYPE)

@dp.message_handler(state=STATE_CAR_ENGINE_TYPE)
async def get_car_engine_type(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_engine_type"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Хорошо! Какой объем двигателя у автомобиля?")
    await state.set_state(STATE_CAR_ENGINE_VOLUME)

@dp.message_handler(state=STATE_CAR_ENGINE_VOLUME)
async def get_car_engine_volume(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_engine_volume"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Укажите мощность двигателя автомобиля.")
    await state.set_state(STATE_CAR_POWER)

@dp.message_handler(state=STATE_CAR_POWER)
async def get_car_power(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_power"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой тип коробки передач используется в автомобиле?")
    await state.set_state(STATE_CAR_TRANSMISSION_TYPE)

@dp.message_handler(state=STATE_CAR_TRANSMISSION_TYPE)
async def get_car_transmission_type(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_transmission_type"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Какого цвета автомобиль?")
    await state.set_state(STATE_CAR_COLOR)

@dp.message_handler(state=STATE_CAR_COLOR)
async def get_car_color(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_color"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Каков пробег автомобиля?")
    await state.set_state(STATE_CAR_MILEAGE)

@dp.message_handler(state=STATE_CAR_MILEAGE)
async def get_car_mileage(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_mileage"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Каков статус документов у автомобиля?")
    await state.set_state(STATE_CAR_DOCUMENT_STATUS)

@dp.message_handler(state=STATE_CAR_DOCUMENT_STATUS)
async def get_car_document_status(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_document_status"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Сколько владельцев у автомобиля?")
    await state.set_state(STATE_CAR_OWNERS)

@dp.message_handler(state=STATE_CAR_OWNERS)
async def get_car_owners(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_owners"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Растаможен ли автомобиль?")
    await state.set_state(STATE_CAR_CUSTOMS_CLEARED)

@dp.message_handler(state=STATE_CAR_CUSTOMS_CLEARED)
async def get_car_customs_cleared(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_customs_cleared"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Добавьте фотографии автомобиля.")
    await state.set_state(STATE_CAR_PHOTO)


@dp.message_handler(state=STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data() or {}
    photo_id = message.photo[-1].file_id
    caption = str(user_data)

    photo_uuid = str(uuid.uuid4())

    if "sent_photos" not in user_data:
        user_data["sent_photos"] = []

    user_data["sent_photos"].append({"file_id": photo_id, "uuid": photo_uuid})

    buffered_photos.append(InputMediaPhoto(media=photo_id, caption=caption))
    if len(buffered_photos) > 1:
        for i in range(len(buffered_photos) - 1):
            buffered_photos[i].caption = None
        last_photo = buffered_photos[-1]
        last_photo.caption = caption

    await message.reply("Фото добавлено")
    await state.finish()
    await state.set_state(STATE_CAR_DESCRIPTION)


@dp.message_handler(state=STATE_CAR_DESCRIPTION)
async def get_car_description(event: types.Message, state: FSMContext):
    user_data = await state.get_data() or {}
    user_data["car_description"] = event.text
    await state.update_data(user_data=user_data)  # Обновление данных состояния
    await event.answer("Какова цена автомобиля?")
    await state.set_state(STATE_CAR_PRICE)


@dp.message_handler(state=STATE_CAR_PRICE)
async def get_car_price(event: types.Message, state: FSMContext):
    user_data = await state.get_data() or {}
    user_data["car_price"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Прекрасно! Где находится автомобиль?")
    await state.set_state(STATE_CAR_LOCATION)


@dp.message_handler(state=STATE_CAR_LOCATION)
async def get_car_location(event: types.Message, state: FSMContext):
    user_data = await state.get_data() or {}
    user_data["car_location"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Прекрасно! Укажите имя продавца.")
    await state.set_state(STATE_SELLER_NAME)


@dp.message_handler(state=STATE_SELLER_NAME)
async def get_seller_name(event: types.Message, state: FSMContext):
    user_data = await state.get_data() or {}
    user_data["seller_name"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой телефонный номер у продавца?")
    await state.set_state(STATE_SELLER_PHONE)


@dp.message_handler(state=STATE_SELLER_PHONE)
async def get_seller_phone(event: types.Message, state: FSMContext):
    user_data = await state.get_data() or {}
    user_data["seller_phone"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Сейчас запостим фото!")
    await state.finish()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Отправить объявление")
    )
    await event.answer("Фотографии отправлены в канал.", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Отправить объявление")
async def send_advertisement(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    await send_photos_to_channel(user_id, user_data)  # Вместо (user_data, user_id)
    await message.answer("Объявление отправлено в канал.")


async def send_photos_to_channel(user_id, user_data):
    async with lock:
        if buffered_photos:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            await bot.send_message(user_id, "Фотографии отправлены в канал.")
            buffered_photos.clear()
        else:
            print("Buffered photos is empty. Nothing to send.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)