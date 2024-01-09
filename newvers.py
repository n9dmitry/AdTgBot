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

STATE_CAR_BRAND = 'state_car_brand'
STATE_CAR_PHOTO = 'state_car_photo'
STATE_CAR_MODEL = 'state_car_model'
STATE_CAR_YEAR = 'state_car_year'

@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    user_data = await dp.storage.get_data(user=user_id)
    await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
    await state.update_data(user_data={"user_id": user_id})
    await event.answer("Напишите бренд автомобиля:")
    await state.set_state(STATE_CAR_BRAND)

@dp.message_handler(state=STATE_CAR_BRAND)
async def get_car_brand(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_brand"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Привет! Загрузи фотографии с описанием, и я отправлю их в канал.")
    await state.set_state(STATE_CAR_PHOTO)

@dp.message_handler(state=STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await dp.storage.get_data(user=user_id)
    photo_id = message.photo[-1].file_id
    caption = message.caption

    photo_uuid = str(uuid.uuid4())

    if "sent_photos" not in user_data:
        user_data["sent_photos"] = []

    user_data["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})

    buffered_photos.append(InputMediaPhoto(media=photo_id, caption=caption))

    if len(buffered_photos) >= 1:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Перейти к следующему шагу")
        )
        await message.reply("Фото добавлено", reply_markup=keyboard)

        # Добавлено условие для перехода к следующему шагу - STATE_CAR_MODEL
        await state.set_state(STATE_CAR_MODEL)  # Переход к следующему шагу - STATE_CAR_MODEL

async def send_photos_to_channel(user_id, user_data):
    async with lock:
        if buffered_photos:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            await bot.send_message(user_id, "Фотографии отправлены в канал.")
        else:
            print("Buffered photos is empty. Nothing to send.")

@dp.message_handler(lambda message: message.text == "Перейти к следующему шагу")
async def next_step(message: types.Message):
    await bot.send_message(message.chat.id, "Перейдите к следующему шагу")

@dp.message_handler(state=STATE_CAR_MODEL)
async def get_car_brand(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_brand"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Привет!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)