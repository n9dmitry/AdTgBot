# import logging
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.types import InputMediaPhoto
# import uuid
# import asyncio
#
# API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
# CHANNEL_ID = '@autoxyibot1'
# bot = Bot(token=API_TOKEN)
### """ dp = Dispatcher(bot) """
# lock = asyncio.Lock()
#
# # Функция для отправки фотографий в канал
# async def send_photos_to_channel(user_id): # Функция отправляет группу фотографий в указанный канал (CHANNEL_ID)
#     async with lock: # блокировка (async with lock) для синхронизации доступа к ресурсам между потоками.
#         if user_id in dp.data and "sent_photos" in dp.data[user_id]:
#             photos = dp.data[user_id]["sent_photos"]
#             media_group = [InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", "")) for photo in photos]
#
#             # Отправляем медиагруппу в канал
#             await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
#
#             # Очищаем список после отправки всех фотографий
#             dp.data[user_id]["sent_photos"] = []
#             dp.data[user_id]["sent_uuids"].clear()  # Очищаем множество уникальных идентификаторов
#
#             # Отправляем уведомление пользователю о успешной отправке
#             await bot.send_message(user_id, "Фотографии отправлены в канал.")
#
# # Обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def handle_start(message: types.Message):
#     user_id = message.from_user.id
#
#     # Если у пользователя уже были отправлены фотографии, выводим уведомление
#     if user_id in dp.data and "sent_photos" in dp.data[user_id]:
#         await message.answer("Вы уже отправляли фотографии. Если хотите отправить новые, загрузите их снова.")
#     else:
#         await message.answer("Привет! Загрузи фотографии с описанием, и я отправлю их в канал.")
#
# # Обработчик сообщений с фотографиями
# @dp.message_handler(content_types=['photo'])
# async def handle_photos(message: types.Message):
#     user_id = message.from_user.id
#
#     # Генерируем уникальный идентификатор для фотографии
#     photo_uuid = str(uuid.uuid4())
#
#     # Проверяем, отправляали ли уже фото с таким же уникльным идентификатором
#     if user_id not in dp.data:
#         dp.data[user_id] = {"sent_uuids": set(), "sent_photos": []}
#
#     if photo_uuid not in dp.data[user_id]["sent_uuids"]:
#         dp.data[user_id]["sent_uuids"].add(photo_uuid)
#
#         # отправка
#         # Получаем идентификатор фотографии и описание
#         photo_id = message.photo[-1].file_id
#         caption = message.caption
#
#         # Добавляем информацию о фотографии в список для отправки в канал
#         dp.data[user_id]["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
#         await message.reply(f"Фото добавлено")
#
#         # Если у пользователя есть хотя бы одна фотография, отправляем их в канал
#         if len(dp.data[user_id]["sent_photos"]) >= 1:
#             photo_count = 0
#             for i in range(len(dp.data[user_id]['sent_photos'])):
#                 photo_count += 1
#                 # print(f"Получаем фото от пользователя {user_id} {photo_count} из {len(dp.data[user_id]['sent_photos'])} штук")
#
#             # Проверяем, что не отправляли уже фотографии при обработке команды /start
#             if "sent_photos" in dp.data[user_id]:
#                 # print(f"Отправляем фото ботом в массив для передачи в канал.")
#                 await send_photos_to_channel(user_id)
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)


# Вариант с юзер датой

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
import uuid
import asyncio

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
CHANNEL_ID = '@autoxyibot1'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
lock = asyncio.Lock()

# Функция для отправки фотографий в канал
async def send_photos_to_channel(user_id, user_data):
    async with lock:
        if "sent_photos" in user_data:
            photos = user_data["sent_photos"]
            media_group = [InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", "")) for photo in photos]

            # Отправляем медиагруппу в канал
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

            # Очищаем список после отправки всех фотографий
            user_data["sent_photos"] = []
            user_data["sent_uuids"].clear()

            # Отправляем уведомление пользователю о успешной отправке
            await bot.send_message(user_id, "Фотографии отправлены в канал.")

# Обработчик команды /start
import logging
from aiogram import Bot, types
from aiogram.types import InputMediaPhoto
import uuid
import asyncio

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
CHANNEL_ID = '@autoxyibot1'
bot = Bot(token=API_TOKEN)
lock = asyncio.Lock()

# Функция для отправки фотографий в канал
async def send_photos_to_channel(user_id, user_data):
    async with lock:
        if "sent_photos" in user_data:
            photos = user_data["sent_photos"]
            media_group = [InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", "")) for photo in photos]

            # Отправляем медиагруппу в канал
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

            # Очищаем список после отправки всех фотографий
            user_data["sent_photos"] = []
            user_data["sent_uuids"].clear()

            # Отправляем уведомление пользователю о успешной отправке
            await bot.send_message(user_id, "Фотографии отправлены в канал.")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    user_data = await bot.get_storage().get_data(user_id)

    if "sent_photos" in user_data:
        await message.answer("Вы уже отправляли фотографии. Если хотите отправить новые, загрузите их снова.")
    else:
        await message.answer("Привет! Загрузи фотографии с описанием, и я отправлю их в канал.")

# Обработчик сообщений с фотографиями
@bot.message_handler(content_types=['photo'])
async def handle_photos(message: types.Message):
    user_id = message.from_user.id
    user_data = await bot.get_storage().get_data(user_id)

    photo_uuid = str(uuid.uuid4())

    if "sent_uuids" not in user_data:
        user_data["sent_uuids"] = set()
        user_data["sent_photos"] = []

    if photo_uuid not in user_data["sent_uuids"]:
        user_data["sent_uuids"].add(photo_uuid)

        photo_id = message.photo[-1].file_id
        caption = message.caption

        user_data["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
        await message.reply(f"Фото добавлено")

        if len(user_data["sent_photos"]) >= 1:
            await send_photos_to_channel(user_id, user_data)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(bot, skip_updates=True)

