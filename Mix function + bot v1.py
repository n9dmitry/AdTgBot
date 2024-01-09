from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio

# API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
# API_TOKEN2 = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# API_fttlolbot = '6986960778:AAGzuNdkvAfgrr5Gc2oVHfEwrWYY7NvRqJE'
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


# ========================

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import uuid
import asyncio


# API_TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'
# API_TOKEN2 = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# API_fttlolbot = '6986960778:AAGzuNdkvAfgrr5Gc2oVHfEwrWYY7NvRqJE'
API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
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
    # Используем уникальный идентификатор для фотографии
    photo_uuid = str(uuid.uuid4())
    # if "sent_photos" not in user_data:
    user_data["sent_photos"] = []

    user_data["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
    print("user_data:", user_data)  # Добавленный принт
    # Добавим фотографию в буфер
    buffered_photos.append(InputMediaPhoto(media=photo_id, caption=caption))
    print("buffered_photos:", buffered_photos)
    # Проверим, загружены ли все фотографии
    if len(buffered_photos) >= 1:  # Укажите здесь желаемое количество фотографий в альбоме
        # Добавим кнопку "Подтвердить фото" в самый низ клавиатуры
        confirm_button = InlineKeyboardButton("Закончить добавление фотографий", callback_data='confirm_photo')
        keyboard = InlineKeyboardMarkup().add(confirm_button)
        # Отправим клавиатуру с кнопкой вместе с сообщением
        await message.reply("Фото добавлено", reply_markup=keyboard)
        await state.finish()



@dp.callback_query_handler(lambda c: c.data == 'confirm_photo')
async def confirm_photo(callback_query: types.CallbackQuery):
    # Обработка нажатия кнопки "Подтвердить фото"
    await bot.answer_callback_query(callback_query.id, text="Фото подтверждено")

    user_id = callback_query.from_user.id
    user_data = await dp.storage.get_data(user=user_id)

    # Вызываем функцию отправки фотографий вместе с user_data
    await send_photos_to_channel(user_id, user_data)

async def send_photos_to_channel(user_id, user_data):
    async with lock:
        # global buffered_photos

        if buffered_photos:
            print("Sending media group:", buffered_photos)  # Добавим этот принт
            # Отправляем медиагруппу в канал
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            # Очищаем буфер после отправки всех фотографий
            # buffered_photos.clear()
            # Очищаем список после отправки всех фотографий
            # user_data["sent_photos"].clear()
            # Проверяем наличие ключа 'sent_uuids' перед его очисткой
            # if "sent_uuids" in user_data:
            #     user_data["sent_uuids"].clear()
            # Отправляем уведомление пользователю о успешной отправке
            await bot.send_message(user_id, "Фотографии отправлены в канал.")
        else:
            print("Buffered photos is empty. Nothing to send.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
# import uuid
# import asyncio
#
# API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# CHANNEL_ID = '@autoxyibot1'
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# lock = asyncio.Lock()
#
# buffered_photos = []  # Глобальная переменная для буфера фотографий
#
# async def send_photos_to_channel(user_id, user_data):
#     async with lock:
#         global buffered_photos
#
#         if buffered_photos:
#             print("Sending media group:", buffered_photos)  # Добавим этот принт
#
#             # Отправляем медиагруппу в канал
#             await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
#
#             # Очищаем буфер после отправки всех фотографий
#             buffered_photos.clear()
#
#             # Очищаем список после отправки всех фотографий
#             user_data["sent_photos"].clear()
#
#             # Проверяем наличие ключа 'sent_uuids' перед его очисткой
#             if "sent_uuids" in user_data:
#                 user_data["sent_uuids"].clear()
#
#             # Отправляем уведомление пользователю о успешной отправке
#             await bot.send_message(user_id, "Фотографии отправлены в канал.")
#         else:
#             print("Buffered photos is empty. Nothing to send.")
#
# @dp.message_handler(commands=['start'])
# async def handle_start(message: types.Message):
#     user_id = message.from_user.id
#     user_data = await dp.storage.get_data(user=user_id)
#
#     if "sent_photos" in user_data:
#         await message.answer("Вы уже отправляли фотографии. Если хотите отправить новые, загрузите их снова.")
#     else:
#         # Инициализируем user_data, если его нет
#         user_data = {"sent_photos": []}
#         await dp.storage.set_data(user=user_id, data=user_data)  # Сохраняем user_data
#         await message.answer("Привет! Загрузи фотографии с описанием, и я отправлю их в канал.")
#
# @dp.message_handler(content_types=['photo'])
# async def handle_photos(message: types.Message):
#     user_id = message.from_user.id
#     user_data = await dp.storage.get_data(user=user_id)
#
#     photo_id = message.photo[-1].file_id
#     caption = message.caption
#
#     # Используем уникальный идентификатор для фотографии
#     photo_uuid = str(uuid.uuid4())
#
#     if "sent_photos" not in user_data:
#         user_data["sent_photos"] = []
#
#     user_data["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
#
#     print("user_data:", user_data)  # Добавленный принт
#
#     # Добавим фотографию в буфер
#     buffered_photos.append(InputMediaPhoto(media=photo_id, caption=caption))
#
#     # Проверим, загружены ли все фотографии
#     if len(buffered_photos) >= 1:  # Укажите здесь желаемое количество фотографий в альбоме
#         # Добавим кнопку "Подтвердить фото" в самый низ клавиатуры
#         confirm_button = InlineKeyboardButton("Закончить добавление фотографий", callback_data='confirm_photo')
#         keyboard = InlineKeyboardMarkup().add(confirm_button)
#
#         # Отправим клавиатуру с кнопкой вместе с сообщением
#         await message.reply("Фото добавлено", reply_markup=keyboard)
#
# @dp.callback_query_handler(lambda c: c.data == 'confirm_photo')
# async def confirm_photo(callback_query: types.CallbackQuery):
#     # Обработка нажатия кнопки "Подтвердить фото"
#     await bot.answer_callback_query(callback_query.id, text="Фото подтверждено")
#
#     user_id = callback_query.from_user.id
#     user_data = await dp.storage.get_data(user=user_id)
#
#     # Вызываем функцию отправки фотографий вместе с user_data
#     await send_photos_to_channel(user_id, user_data)
#
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)
