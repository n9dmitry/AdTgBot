import asyncio
import json
import random
import datetime
import uuid
import openpyxl

from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import KeyboardButton, InputMediaPhoto, Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from fuzzywuzzy import fuzz

from config import *
from states import *
from validation import *
from enumlist import *
from middleware_photogroup import AlbumMiddleware


router = Router()

router.message.middleware(AlbumMiddleware())

lock = asyncio.Lock()
session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": ParseMode.HTML}
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# Загрузка JSON в начале скрипта
with open('dicts.json', 'r', encoding='utf-8') as file:
    dicts = json.load(file)

dict_start_brands = dicts.get("dict_start_brands", {})
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

def create_keyboard(button_texts):
    buttons = [KeyboardButton(text=text) for text in button_texts]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons).adjust(2)
    return builder

def recognize_car_model(event, brand_name):
    models = None
    similar_brands = []

    if brand_name.lower() in ['жигули']:
        brand_name = 'Lada (ВАЗ)'

    with open('cars.json', encoding='utf-8') as file:
        data = json.load(file)

    found_brand = False
    for item in data:
        # Сравнение имени бренда с учетом расстояния Левенштейна
        if 'name' in item and fuzz.token_sort_ratio(brand_name.lower(), item['name'].lower()) >= 90:
            if 'models' in item:
                models = item['models']
            found_brand = True
            break
        # Сравнение кириллического имени бренда
        elif 'cyrillic-name' in item and fuzz.token_sort_ratio(brand_name.lower(), item['cyrillic-name'].lower()) >= 90:
            if 'models' in item:
                models = item['models']
            found_brand = True
            break

    if not found_brand and len(brand_name) >= 3:
        for inner_item in data:
            # Поиск похожих брендов с учетом расстояния Левенштейна
            if 'name' in inner_item and fuzz.token_sort_ratio(brand_name.lower(), inner_item['name'].lower()) >= 50 \
                    and inner_item['name'] not in similar_brands:
                similar_brands.append(inner_item['name'])
            # Поиск похожих кириллических брендов
            elif 'cyrillic-name' in inner_item and fuzz.token_sort_ratio(brand_name.lower(),
                                                                         inner_item['cyrillic-name'].lower()) >= 50 \
                    and inner_item['name'] not in similar_brands:
                similar_brands.append(inner_item['name'])

        if similar_brands:
            response_message = "Похожие бренды:\n" + "\n".join(similar_brands)
            await event.answer(response_message)

    return models if models else []

# Команды
@router.message(F.text == "Перезагрузить бота")
@router.message(F.text == "Добавить ещё объявление")
@router.message(F.text == "Отменить и заполнить заново")
@router.message(User.STATE_SUPPORT_END)
@router.message(Command("restart"))
async def restart(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Бот перезапущен.")
    await start(message, state)


@router.message(Command("support"))
async def support(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    secret_number = str(random.randint(100, 999))

    await message.answer(f"Нашли баг? Давайте отправим сообщение разработчикам! "
                         f"Но перед этим введите проверку. Докажите что вы не робот. Напишите число {secret_number}:")
    user_data['secret_number'] = secret_number
    await state.update_data(user_data)
    await state.set_state(User.STATE_SUPPORT_VALIDATION)


@router.message(User.STATE_SUPPORT_VALIDATION)
async def support_validation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    secret_number = user_data['secret_number']
    if message.text.isdigit() and message.text == secret_number:
        await message.reply(f"Проверка пройдена успешно!")
        await asyncio.sleep(1)
        await message.answer(f"Опишите техническую проблему в деталях для разработчиков: ")
        await state.set_state(User.STATE_SUPPORT_MESSAGE)
    else:
        await message.answer(f"Попробуйте ещё раз!")
        await asyncio.sleep(1)
        await support(message, state)


@router.message(User.STATE_SUPPORT_MESSAGE)
async def support_message(message: types.Message, state: FSMContext):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_to_write = f"""
    Дата: {current_time}
    Имя: {message.from_user.full_name}
    Telegram @{message.from_user.username or message.from_user.id} 
  
    Сообщение: {message.text}
    ...
        """
    # Открываем файл для записи и записываем сообщение
    with open("support.txt", "a") as file:
        file.write(message_to_write)
    builder = create_keyboard(['Перезагрузить бота'])
    await message.reply("Спасибо за ваше сообщение! Мы рассмотрим вашу проблему!",
                        reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(User.STATE_SUPPORT_END)

# Начало работы бота
@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    image_hello_path = ImageDirectory.auto_say_hi
    await message.answer_photo(photo=types.FSInputFile(image_hello_path),
                               caption=f"Привет, {message.from_user.first_name}! Давай продадим твоё авто! Начнём же сбор данных!")
    await asyncio.sleep(0.5)
    builder = create_keyboard(list(dict_start_brands))
    image_path = ImageDirectory.auto_car_brand
    await message.answer_photo(photo=types.FSInputFile(image_path), caption="Выберите бренд автомобиля:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(User.STATE_CAR_BRAND)


@router.message(User.STATE_CAR_BRAND)
async def get_car_brand(message, state):
    search_brand = message.text
    user_data = {"car_brand": search_brand}  # Сохраняем название марки в данных пользователя
    await state.update_data(user_data=user_data)  # Обновляем данные пользователя в состоянии

    if search_brand == "⌨ Введите свой бренд":
        await message.answer("Пожалуйста, введите название марки своего автомобиля:")
    else:
        models = await recognize_car_model(message, search_brand)

        if not models:
            await message.answer("Марка не найдена, попробуйте еще раз")
        else:
            model_names = [model['name'] for model in models]
            builder = create_keyboard(model_names)
            await message.answer("Выберите модель автомобиля из списка:", reply_markup=builder.as_markup(resize_keyboard=True, row_width=2))

            response = f"Модели автомобилей марки '{search_brand}':"
            await message.answer(response, reply_markup=builder)
            await state.set_state(User.STATE_CAR_MODEL)


@router.message(User.STATE_CAR_MODEL)
async def get_car_model(self, message, state):
    user_data = await state.get_data()
    car_brand = user_data.get("car_brand", "")

    user_data["car_model"] = message.text  # Сохраняем выбранную модель в данных пользователя
    await state.update_data(user_data=user_data)  # Обновляем данные пользователя в состоянии

    image_path = ImageDirectory.auto_car_year
    with open(image_path, "rb") as image:
        self.m = await message.answer_photo(image, caption="Какой год выпуска у автомобиля? (напишите)")

    await state.set_state(User.STATE_CAR_YEAR)  # Переключаемся на следующий шаг


@router.message(User.STATE_CAR_YEAR)
async def get_car_year(self, message, state):
    user_data = await state.get_data()

    if await validate_year(message.text):
        user_data["car_year"] = message.text
        keyboard = create_keyboard(dict_car_body_types)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_body_type
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Отлично! Какой тип кузова у автомобиля?",
                                                reply_markup=keyboard)
        # self.m = await message.answer("Отлично! Какой тип кузова у автомобиля?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_BODY_TYPE)
    else:
        self.m = await message.answer("Пожалуйста, введите год в формате YYYY (например, 1990 или 2024)")
        await state.set_state(User.STATE_CAR_YEAR)


@router.message(User.STATE_CAR_BODY_TYPE)
async def get_car_body_type(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_body_types):
        user_data["car_body_type"] = message.text
        keyboard = create_keyboard(dict_car_engine_types)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_engine_type
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Отлично! Какой тип двигателя у автомобиля?",
                                                reply_markup=keyboard)
        # self.m = await message.answer("Отлично! Какой тип двигателя у автомобиля?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_ENGINE_TYPE)
    else:
        keyboard = create_keyboard(dict_car_body_types)
        self.m = await message.answer("Пожалуйста, выберите корректный тип кузова.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_BODY_TYPE)


@router.message(User.STATE_CAR_ENGINE_TYPE)
async def get_car_engine_type(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_engine_types):
        user_data["car_engine_type"] = message.text
        # Добавляем кнопки на основе словаря
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_engine_volume
        with open(image_path, "rb") as image:
            self.m = self.m = await message.answer_photo(image,
                                                         caption="Хорошо! Какой объем двигателя у автомобиля (л.)? (напишите через точку: например 1.6)")
        # self.m = await message.answer("Хорошо! Какой объем двигателя у автомобиля (л.)? (напишите через точку: например 1.6)")
        await state.set_state(User.STATE_CAR_ENGINE_VOLUME)
    else:
        keyboard = create_keyboard(dict_car_engine_types)
        self.m = await message.answer("Пожалуйста, выберите корректный тип двигателя.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_ENGINE_TYPE)


@router.message(User.STATE_CAR_ENGINE_VOLUME)
async def get_car_engine_volume(self, message, state):
    user_data = await state.get_data()
    try:
        if "," in message.text:
            message.text = message.text.replace(',', '.')
        message.text = float(message.text)

        if await validate_engine_volume(message.text) and 0.2 <= message.text <= 10.0:
            user_data["car_engine_volume"] = message.text

            # Добавляем кнопки на основе словаря

            await state.update_data(user_data=user_data)
            image_path = ImageDirectory.auto_car_power
            with open(image_path, "rb") as image:
                self.m = await message.answer_photo(image,
                                                    caption="Отлично! Укажите мощность двигателя автомобиля от 50 до 1000 (л.с.). (напишите)")
            # self.m = await message.answer("Отлично! Укажите мощность двигателя автомобиля от 50 до 1000 (л.с.). (напишите)")
            await state.set_state(User.STATE_CAR_POWER)
        else:
            await message.answer(
                "Пожалуйста, корректный объем двигателя (в пределах от 0.2 до 10.0 литров) через точку или целым числом(!).")
            await state.set_state(User.STATE_CAR_ENGINE_VOLUME)


    except ValueError:
        # Если не удалось преобразовать введенный текст в число
        self.m = await message.answer(
            "Пожалуйста, корректный объем двигателя (в пределах от 0.2 до 10.0 литров) через точку или целым числом(!).")
        await state.set_state(User.STATE_CAR_ENGINE_VOLUME)


@router.message(User.STATE_CAR_POWER)
async def get_car_power(self, message, state):
    user_data = await state.get_data()
    if await validate_car_power(message.text):
        user_data["car_power"] = message.text
        keyboard = create_keyboard(dict_car_transmission_types)

        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_transmission_type
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image,
                                                caption="Отлично! Какой тип коробки передач используется в автомобиле?",
                                                reply_markup=keyboard)
        # await message.answer("Отлично! Какой тип коробки передач используется в автомобиле?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_TRANSMISSION_TYPE)
    else:
        self.m = await message.answer(
            "Пожалуйста, введите корректную мощность двигателя (в пределах от 50 до 1000 л.с.).")
        await state.set_state(User.STATE_CAR_POWER)


@router.message(User.STATE_CAR_TRANSMISSION_TYPE)
async def get_car_transmission_type(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_transmission_types):
        user_data["car_transmission_type"] = message.text
        keyboard = create_keyboard(dict_car_colors)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_color
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Какого цвета автомобиль?", reply_markup=keyboard)
        # self.m = await message.answer("Какого цвета автомобиль?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_COLOR)
    else:
        keyboard = create_keyboard(dict_car_transmission_types)
        self.m = await message.answer("Пожалуйста, выберите корректный тип трансмиссии.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_TRANSMISSION_TYPE)


@router.message(User.STATE_CAR_COLOR)
async def get_car_color(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_colors):
        user_data["car_color"] = message.text
        keyboard = create_keyboard(dict_car_mileages)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_mileage
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image,
                                                caption="Каков пробег автомобиля(км.)? (если новый, выберите 'Новый')",
                                                reply_markup=keyboard)
        # self.m = await message.answer("Каков пробег автомобиля(км.)? (если новый, выберите 'Новый')", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_MILEAGE)
    else:
        keyboard = create_keyboard(dict_car_colors)
        self.m = await message.answer("Пожалуйста, выберите корректный цвет автомобиля.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_COLOR)


@router.message(User.STATE_CAR_MILEAGE)
async def get_car_mileage(self, message, state):
    user_data = await state.get_data()
    if await validate_car_mileage(message.text):
        user_data["car_mileage"] = message.text
        keyboard = create_keyboard(dict_car_document_statuses)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_document_status
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Каков статус документов у автомобиля ?",
                                                reply_markup=keyboard)
        # self.m = await message.answer("Каков статус документов у автомобиля ?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_DOCUMENT_STATUS)
    else:
        keyboard = create_keyboard(dict_car_mileages)
        self.m = await message.answer("Пожалуйста, введите корректное значение пробега.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_MILEAGE)


@router.message(User.STATE_CAR_DOCUMENT_STATUS)
async def get_car_document_status(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_document_statuses):

        user_data["car_document_status"] = message.text
        keyboard = create_keyboard(dict_car_owners)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_owners
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Сколько владельцев у автомобиля?",
                                                reply_markup=keyboard)
        # self.m = await message.answer("Сколько владельцев у автомобиля?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_OWNERS)
    else:
        keyboard = create_keyboard(dict_car_document_statuses)
        self.m = await message.answer("Пожалуйста, выберите корректный статус документов автомобиля.",
                                      reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_DOCUMENT_STATUS)


@router.message(User.STATE_CAR_OWNERS)
async def get_car_owners(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_owners):
        user_data["car_owners"] = message.text
        keyboard = create_keyboard(dict_car_customs_cleared)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_customs_cleared
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Растаможен ли автомобиль?", reply_markup=keyboard)
        # self.m = await message.answer("Растаможен ли автомобиль?", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_CUSTOMS_CLEARED)
    else:
        keyboard = create_keyboard(dict_car_owners)
        self.m = await message.answer("Пожалуйста, выберите корректное количество владельцев автомобиля.",
                                      reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_OWNERS)


@router.message(User.STATE_CAR_CUSTOMS_CLEARED)
async def get_car_customs_cleared(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_customs_cleared):
        user_data["car_customs_cleared"] = message.text
        keyboard = create_keyboard(dict_car_conditions)
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_condition
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Выберите состояние автомобиля:", reply_markup=keyboard)
        # self.m = await message.answer("Выберите состояние автомобиля:", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_CONDITION)
    else:
        keyboard = create_keyboard(dict_car_customs_cleared)
        self.m = await message.answer("Пожалуйста, выберите корректный статус растаможки автомобиля.",
                                      reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_CUSTOMS_CLEARED)


@router.message(User.STATE_CAR_CONDITION)
async def get_car_condition(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_car_conditions):
        user_data["car_condition"] = message.text
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_description
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Описание автомобиля. (напишите до 350 символов)")
        # self.m = await message.answer("Описание автомобиля. (напишите)")
        await state.set_state(User.STATE_CAR_DESCRIPTION)
    else:
        keyboard = create_keyboard(dict_car_conditions)
        self.m = await message.answer("Пожалуйста, выберите корректное состояние автомобиля.", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_CONDITION)


@router.message(User.STATE_CAR_DESCRIPTION)
async def get_car_description(self, message, state):
    user_data = await state.get_data()
    if await validate_length_text(message):
        if await validate_car_description(message.text):
            user_data["car_description"] = message.text
            keyboard = create_keyboard(dict_currency)
            await state.update_data(user_data=user_data)
            image_path = ImageDirectory.auto_car_currency
            with open(image_path, "rb") as image:
                self.m = await message.answer_photo(image, caption="Выберите валюту:", reply_markup=keyboard)
            # self.m = await message.answer("Выберите валюту:", reply_markup=keyboard)
            await state.set_state(User.STATE_SELECT_CURRENCY)
        else:
            self.m = await message.answer("Пожалуйста, введите корректное описание.")
            await state.set_state(User.STATE_CAR_DESCRIPTION)
    else:
        self.m = await message.answer("Ваше описание сильно большое. Напишите до ~350 символов:")
        await state.set_state(User.STATE_CAR_DESCRIPTION)


@router.message(User.STATE_SELECT_CURRENCY)
async def select_currency(self, message, state):
    user_data = await state.get_data()
    if await validate_button_input(message.text, dict_currency):
        user_data["currency"] = message.text
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_price
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Цена автомобиля?")
        # self.m = await message.answer("Цена автомобиля?")
        await state.set_state(User.STATE_CAR_PRICE)
    else:
        keyboard = create_keyboard(dict_currency)
        self.m = await message.answer("Пожалуйста, выберите корректную валюту.", reply_markup=keyboard)
        await state.set_state(User.STATE_SELECT_CURRENCY)


@router.message(User.STATE_CAR_PRICE)
async def get_car_price(self, message, state):
    user_data = await state.get_data()
    if await validate_car_price(message.text):
        user_data["car_price"] = message.text
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_car_location
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image,
                                                caption="Прекрасно! Где находится автомобиль? Город/пункт. (напишите)")
        # self.m = await message.answer("Прекрасно! Где находится автомобиль? Город/пункт. (напишите)")
        await state.set_state(User.STATE_CAR_LOCATION)
    else:
        self.m = await message.answer("Пожалуйста, введите корректную цену.")
        await state.set_state(User.STATE_CAR_PRICE)


@router.message(User.STATE_CAR_LOCATION)
async def get_car_location(self, message, state):
    user_data = await state.get_data()
    if await validate_car_location(message.text):
        user_data["car_location"] = message.text
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_seller_name
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image, caption="Прекрасно! Укажите имя продавца. (напишите)")
        # self.m = await message.answer("Прекрасно! Укажите имя продавца. (напишите)")
        await state.set_state(User.STATE_SELLER_NAME)
    else:
        self.m = await message.answer("Пожалуйста, введите корректные данные.")
        await state.set_state(User.STATE_CAR_LOCATION)


@router.message(User.STATE_SELLER_NAME)
async def get_seller_name(self, message, state):
    user_data = await state.get_data()
    if await validate_name(message.text) is True:
        user_data["seller_name"] = message.text
        await state.update_data(user_data=user_data)
        image_path = ImageDirectory.auto_seller_phone
        with open(image_path, "rb") as image:
            self.m = await message.answer_photo(image,
                                                caption="Отлично! Какой телефонный номер у продавца? (напишите в формате +7XXXNNNXXNN или 8XXXNNNXXNN)")
        await state.set_state(User.STATE_SELLER_PHONE)
    else:
        self.m = await message.answer("Пожалуйста, введите корректное имя.")
        await state.set_state(User.STATE_SELLER_NAME)


@router.message(User.STATE_SELLER_PHONE)
async def get_seller_phone(self, message, state):
    user_data = await state.get_data()
    if await validate_phone_number(message.text) is True:
        message.text = '+7' + message.text[1:] if message.text.startswith('8') else message.text
        user_data["seller_phone"] = message.text
        await state.update_data(user_data=user_data)
        if await validate_final_length(message, state, user_data):
            image_path = ImageDirectory.auto_car_photos
            with open(image_path, "rb") as image:
                self.m = await message.answer_photo(image, caption="Добавьте фотографии авто до 10 штук (За один раз!)")
            await state.set_state(User.STATE_CAR_PHOTO)
        else:
            await message.reply(
                f"Ваше сообщение получилось сильно большим! \nПерезагрузите бота и напишите объявление заново.")

    else:
        self.m = await message.answer("Пожалуйста, введите корректный номер в формате +7XXXNNNXXNN.")
        await state.set_state(User.STATE_SELLER_PHONE)


@router.message(User.STATE_CAR_PHOTO)
@router.message(F.media_group_id)
async def handle_photos(event: types.Message, state: FSMContext, album: list[Message]):
    user_data = await state.get_data()
    if 'sent_photos' not in user_data:
        user_data['sent_photos'] = []

    new_id = str(uuid.uuid4().int)[:6]

    caption = (
        f"💬<b>Телеграм:</b> <span class='tg-spoiler'>{event.from_user.username if event.from_user.username is not None else 'по номеру телефона'}</span>\n\n"
        f"<b>ID объявления: #{new_id}</b>"
    )

    for message in album:
        # Проверяем, есть ли атрибут photo у текущего сообщения
        if message.photo:
            # Берем последний элемент списка photo, который обычно является наивысшим качеством
            top_photo = message.photo[-1]
            # Получаем file_id фотографии и добавляем его в список sent_photos
            user_data['sent_photos'].append(
                InputMediaPhoto(media=top_photo.file_id, caption=None, parse_mode="HTML"))

    user_data['sent_photos'][0].caption = caption

    await state.update_data(user_data)

    builder = ReplyKeyboardBuilder([[types.KeyboardButton(text="Следущий шаг"), ]])
    if album:
        count_photos = len(album)
        await event.reply(f'{count_photos} Фото добавлены', reply_markup=builder.as_markup(resize_keyboard=True))

    await state.set_state(User.STATE_PREVIEW_ADVERTISMENT)


@router.message(F.text == "Отправить в канал")
async def send_advertisement(message: types.Message, state):
    user_data = await state.get_data()
    await add_data_to_excel(message, state)
    user_id = message.from_user.id
    await bot.send_media_group(chat_id=CHANNEL_ID, media=user_data['sent_photos'], disable_notification=True)
    builder = create_keyboard(['Добавить ещё объявление', 'Ускорить продажу'])
    await bot.send_message(user_id, "Объявление отправлено в канал!",
                           reply_markup=builder.as_markup(resize_keyboard=True))
    await state.clear()


# @router.message(F.text == "Отменить и заполнить заново")
# async def fill_again(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     builder = create_keyboard(list(dict_car_brands_and_models.keys()))
#     image_path = ImageDirectory.auto_car_brand
#     with open(image_path, "rb"):
#         await message.answer_photo(photo=types.FSInputFile(image_path), caption="Выберите бренд автомобиля:",
#                                    reply_markup=builder.as_markup(resize_keyboard=True, row_width=2))
#     user_data['sent_photos'].clear()
#     await state.clear()
#     await state.set_state(User.STATE_CAR_BRAND)


@router.message(F.text == "Ускорить продажу")
async def promotion(message: types.Message):
    builder = create_keyboard(['Перезагрузить бота'])
    await message.reply("Чтобы купить закреп напишите @selbie_adv",
                        reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(User.STATE_PREVIEW_ADVERTISMENT)
async def preview_advertisement(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print('1', user_data['sent_photos'])
    await bot.send_media_group(chat_id=message.chat.id, media=user_data['sent_photos'])

    builder = ReplyKeyboardBuilder([[
        KeyboardButton(text="Отправить в канал"),
        KeyboardButton(text="Отменить и заполнить заново")
    ]])

    await message.reply(
        "Так будет выглядеть ваше объявление. Вы можете либо разместить либо отменить и заполнить заново.",
        reply_markup=builder.as_markup(resize_keyboard=True))

    # db_fix.clear()


async def add_data_to_excel(message, state):
    user_data = await state.get_data()
    file_path = 'db.xlsx'
    row_data = [
        # db_fix.get('new_id'),
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        # user_data.get('car_brand', ''),
        message.from_user.username if message.from_user.username is not None else 'по номеру телефона',
    ]

    # Проверяем, существует ли файл Excel
    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
    else:
        workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Проверяем, нужно ли добавить заголовки
    if sheet.max_row == 1:
        headers = [
            'ID', 'Дата', 'Бренд', 'Модель', 'Год', 'Пробег (км)', 'Тип трансмиссии',
            'Тип кузова', 'Тип двигателя', 'Объем двигателя (л)', 'Мощность (л.с.)',
            'Цвет', 'Статус документа', 'Количество владельцев', 'Растаможен',
            'Состояние', 'Дополнительное описание', 'Цена', 'Валюта',
            'Местоположение', 'Имя продавца', 'Телефон продавца', 'Телеграм'
        ]
        sheet.append(headers)

    sheet.append(row_data)
    workbook.save(file_path)


# end support


# старт бота
if __name__ == '__main__':
    asyncio.run(main())
