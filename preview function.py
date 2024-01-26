from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from config import *
from states import *
from validation import *
import json

# Загрузка JSON в начале скрипта
with open('dicts.json', 'r', encoding='utf-8') as file:
    dicts = json.load(file)

dict_car_brands_and_models = dicts.get("dict_car_brands_and_models", {})
dict_car_body_types = dicts.get("dict_car_body_types", {})
dict_car_engine_types = dicts.get("dict_car_engine_types", {})
dict_car_transmission_types = dicts.get("dict_car_transmission_types", {})
dict_car_colors = dicts.get("dict_car_colors", {})
dict_car_document_statuses = dicts.get("dict_car_document_statuses", {})
dict_car_owners = dicts.get("dict_car_owners", {})
dict_car_customs_cleared = dicts.get("dict_car_customs_cleared", {})
dict_currency = dicts.get("dict_currency", {})
dict_car_conditions = dicts.get("dict_car_conditions", {})
dict_car_mileages = dicts.get("dict_car_mileages", {})
dict_edit_buttons = dicts.get("dict_edit_buttons", {})
# Конец импорта json словарей


# Создание клавиатуры
def create_keyboard(button_texts, resize_keyboard=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=2)
    buttons = [KeyboardButton(text=text) for text in button_texts]
    keyboard.add(*buttons)
    return keyboard

class CarBotHandler:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.sent_message = None
        self.bot = Bot

# Удаление предыдущих ответов
    async def delete_previous_question(self, event):
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id - 1)

    async def delete_hello(self, event):
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id - 2)

# Начало работы бота

    async def start(self, event, state):
        await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state(STATE_CAR_BRAND)

    async def get_car_brand(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        if user_data.get('car_brand') is None:
            print(user_data.get('car_brand'))
            selected_brand = event.text
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await self.delete_hello(event)

            await event.answer("Отлично! Перетащите фото:")
            await state.set_state(STATE_CAR_PHOTO)
            # редкатирование
        else:
            keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
            await event.answer(f"Ваше значение бренда: '{user_data.get('user_data').get('car_brand')}'. Введите новое значение:", reply_markup=keyboard)
            selected_brand = event.text
            user_data["car_brand"] = selected_brand
            # await self.delete_previous_question(event)


    async def handle_photos(self, message, state):
        user_data = await state.get_data('user_data')
        photo_id = message.photo[-1].file_id
        # Construct the caption
        caption = (
            f"🛞 <b>#{user_data.get('user_data').get('car_brand')}{user_data.get('user_data').get('car_model')}</b>\n\n"
            f"💬<b>Телеграм:</b> <span class='tg-spoiler'>{message.from_user.username if message.from_user.username is not None else 'по номеру телефона'}</span>\n\n"
            f"ООО 'Продвижение' Авто в ДНР (link: разместить авто)"
        )

        photo_uuid = str(uuid.uuid4())

        if "sent_photos" not in user_data:
            user_data["sent_photos"] = []

        user_data["sent_photos"].append({"file_id": photo_id, "uuid": photo_uuid})
        buffered_photos.append(InputMediaPhoto(media=photo_id, caption=caption, parse_mode=types.ParseMode.HTML))
        if len(buffered_photos) > 1:
            for i in range(len(buffered_photos) - 1):
                buffered_photos[i].caption = None
            last_photo = buffered_photos[-1]
            last_photo.caption = caption

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Следущий шаг"),
        )
        await message.reply("Фото в обработке", reply_markup=keyboard)
        await state.finish()

    async def preview_advertisement(self, message):
        try:
            await bot.send_media_group(chat_id=message.chat.id, media=buffered_photos, disable_notification=True)
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton("Отправить в канал"),
                KeyboardButton("Редактировать"),
            )
            await message.reply("Так будет выглядеть ваше объявление. Вы можете либо отредактировать либо разместить.", reply_markup=keyboard)

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    async def send_advertisement(self, message):
        user_id = message.from_user.id
        async with lock:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            await bot.send_message(user_id, "Объявление отправлено в канал.")
            # buffered_photos.clear()

    async def edit_advertisement(self, message, state):
        user_data = await state.get_data()
        keyboard = create_keyboard(dict_edit_buttons)
        await message.answer("Выберите кнопку:", reply_markup=keyboard)
        # response = await state.wait_for_message()
        # if response.text == "Редактировать бренд автомобиля":
        #     await self.edit_car_brand(response, state)
        # Пример функции редактирования бренда автомобиля






car_bot = CarBotHandler()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
lock = asyncio.Lock()
buffered_photos = []

@dp.message_handler(commands=["start"])
async def cmd_start(event: types.Message, state: FSMContext):
    await car_bot.start(event, state)

@dp.message_handler(state=STATE_CAR_BRAND)
async def process_brand_selection(event: types.Message, state: FSMContext):
    await car_bot.get_car_brand(event, state)

@dp.message_handler(state=STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(message: types.Message, state: FSMContext):
    await car_bot.handle_photos(message, state)

@dp.message_handler(lambda message: message.text == "Следущий шаг")
async def preview_advertisement(message: types.Message):
    await car_bot.preview_advertisement(message)

@dp.message_handler(lambda message: message.text == "Отправить в канал")
async def send_advertisement(message: types.Message):
    await car_bot.send_advertisement(message)

@dp.message_handler(lambda message: message.text == "Редактировать")
async def edit_advertisement(message: types.Message, state: FSMContext):
    await car_bot.edit_advertisement(message, state)



@dp.message_handler(lambda message: message.text == "Редактировать бренд автомобиля")
async def edit_car_brand(message, state):
    await car_bot.get_car_brand(message, state)
    # user_data = await state.get_data()
    #
    # if user_data.get('car_brand'):
    #     print({user_data.get('user_data').get('car_brand')})
    #     keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
    #     await message.answer(f"Ваше значение бренда: '{user_data.get('user_data').get('car_brand')}'. Введите новое значение:", reply_markup=keyboard)
    #     selected_brand = message.text
    #     user_data["car_brand"] = selected_brand
    # else:
    #     print({user_data.get('user_data').get('car_brand')})
    #     await message.answer("Какой год выпуска у автомобиля? (напишите)")

# старт бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)