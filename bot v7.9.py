from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from config import *
from states import *
from validation import *
import json
import sys

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
# Конец импорта json словарей



def create_keyboard(button_texts, resize_keyboard=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=2)
    buttons = [KeyboardButton(text=text) for text in button_texts]
    keyboard.add(*buttons)
    return keyboard


class CarBotHandler:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.sent_message = None

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
        selected_brand = event.text
        valid_brands = dict_car_brands_and_models
        if await validate_car_brand(selected_brand, valid_brands):
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await self.delete_hello(event)
            # Создаем клавиатуру
            keyboard = create_keyboard(dict_car_brands_and_models[selected_brand])
            await event.answer("Отлично! Выберите модель автомобиля:", reply_markup=keyboard)
            await state.set_state(STATE_CAR_MODEL)
        else:
            await self.delete_previous_question(event)
            await self.delete_hello(event)
            keyboard = create_keyboard(dict_car_brands_and_models.keys())
            await bot.send_message(event.from_user.id, "Пожалуйста, выберите бренд из предложенных вариантов или напишите нам если вашего бренда нет", reply_markup=keyboard)
            await state.set_state(STATE_CAR_BRAND)

    async def get_car_model(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        car_brand = user_data.get("car_brand", "")
        valid_models = dict_car_brands_and_models.get(car_brand, [])

        if await validate_car_model(event.text, valid_models):
            user_data["car_model"] = event.text
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Какой год выпуска у автомобиля? (напишите)")
            await state.set_state(STATE_CAR_YEAR)
        else:
            await self.delete_previous_question(event)
            keyboard = create_keyboard(valid_models)
            await bot.send_message(event.from_user.id, "Пожалуйста, выберите модель из предложенных вариантов.",
                                   reply_markup=keyboard)
            await state.set_state(STATE_CAR_MODEL)

    async def get_car_year(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_year(event.text):
            user_data["car_year"] = event.text
            keyboard = create_keyboard(dict_car_body_types)
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Отлично! Какой тип кузова у автомобиля?", reply_markup=keyboard)
            await state.set_state(STATE_CAR_BODY_TYPE)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите год в формате YYYY (например, 1990 ил   и 2022)")
            await state.set_state(STATE_CAR_YEAR)

    async def get_car_body_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_body_type"] = event.text

        keyboard = create_keyboard(dict_car_engine_types)

        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Отлично! Какой тип двигателя у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_ENGINE_TYPE)

    async def get_car_engine_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_engine_type"] = event.text

        # Добавляем кнопки на основе словаря
        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Хорошо! Какой объем двигателя у автомобиля (л.)? (напишите через точку: например 1.6)")
        await state.set_state(STATE_CAR_ENGINE_VOLUME)

    async def get_car_engine_volume(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_engine_volume(event.text):
            user_data["car_engine_volume"] = event.text

            # Добавляем кнопки на основе словаря
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Отлично! Укажите мощность двигателя автомобиля (л.с.). (напишите)")
            await state.set_state(STATE_CAR_POWER)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, корректный объем двигателя (в пределах от 0.2 до 10.0 литров) через точку или целым числом(!).")
            await state.set_state(STATE_CAR_ENGINE_VOLUME)

    async def get_car_power(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_car_power(event.text):
            user_data["car_power"] = event.text

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add(*dict_car_transmission_types)
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Отлично! Какой тип коробки передач используется в автомобиле?", reply_markup=keyboard)
            await state.set_state(STATE_CAR_TRANSMISSION_TYPE)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректную мощность двигателя (в пределах от 50 до 1000 л.с.).")
            await state.set_state(STATE_CAR_POWER)

    async def get_car_transmission_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        if event.text in dict_car_transmission_types:
            user_data["car_transmission_type"] = event.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add(*dict_car_colors)
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Какого цвета автомобиль?", reply_markup=keyboard)
            await state.set_state(STATE_CAR_COLOR)

    async def get_car_color(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_color"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_mileages)

        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Каков пробег автомобиля? (напишите пробег в км. или выберите 'Новый')", reply_markup=keyboard)
        await state.set_state(STATE_CAR_MILEAGE)

    async def get_car_mileage(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        if await validate_car_mileage(event.text):
            user_data["car_mileage"] = event.text

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add(*dict_car_document_statuses)
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Каков статус документов у автомобиля (тыс. км.)? например 100 = 100 тыс. км.", reply_markup=keyboard)
            await state.set_state(STATE_CAR_DOCUMENT_STATUS)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректное значение пробега.")
            await state.set_state(STATE_CAR_MILEAGE)

    async def get_car_document_status(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_document_status"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_owners)
        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Сколько владельцев у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_OWNERS)

    async def get_car_owners(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_owners"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_customs_cleared)
        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Растаможен ли автомобиль?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_CUSTOMS_CLEARED)

    async def get_car_customs_cleared(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_customs_cleared"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_conditions)

        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Выберите состояние автомобиля:", reply_markup=keyboard)
        await state.set_state(STATE_CAR_CONDITION)

    async def get_car_condition(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_condition"] = event.text

        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Описание автомобиля. (напишите)")
        await state.set_state(STATE_CAR_DESCRIPTION)

    async def get_car_description(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_car_description(event.text):
            user_data["car_description"] = event.text

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add(*dict_currency)

            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Выберите валюту:", reply_markup=keyboard)
            await state.set_state(STATE_SELECT_CURRENCY)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректное описание.")
            await state.set_state(STATE_CAR_DESCRIPTION)

    async def select_currency(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["currency"] = event.text
        await state.update_data(user_data=user_data)
        await self.delete_previous_question(event)
        await event.answer("Цена автомобиля?")
        await state.set_state(STATE_CAR_PRICE)

    async def get_car_price(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_car_price(event.text):
            user_data["car_price"] = event.text

            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Прекрасно! Где находится автомобиль? Город/пункт. (напишите)")
            await state.set_state(STATE_CAR_LOCATION)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректную цену.")
            await state.set_state(STATE_CAR_PRICE)

    async def get_car_location(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        if await validate_car_location(event.text):
            user_data["car_location"] = event.text
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Прекрасно! Укажите имя продавца. (напишите)")
            await state.set_state(STATE_SELLER_NAME)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректные данные.")
            await state.set_state(STATE_CAR_LOCATION)

    async def get_seller_name(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})

        if await validate_name(event.text) is True:
            user_data["seller_name"] = event.text
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Отлично! Какой телефонный номер у продавца? (напишите в формате +7XXXNNNXXNN)")
            await state.set_state(STATE_SELLER_PHONE)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректное имя.")
            await state.set_state(STATE_SELLER_NAME)

    async def get_seller_phone(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        if await validate_phone_number(event.text) is True:
            user_data["seller_phone"] = event.text
            await state.update_data(user_data=user_data)
            await self.delete_previous_question(event)
            await event.answer("Добавьте фотографии авто")
            await state.set_state(STATE_CAR_PHOTO)
        else:
            await self.delete_previous_question(event)
            await event.answer("Пожалуйста, введите корректный номер в формате +7XXXNNNXXNN.")
            await state.set_state(STATE_SELLER_PHONE)
    async def handle_photos(self, message, state):
        user_data = await state.get_data('user_data')
        photo_id = message.photo[-1].file_id

        caption = (
            f"🛞 <b>#{user_data.get('user_data').get('car_brand')}{user_data.get('user_data').get('car_model')}</b>\n\n"
            f"   <b>-Год:</b> {user_data.get('user_data', {}).get('car_year')}\n"
            f"   <b>-Пробег (км.):</b> {user_data.get('user_data').get('car_mileage')}\n"
            f"   <b>-Тип КПП:</b> {user_data.get('user_data').get('car_transmission_type')}\n"
            f"   <b>-Кузов:</b> {user_data.get('user_data').get('car_body_type')}\n"
            f"   <b>-Тип двигателя:</b> {user_data.get('user_data').get('car_engine_type')}\n"
            f"   <b>-Объем двигателя (л.):</b> {user_data.get('user_data').get('car_engine_volume')}\n"
            f"   <b>-Мощность (л.с.):</b> {user_data.get('user_data').get('car_power')}\n"
            f"   <b>-Цвет:</b> {user_data.get('user_data').get('car_color')}\n"
            f"   <b>-Статус документов:</b> {user_data.get('user_data').get('car_document_status')}\n"
            f"   <b>-Количество владельцев:</b> {user_data.get('user_data').get('car_owners')}\n"
            f"   <b>-Растаможка:</b> {'Да' if user_data.get('user_data').get('car_customs_cleared') else 'Нет'}\n"
            f"   <b>-Состояние:</b> {user_data.get('user_data').get('car_condition')}\n\n"
            f"ℹ️<b>Дополнительная информация:</b> {user_data.get('user_data').get('car_description')}\n\n"
            f"🔥<b>Цена:</b> {user_data.get('user_data').get('car_price')} {user_data.get('user_data').get('currency')}\n\n"
            f"📍<b>Местоположение:</b> {user_data.get('user_data').get('car_location')}\n"
            f"👤<b>Продавец:</b> <span class='tg-spoiler'> {user_data.get('user_data').get('seller_name')} </span>\n"
            f"📲<b>Телефон продавца:</b> <span class='tg-spoiler'>{user_data.get('user_data').get('seller_phone')} </span>\n"
            f"💬<b>Телеграм:</b> <span class='tg-spoiler'>{message.from_user.username if message.from_user.username is not None else 'по номеру телефона'}</span>\n\n"            
            f"ООО 'Продвижение' Авто в ДНР (link: разместить авто)"
        )


        print(user_data)
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
            KeyboardButton("Отправить объявление")
        )
        await message.reply("Фото добавлено", reply_markup=keyboard)
        await state.finish()

    async def send_advertisement(self, message, state):
        user_id = message.from_user.id
        user_data = await state.get_data()
        await self.send_photos_to_channel(user_id, user_data)
        await message.answer("Объявление отправлено в канал.")

    async def send_photos_to_channel(self, user_id, user_data):
        async with lock:
            if buffered_photos:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
                await bot.send_message(user_id, "Фотографии отправлены в канал.")
                buffered_photos.clear()


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

@dp.message_handler(state=STATE_CAR_MODEL)
async def process_model(event: types.Message, state: FSMContext):
    await car_bot.get_car_model(event, state)

@dp.message_handler(state=STATE_CAR_YEAR)
async def get_car_year_handler(event: types.Message, state: FSMContext):
    await car_bot.get_car_year(event, state)

@dp.message_handler(state=STATE_CAR_BODY_TYPE)
async def get_car_body_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_body_type(event, state)

@dp.message_handler(state=STATE_CAR_ENGINE_TYPE)
async def get_car_engine_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_engine_type(event, state)

@dp.message_handler(state=STATE_CAR_ENGINE_VOLUME)
async def get_car_engine_volume(event: types.Message, state: FSMContext):
    await car_bot.get_car_engine_volume(event, state)

@dp.message_handler(state=STATE_CAR_POWER)
async def get_car_power(event: types.Message, state: FSMContext):
    await car_bot.get_car_power(event, state)

@dp.message_handler(state=STATE_CAR_TRANSMISSION_TYPE)
async def get_car_transmission_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_transmission_type(event, state)

@dp.message_handler(state=STATE_CAR_COLOR)
async def get_car_color(event: types.Message, state: FSMContext):
    await car_bot.get_car_color(event, state)

@dp.message_handler(state=STATE_CAR_MILEAGE)
async def get_car_mileage(event: types.Message, state: FSMContext):
    await car_bot.get_car_mileage(event, state)

@dp.message_handler(state=STATE_CAR_DOCUMENT_STATUS)
async def get_car_document_status(event: types.Message, state: FSMContext):
    await car_bot.get_car_document_status(event, state)

@dp.message_handler(state=STATE_CAR_OWNERS)
async def get_car_owners(event: types.Message, state: FSMContext):
    await car_bot.get_car_owners(event, state)

@dp.message_handler(state=STATE_CAR_CUSTOMS_CLEARED)
async def get_car_customs_cleared(event: types.Message, state: FSMContext):
    await car_bot.get_car_customs_cleared(event, state)

@dp.message_handler(state=STATE_CAR_CONDITION)
async def get_car_condition(event: types.Message, state: FSMContext):
    await car_bot.get_car_condition(event, state)

@dp.message_handler(state=STATE_CAR_DESCRIPTION)
async def get_car_description(event: types.Message, state: FSMContext):
    await car_bot.get_car_description(event, state)

@dp.message_handler(state=STATE_SELECT_CURRENCY)
async def select_currency(event: types.Message, state: FSMContext):
    await car_bot.select_currency(event, state)

@dp.message_handler(state=STATE_CAR_PRICE)
async def get_car_price(event: types.Message, state: FSMContext):
    await car_bot.get_car_price(event, state)

@dp.message_handler(state=STATE_CAR_LOCATION)
async def get_car_location_handler(event: types.Message, state: FSMContext):
    await car_bot.get_car_location(event, state)

@dp.message_handler(state=STATE_SELLER_NAME)
async def get_seller_name_handler(event: types.Message, state: FSMContext):
    await car_bot.get_seller_name(event, state)

@dp.message_handler(state=STATE_SELLER_PHONE)
async def get_seller_phone_handler(event: types.Message, state: FSMContext):
    await car_bot.get_seller_phone(event, state)

@dp.message_handler(state=STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos_handler(message: types.Message, state: FSMContext):
    await car_bot.handle_photos(message, state)

@dp.message_handler(lambda message: message.text == "Отправить объявление")
async def send_advertisement(message: types.Message, state: FSMContext):
    await car_bot.send_advertisement(message, state)
    await car_bot.send_photos_to_channel(message.from_user.id, await state.get_data())



# старт бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
