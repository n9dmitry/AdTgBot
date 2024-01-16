from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import uuid
import asyncio
from dicts import dict_car_brands_and_models

API_TOKEN = '6803723279:AAGEujzpCZq3nMCidAt0MsZjBEMKkQUDw9M'
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
#
# # Массивы вопросов
# dict_car_brands_and_models = {
#     'Audi': ['Ввести марку', 'A3', 'A4', 'Q5', 'Q7'],
#     'BMW': ['Ввести марку', '3 Series', '5 Series', 'X3', 'X5'],
#     'Mercedes-Benz': ['Ввести марку', 'C-Class', 'E-Class', 'GLC', 'GLE'],
#     'Chevrolet': ['Ввести марку', 'Cruze', 'Malibu', 'Equinox', 'Tahoe'],
#     'Ford': ['Ввести марку', 'Focus', 'Fusion', 'Escape', 'Explorer'],
#     'Honda': ['Ввести марку', 'Civic', 'Accord', 'CR-V', 'Pilot'],
#     'Hyundai': ['Ввести марку', 'Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
#     'Kia': ['Ввести марку', 'Optima', 'Sorento', 'Sportage', 'Telluride'],
#     'Nissan': ['Ввести марку', 'Altima', 'Maxima', 'Rogue', 'Pathfinder'],
#     'Toyota': ['Ввести марку', 'Camry', 'Corolla', 'Rav4', 'Highlander'],
#     'Volkswagen': ['Ввести марку', 'Golf', 'Jetta', 'Tiguan', 'Atlas'],
#     'Volvo': ['Ввести марку', 'S60', 'S90', 'XC60', 'XC90'],
#     'Ferrari': ['Ввести марку', '488', 'F8 Tributo', 'Portofino', 'SF90 Stradale'],
#     'Porsche': ['Ввести марку', '911', 'Cayenne', 'Panamera', 'Macan'],
#     'Tesla': ['Ввести марку', 'Model S', 'Model 3', 'Model X', 'Model Y'],
#     'Lamborghini': ['Ввести марку', 'Huracan', 'Aventador', 'Urus'],
#     'Jaguar': ['Ввести марку', 'XE', 'XF', 'F-Pace', 'I-Pace'],
#     'Land Rover': ['Ввести марку', 'Discovery', 'Range Rover Evoque', 'Range Rover Sport', 'Defender'],
#     'Mazda': ['Ввести марку', 'Mazda3', 'Mazda6', 'CX-5', 'CX-9'],
#     'Subaru': ['Ввести марку', 'Impreza', 'Outback', 'Forester', 'Ascent'],
#     'LADA': ['Ввести марку', 'Vesta', 'Granta', 'XRAY', '4x4'],
#     'УАЗ': ['Ввести марку', 'Patriot', 'Hunter', 'Bukhanka'],
#     'ГАЗ': ['Ввести марку', 'Sobol', 'Next', 'Gazelle'],
#     'КАМАЗ': ['Ввести марку', '5490', '6520', '43118'],
#     'АвтоВАЗ': ['Ввести марку', 'LADA 4x4', 'LADA Kalina', 'LADA Priora', 'LADA XRAY']
# }
# # car_year - нужна просто проверка на инпут на 4 знака
# dict_car_body_types = {
#     "Седан",
#     "Хэтчбек",
#     "Универсал",
#     "Купе",
#     "Кабриолет",
#     "Спортивный купе",
#     "Внедорожник",
#     "Кроссовер",
#     "Минивэн",
#     "Пикап",
# }
# dict_car_engine_types = {
#     "Бензиновый",
#     "Дизельный",
#     "Электрический",
#     "Гибридный",
#     "Турбированный",
#     "Роторный (Ванкель)",
#     "Газовый",
#     "Водородный",
# }
# # car_engine_volume (объём) - не нужен словарь. инпут проверка (продумать логику)
# # car_power (мощность) - не нужен словарь. инпут проверка (продумать логику)
# dict_car_transmission_types = {
#     "Механическая",
#     "Автоматическая",
#     "Роботизированная",
#     "Вариатор",
# }
# dict_car_colors = {
#     "Черный": "⚫",
#     "Белый": "⚪",
#     "Серый": "⚪",
#     "Красный": "🔴",
#     "Синий": "🔵",
#     "Зеленый": "🟢",
#     "Желтый": "🟡",
#     "Оранжевый": "🟠",
#     "Фиолетовый": "🟣",
#     "Розовый": "💗",
# }
# # car_mileage (пробег) - проверка на инпут, примеры
# dict_car_document_statuses = {
#     "Оригинал",
#     "Дубликат",
#     "Временный",
#     "Без документов",
#     "Исполненные",
#     "Отозванные",
#     "На рассмотрении",
#     "Продленные",
#     "Утерянные",
# }
# dict_car_owners = {
#     "1",
#     "2",
#     "3",
#     "4 и более",
# }
# # car_customs_cleared - yes/no
# # car_description - проверка на количество символов
# # car_price - проверка на количество символов
# # car_location - валидация
# # seller_name - валидация
# # seller_phone - валидация


@dp.message_handler(Command("start"))
async def cmd_start(event: types.Message, state: FSMContext):
    user_id = event.from_user.id
    user_data = await state.get_data() or {}
    user_data["user_id"] = user_id
    await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")

    # Создаем инлайн-клавиатуру с вариантами выбора бренда
    keyboard = InlineKeyboardMarkup(row_width=2)
    brands = list(dict_car_brands_and_models.keys())
    buttons = [InlineKeyboardButton(text=brand, callback_data=f"brand_{brand}") for brand in brands]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text='Ввести свою марку', callback_data='brand_custom'))

    await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
    await state.set_state('state_car_brand')


@dp.callback_query_handler(lambda c: c.data.startswith('brand_'), state='state_car_brand')
async def process_brand_callback(query: types.CallbackQuery, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    selected_brand = query.data.split('_')[1]

    if selected_brand == 'custom':
        await query.message.answer("Введите свою марку автомобиля:")
        await state.set_state('state_car_model')
    else:
        user_data["car_brand"] = selected_brand
        await state.update_data(user_data=user_data)

        # Создаем инлайн-клавиатуру с моделями выбранного бренда
        keyboard = InlineKeyboardMarkup(row_width=2)
        models = dict_car_brands_and_models[selected_brand]
        buttons = [InlineKeyboardButton(text=model, callback_data=f"model_{model}") for model in models]
        keyboard.add(*buttons)

        await query.message.answer("Выберите модель автомобиля:", reply_markup=keyboard)
        await state.set_state('state_car_model')

    await query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('model_'), state='state_car_model')
async def process_model_callback(query: types.CallbackQuery, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    selected_model = query.data.split('_')[1]
    user_data["car_model"] = selected_model
    await state.update_data(user_data=user_data)
    await query.message.answer("Отлично! Какой год выпуска у автомобиля?")
    await state.set_state('state_car_year')
    await query.answer()

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
    await event.answer("Добавьте описание.")
    await state.set_state(STATE_CAR_DESCRIPTION)

@dp.message_handler(state=STATE_CAR_DESCRIPTION)
async def get_car_description(event: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get("user_data", {})
    # Добавление ключа "car_description" со значением event.text в словарь user_data
    user_data["car_description"] = event.text
    await state.update_data(user_data=user_data)  # Обновление данных состояния

    # Место для сохранения значений после STATE_CAR_PHOTO
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
    await event.answer("Добавьте фотографии авто")
    await state.set_state(STATE_CAR_PHOTO)

@dp.message_handler(state=STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data() or {}
    photo_id = message.photo[-1].file_id

    caption = (
        f"🚗 #{user_data.get('user_data').get('car_brand')} {user_data.get('user_data').get('car_model')}\n"
        f"Год: {user_data.get('user_data').get('car_year')}\n"
        f"Тип КПП: {user_data.get('user_data').get('car_transmission_type')}\n"
        f"Кузов: {user_data.get('user_data').get('car_body_type')}\n"
        f"Тип двигателя: {user_data.get('user_data').get('car_engine_type')}\n"
        f"Объем двигателя: {user_data.get('user_data').get('car_engine_volume')}\n"
        f"Мощность: {user_data.get('user_data').get('car_power')}\n"
        f"Цвет: {user_data.get('user_data').get('car_color')}\n"
        f"Пробег: {user_data.get('user_data').get('car_mileage')}\n"
        f"Статус документов: {user_data.get('user_data').get('car_document_status')}\n"
        f"Количество владельцев: {user_data.get('user_data').get('car_owners')}\n"
        f"Растаможка: {user_data.get('user_data').get('car_customs_cleared')}\n"
        f"Дополнительная информация: {user_data.get('user_data').get('car_description')}\n"
        f"Цена: {user_data.get('user_data').get('car_price')} руб\n"
        f"Местоположение: {user_data.get('user_data').get('car_location')}\n"
        f"Продавец: {user_data.get('user_data').get('seller_name')}\n"
        f"Телефон продавца: {user_data.get('user_data').get('seller_phone')}"
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

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)