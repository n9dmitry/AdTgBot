from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from config import *
from state import *
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
# Конец импорта json словарей


# get_car_data
# get_car_data_input

class CarBotHandler:
    def __init__(self, ):
        self.lock = asyncio.Lock()
        self.buffered_photos = []

    async def start(self, event, state):
        user_id = event.from_user.id
        user_data = await state.get_data() or {}
        user_data["user_id"] = user_id
        await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")

        # Создаем ReplyKeyboardMarkup с вариантами выбора бренда
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        brands = list(dict_car_brands_and_models.keys())
        buttons = [KeyboardButton(text=brand) for brand in brands]
        keyboard.add(*buttons)
        keyboard.add(KeyboardButton(text='Ввести свою марку'))

        await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state(STATE_CAR_BRAND)

    async def process_brand_selection(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        selected_brand = event.text

        user_data["car_brand"] = selected_brand
        await state.update_data(user_data=user_data)

        # Создаем ReplyKeyboardMarkup с моделями выбранного бренда
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        models = dict_car_brands_and_models[selected_brand]
        buttons = [KeyboardButton(text=model) for model in models]
        keyboard.add(*buttons)

        await event.answer("Выберите модель автомобиля:", reply_markup=keyboard)
        await state.set_state(STATE_CAR_MODEL)

    async def process_model(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        selected_model = event.text

        user_data["car_model"] = selected_model
        await state.update_data(user_data=user_data)

        await event.answer("Отлично! Какой год выпуска у автомобиля?")
        await state.set_state(STATE_CAR_YEAR)

    async def get_car_year(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_year"] = event.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_body_types)  # Добавляем кнопки на основе словаря
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой тип кузова у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_BODY_TYPE)

    async def get_car_body_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_body_type"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_engine_types)  # Добавляем кнопки на основе словаря

        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой тип двигателя у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_ENGINE_TYPE)

    async def get_car_engine_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_engine_type"] = event.text

        # Добавляем кнопки на основе словаря
        await state.update_data(user_data=user_data)
        await event.answer("Хорошо! Какой объем двигателя у автомобиля?")
        await state.set_state(STATE_CAR_ENGINE_VOLUME)

    async def get_car_engine_volume(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_engine_volume"] = event.text

        # Добавляем кнопки на основе словаря
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Укажите мощность двигателя автомобиля.")
        await state.set_state(STATE_CAR_POWER)

    async def get_car_power(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_power"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_transmission_types)
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой тип коробки передач используется в автомобиле?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_TRANSMISSION_TYPE)

    async def get_car_transmission_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_transmission_type"] = event.text

        await state.update_data(user_data=user_data)
        await event.answer("Какого цвета автомобиль?", )
        await state.set_state(STATE_CAR_COLOR)

    async def get_car_color(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_color"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Каков пробег автомобиля?")
        await state.set_state(STATE_CAR_MILEAGE)

    async def get_car_mileage(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_mileage"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_document_statuses)
        await state.update_data(user_data=user_data)
        await event.answer("Каков статус документов у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_DOCUMENT_STATUS)

    async def get_car_document_status(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_document_status"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_owners)
        await state.update_data(user_data=user_data)
        await event.answer("Сколько владельцев у автомобиля?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_OWNERS)

    async def get_car_owners(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_owners"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_car_customs_cleared)
        await state.update_data(user_data=user_data)
        await event.answer("Растаможен ли автомобиль?", reply_markup=keyboard)
        await state.set_state(STATE_CAR_CUSTOMS_CLEARED)

    async def get_car_customs_cleared(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_customs_cleared"] = event.text

        await state.update_data(user_data=user_data)
        await event.answer("Добавьте описание.")
        await state.set_state(STATE_CAR_DESCRIPTION)

    async def get_car_description(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_description"] = event.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*dict_currency)

        await state.update_data(user_data=user_data)
        await event.answer("Выберите валюту:", reply_markup=keyboard)
        await state.set_state(STATE_SELECT_CURRENCY)

    async def select_currency(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["currency"] = event.text
        await state.update_data(user_data=user_data)

        await event.answer("Какова цена автомобиля?")
        await state.set_state(STATE_CAR_PRICE)

    async def get_car_price(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_price"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Прекрасно! Где находится автомобиль?")
        await state.set_state(STATE_CAR_LOCATION)

    async def get_car_location(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["car_location"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Прекрасно! Укажите имя продавца.")
        await state.set_state(STATE_SELLER_NAME)

    async def get_seller_name(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["seller_name"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Отлично! Какой телефонный номер у продавца?")
        await state.set_state(STATE_SELLER_PHONE)

    async def get_seller_phone(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        user_data["seller_phone"] = event.text
        await state.update_data(user_data=user_data)
        await event.answer("Добавьте фотографии авто")
        await state.set_state(STATE_CAR_PHOTO)

    async def handle_photos(self, message, state):
        user_data = (await state.get_data()).get("user_data", {})
        photo_id = message.photo[-1].file_id

        caption = (
            f"🛞 <b>#{user_data.get('user_data').get('car_brand')}</b> <b>{user_data.get('user_data').get('car_model')}</b>\n\n"
            f"   <b>-Год:</b> {user_data.get('user_data').get('car_year')}г\n"
            f"   <b>-Пробег:</b> {user_data.get('user_data').get('car_mileage')}км\n"
            f"   <b>-Тип КПП:</b> {user_data.get('user_data').get('car_transmission_type')}\n"
            f"   <b>-Кузов:</b> {user_data.get('user_data').get('car_body_type')}\n"
            f"   <b>-Тип двигателя:</b> {user_data.get('user_data').get('car_engine_type')}\n"
            f"   <b>-Объем двигателя (л):</b> {user_data.get('user_data').get('car_engine_volume')}\n"
            f"   <b>-Мощность:</b> {user_data.get('user_data').get('car_power')}л.с.\n"
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
            f"💬<b>Телеграм:</b> <span class='tg-spoiler'>{message.from_user.username}</span>\n\n"
            f"ООО 'Продвижение' Авто в ДНР (link: разместить авто)"
        )

        print(user_data)
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

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Отправить объявление")
        )
        await message.reply("Фото добавлено", reply_markup=keyboard)
        await state.finish()

    async def send_advertisement(self, message, state):
        user_id = message.from_user.id
        user_data = await state.get_data()
        async with self.lock:
            if buffered_photos:
                await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
                await bot.send_message(user_id, "Фотографии отправлены в канал.")
                buffered_photos.clear()
        await message.answer("Объявление отправлено в канал.")


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
    await car_bot.process_brand_selection(event, state)

@dp.message_handler(state=STATE_CAR_MODEL)
async def process_model(event: types.Message, state: FSMContext):
    await car_bot.process_model(event, state)

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
async def send_advertisement_handler(message: types.Message, state: FSMContext):
    await car_bot.send_advertisement(message, state)




# старт бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)