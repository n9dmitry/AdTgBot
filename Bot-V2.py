import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputMediaPhoto
from aiogram.types import InputMediaPhoto, PhotoSize
import asyncio


lock = asyncio.Lock()

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
STATE_CAR_PHOTOS = 'state_car_photos'
STATE_CAR_DESCRIPTION = 'state_car_description'
STATE_CAR_PRICE = 'state_car_price'
STATE_CAR_LOCATION = 'state_car_location'
STATE_SELLER_NAME = 'state_seller_name'
STATE_SELLER_PHONE = 'state_seller_phone'
STATE_SEND = 'state_send'

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
    await state.set_state(STATE_CAR_PHOTOS)

@dp.message_handler(state=STATE_CAR_PHOTOS, content_types=['photo'])
async def get_car_photos(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    if "car_photos" not in user_data:
        user_data["car_photos"] = []
    # Ваш код обработки фотографий, если необходим
    user_id = event.from_user.id
    photo_uuid = str(uuid.uuid4())
    # Проверяем, отправляали ли уже фото с таким же уникльным идентификатором
    if user_id not in dp.data:
        dp.data[user_id] = {"sent_uuids": set(), "sent_photos": []}
    if photo_uuid not in dp.data[user_id]["sent_uuids"]:
        dp.data[user_id]["sent_uuids"].add(photo_uuid)

        # Получаем идентификатор фотографии и описание
        photo_id = event.photo[-1].file_id
        width = event.photo[-1].width
        caption = event.caption

        unique_photos = [photo for photo in user_data["car_photos"] if photo.file_id != photo_id or photo.width < width]
        user_data["car_photos"] = unique_photos
        user_data["car_photos"].append(event.photo[-1])
        dp.data[user_id]["sent_photos"].append({"file_id": photo_id, "caption": caption, "uuid": photo_uuid})
    # user_data["car_photos"] = event.photo  # Здесь можно сохранить ссылку на фотографии или другую информацию о них
    await state.update_data(user_data=user_data)
    await event.answer("Предоставьте описание автомобиля.")
    await state.set_state(STATE_CAR_DESCRIPTION)

@dp.message_handler(state=STATE_CAR_DESCRIPTION)
async def get_car_description(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_description"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Какова цена автомобиля?")
    await state.set_state(STATE_CAR_PRICE)

@dp.message_handler(state=STATE_CAR_PRICE)
async def get_car_price(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_price"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Прекрасно! Где находится автомобиль?")
    await state.set_state(STATE_CAR_LOCATION)

@dp.message_handler(state=STATE_CAR_LOCATION)
async def get_car_location(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["car_location"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Прекрасно! Укажите имя продавца.")
    await state.set_state(STATE_SELLER_NAME)

@dp.message_handler(state=STATE_SELLER_NAME)
async def get_seller_name(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["seller_name"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Какой телефонный номер у продавца?")
    await state.set_state(STATE_SELLER_PHONE)

@dp.message_handler(state=STATE_SELLER_PHONE)
async def get_seller_phone(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    user_data["seller_phone"] = event.text
    await state.update_data(user_data=user_data)
    await event.answer("Отлично! Сейчас запостим фото!")
    await state.set_state(STATE_SEND)

@dp.message_handler(state=STATE_SEND)
async def send_photos_to_channel(user_id): # Функция отправляет группу фотографий в указанный канал (CHANNEL_ID)
    if user_id in dp.data and "sent_photos" in dp.data[user_id]:
        photos = dp.data[user_id]["sent_photos"]
        media_group = [InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", "")) for photo in photos]

        # Отправляем медиагруппу в канал
        await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group, caption=str(dp.data[user_id]))

        # Очищаем список после отправки всех фотографий
        dp.data[user_id]["sent_photos"] = []
        dp.data[user_id]["sent_uuids"].clear()  # Очищаем множество уникальных идентификаторов

        # Отправляем уведомление пользователю о успешной отправке
        await bot.send_message(user_id, "Фотографии отправлены в канал.")
        await send_photos_to_channel(user_id)


# Попытка 1
    # # Финальный шаг - собрать все данные и завершить состояние
    # final_data = await state.get_data()
    # user_data = final_data.get("user_data", {})
    #
    # # Формируем сообщение с данными пользователя
    # message = "Получена новая заявка:\n"
    # for key, value in user_data.items():
    #     message += f"{key.capitalize()}: {value}\n"
    # print(final_data)
    # # Отправляем сообщение в канал
    # await bot.send_message(CHANNEL_ID, message)
    # await state.reset_state()

# Попытка 2
#     media_group = []
#
#     for photo in photos:
#         if isinstance(photo, Photo):
#             # Если это объект Photo, используйте атрибуты
#             media_group.append(InputMediaPhoto(media=photo.file_id, caption=photo.caption))
#         elif isinstance(photo, PhotoSize):
#             # Если это объект PhotoSize, используйте другие атрибуты, например, file_id
#             media_group.append(InputMediaPhoto(media=photo.file_id, caption=""))
#
#     # Отправляем медиагруппу в канал
#     await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
#     photos = user_data["car_photos"]
#     # media_group = [InputMediaPhoto(media=photo["file_id"], caption=photo.get("caption", "")) for photo in photos]
#     media_group = [InputMediaPhoto(media=photo.file_id, caption=photo.caption) for photo in photos if isinstance(photo, PhotoSize)]
#
#
#     # Отправляем медиагруппу в канал
#     await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group, caption=user_data)
#
#
#     # Отправляем уведомление пользователю о успешной отправке
#     await bot.send_message(event.from_user.id, "Фотографии отправлены в канал.")



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)