import asyncio
import json
import random
import requests
import datetime
import uuid
# import openpyxl

from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.client.session import aiohttp
from aiogram.types import KeyboardButton, InputMediaPhoto, Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hlink
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
dict_currency2 = dicts.get("dict_currency2", {})
dict_car_conditions = dicts.get("dict_car_conditions", {})
dict_car_mileages = dicts.get("dict_car_mileages", {})
dict_edit_buttons = dicts.get("dict_edit_buttons", {})
dict_realty_deal = dicts.get('dict_realty_deal', {})
dict_realty_type = dicts.get('dict_realty_type', {})
dict_realty_commercial_type = dicts.get('dict_realty_commercial_type', {})
dict_job_categories = dicts.get('dict_job_categories', {})

async def send_api(message, state):
    user_data = await state.get_data()
    field_mapping = {
        'car': {
            'contact_name': 'car_name',
            'contact_phone': 'car_phone',
            'currency': 'car_currency',
            'price': 'car_price',
            'description': 'car_description',
        },
        'realty': {
            'contact_name': 'realty_name',
            'contact_phone': 'realty_phone',
            'currency': 'realty_currency',
            'price': 'realty_price',
            'description': 'realty_description',

        },
        'job': {
            'contact_name': 'job_name',
            'contact_phone': 'job_phone',
            'currency': 'job_currency',
            'price': 'job_price',
            'description': 'job_description',

        },
    }
    # Получаем категорию объявления
    category = user_data.get('category')
    if category not in field_mapping:
        print("Неподдерживаемая категория:", category)
        return

    # Получаем сопоставление полей для выбранной категории
    field_mapping_category = field_mapping[category]

    # Формируем данные для отправки
    data = {
        'user_id': user_data.get('user_id', ''),
        'username_tg': message.from_user.username if message.from_user.username is not None else 'по номеру телефона',
        'ad_id': user_data.get('ad_id', ''),
        'category': category,
    }

    # Обрабатываем фотографии, если они есть
    photo_urls = []
    for photo_data in user_data.get('sent_photos', []):
        if isinstance(photo_data, InputMediaPhoto):
            file_id = photo_data.media
            file_info_response = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}')
            file_info = file_info_response.json()
            file_path = file_info['result']['file_path']
            photo_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}'
            photo_urls.append(photo_url)
    data['sent_photos'] = ','.join(photo_urls)

    if user_data['category'] == 'car':
        title = f"{user_data['car_brand']} - {user_data['car_model']}, {user_data['car_year']}, {user_data['car_mileage']}"
    elif user_data['category'] == 'realty':
        generate_realty_title(user_data)  # Обновление user_data['title']
        title = user_data['title']
    elif user_data['category'] == 'job':
        title = user_data['job_title']

    # Добавляем заголовок в данные
    data['title'] = title

    for key, value in user_data.items():
        if isinstance(value, set):
            value = list(value)
        if isinstance(value, (list, set)):
            data[key] = ' '.join(str(item) for item in value)
        else:
            data[key] = str(value)

    for key, value in field_mapping_category.items():
        user_data_value = user_data.get(value, '')

        # Если значение - список, объединяем его в строку
        if isinstance(user_data_value, list):
            user_data_value = ' '.join(user_data_value)
            print(f"user_data[{value}] после объединения: {user_data_value}")

        data[key] = user_data_value

    try:
        print('data', data)
        endpoint = f'http://127.0.0.1:8000/api/{category}_ad/'
        response = requests.post(endpoint, data=data)

        if response.status_code == 200 or response.status_code == 201:
            print("Успешно получили данные пользователя с сервера Django!")

    except requests.RequestException as e:
        print("Ошибка при отправке запроса на сервер Django:", e)


# Создание клавиатуры
def create_keyboard(button_texts):
    buttons = [KeyboardButton(text=text) for text in button_texts]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons).adjust(2)
    return builder


def create_keyboard_inline(buttons):
    builder = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return builder


def generate_realty_title(user_data):
    title_parts = []

    title_parts.append(user_data['realty_deal'])
    print("After realty_deal:", title_parts)

    # Добавляем количество комнат, если оно задано
    if user_data['realty_rooms'] is not None:
        title_parts.append(f"{user_data['realty_rooms']} комнат")
        print("After realty_rooms:", title_parts)

    # Добавляем тип недвижимости
    title_parts.append(user_data['realty_type'])
    print("After realty_type:", title_parts)

    if 'realty_commercial_type' in user_data:
        title_parts.append(user_data['realty_commercial_type'])
        print("After realty_commercial_type:", title_parts)

    # Добавляем площадь, если она задана
    if user_data['realty_square'] is not None:
        if "Земельный участок" in user_data['realty_type']:
            title_parts.append(f"{user_data['realty_square']} сот")
        else:
            title_parts.append(f"{user_data['realty_square']} м2")
        print("After realty_square:", title_parts)

    # Добавляем информацию о этаже, если она задана
    if user_data['realty_floor'] is not None and user_data['realty_floors_total'] is not None:
        title_parts.append(f"{user_data['realty_floor']} / {user_data['realty_floors_total']} этаж")
    elif user_data['realty_floor'] is not None:
        title_parts.append(f"{user_data['realty_floor']} этаж")
    elif user_data['realty_floors_total'] is not None:
        title_parts.append(f"{user_data['realty_floors_total']} этажей")
    print("After floors:", title_parts)

    # Собираем тайтл из всех составляющих, исключая None значения
    user_data['title'] = ", ".join(part for part in title_parts if part)
    print("Final title:", user_data['title'])


async def add_message_id(state, message_id):
    user_data = await state.get_data()
    if 'msg_ids' not in user_data:
        user_data['msg_ids'] = []
    if message_id not in user_data['msg_ids']:
        user_data['msg_ids'].append(message_id)
    await state.update_data(user_data)


async def send_photo_with_caption(message, state, image_path, caption, builder=None):
    user_data = await state.get_data()
    reply_markup = None
    if builder:
        reply_markup = builder.as_markup(resize_keyboard=True)
    sent_message = await message.answer_photo(photo=types.FSInputFile(image_path), caption=caption,
                                              reply_markup=reply_markup)
    # await add_message_id(state, sent_message.message_id)  # добавляем айдишник доп функцией
    return sent_message


async def delete_saved_messages(message, state):
    user_data = await state.get_data()
    chat_id = message.chat.id
    if 'msg_ids' not in user_data:
        user_data['msg_ids'] = []
    msg_ids_copy = user_data['msg_ids'].copy()

    for message_id in msg_ids_copy:
        try:
            user_data['msg_ids'].remove(message_id)
            await message.bot.delete_message(chat_id, message_id)
            # await state.update_data(user_data)
        except Exception as e:
            print('Ошибка:', e)
        #     print(user_data)
        #     print(message_id)

        #     print(f"Error deleting message")
        #     # Обработка ошибки, например, удаление сообщения из списка msg_ids
        #     user_data['msg_ids'].remove(message_id)
    await state.update_data(user_data)


async def recognize_car_model(message, brand_name):
    models = []
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
            if 'name' in inner_item and fuzz.token_sort_ratio(brand_name.lower(), inner_item['name'].lower()) >= 75 and \
                    inner_item['name'] not in similar_brands:
                similar_brands.append(inner_item['name'])
            # Поиск похожих кириллических брендов
            elif 'cyrillic-name' in inner_item and fuzz.token_sort_ratio(brand_name.lower(),
                                                                         inner_item['cyrillic-name'].lower()) >= 75 \
                    and inner_item['name'] not in similar_brands:
                similar_brands.append(inner_item['name'])

        if similar_brands:
            response_message = "Похожие бренды:\n" + "\n".join(similar_brands)
            await message.answer(response_message)

    return models


# Команды
@router.message(F.text == "Перезагрузить бота")
@router.message(F.text == "Добавить ещё объявление")
@router.message(F.text == "Отменить и заполнить заново")
@router.message(Cmd.STATE_SUPPORT_END)
@router.message(Command("restart"))
async def restart(message: types.Message, state: FSMContext):
    await delete_saved_messages(message, state)
    await state.clear()
    msg = await message.answer("Бот перезапущен.")
    await add_message_id(state, msg.message_id)
    await start(message, state)

@router.message(Command("my_ads"))
async def my_ads(message: types.Message, state: FSMContext):
    username = f'user_{message.from_user.id}'
    url = f'http://127.0.0.1:8000/api/myads/{username}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status in [200, 201]:
                data = await response.json()
                # buttons = [
                #     [types.InlineKeyboardButton(text='Кнопка 1', callback_data='Кнопка 1')],
                # ]
                # builder = create_keyboard_inline(buttons)
                # await message.answer(f"{data}", reply_markup=builder)
                await message.answer(f"На данный момент просмотр объявлений доступен на сайте. Перейдите в /my_profile чтобы получить ссылку для входа на сайт. \n\nПерейдите в ваш профиль в раздел Мои объявления")

            else:
                error_message = await response.text()
                await message.answer(f"Error: {error_message}")

@router.message(Command("my_profile"))
async def my_profile(message: types.Message, state: FSMContext):
    await delete_saved_messages(message, state)
    username = f'user_{message.from_user.id}'
    print(username)
    url = f'http://127.0.0.1:8000/api/check_user/{username}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status in [200, 201]:
                data = await response.json()
                if data['exists']:
                    gen_link_url = 'http://127.0.0.1:8000/api/generate_link/'
                    async with session.post(gen_link_url, json={'username': username}) as gen_link_response:
                        if gen_link_response.status in [200, 201]:
                            gen_link_data = await gen_link_response.json()
                            print('Пользователь получил ссылку!')
                            builder = create_keyboard(['Перезагрузить бота'])
                            msg = await message.answer(f"Ваша ссылка для входа: {gen_link_data['link']}",
                                                       reply_markup=builder.as_markup(resize_keyboard=True))
                            await add_message_id(state, msg.message_id)
                        else:
                            print('Ошибка при генерации ссылки!')
                            msg = await message.answer("Ошибка при генерации ссылки. Попробуйте позже.")
                            await add_message_id(state, msg.message_id)
                else:
                    print('Пользователь не получил ссылку!')
                    msg = await message.answer("У вас пока нет размещенных объявлений. Нажмите /restart для перезапуска бота")
                    await add_message_id(state, msg.message_id)

@router.message(Command("support"))
async def support(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    secret_number = str(random.randint(100, 999))

    await message.answer(f"Нашли баг? Давайте отправим сообщение разработчикам! "
                         f"Но перед этим введите проверку. Докажите что вы не робот. Напишите число {secret_number}:")
    user_data['secret_number'] = secret_number
    await state.update_data(user_data)
    await state.set_state(Cmd.STATE_SUPPORT_VALIDATION)


@router.message(Cmd.STATE_SUPPORT_VALIDATION)
async def support_validation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    secret_number = user_data['secret_number']
    if message.text.isdigit() and message.text == secret_number:
        await message.reply(f"Проверка пройдена успешно!")
        await asyncio.sleep(1)
        await message.answer(f"Опишите техническую проблему в деталях для разработчиков: ")
        await state.set_state(Cmd.STATE_SUPPORT_MESSAGE)
    else:
        await message.answer(f"Попробуйте ещё раз!")
        await asyncio.sleep(1)
        await support(message, state)


@router.message(Cmd.STATE_SUPPORT_MESSAGE)
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
    await state.set_state(Cmd.STATE_SUPPORT_END)


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)
    buttons = [
        [types.InlineKeyboardButton(text='🚗 Авто', callback_data='Авто')],
        [types.InlineKeyboardButton(text='🏢 Недвижимость', callback_data='Недвижимость')],
        [types.InlineKeyboardButton(text='💼 Работа', callback_data='Работа')],
    ]
    builder = create_keyboard_inline(buttons)
    msg = await message.answer(
        f'/start - Запуск бота\n'
        f'/restart - Перезагрузка бота\n'
        f'/my_ads - Просмотр объявлений\n'
        f'/my_profile - Мой профиль на selbie.ru \n'
        f'/support - Написать в техподдержку')
    await add_message_id(state, msg.message_id)
    msg = await message.answer("Привет! Давай разместим объявление! \n Выбери категорию:", reply_markup=builder)
    await add_message_id(state, msg.message_id)
    await state.update_data(user_data)


@router.callback_query(F.data == "Авто")
@router.message(Car.STATE_START_CARBOT)
async def car_bot_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await delete_saved_messages(callback_query.message, state)
    builder = create_keyboard(dict_start_brands)
    image_path = ImageDirectory.auto_car_brand
    msg = await send_photo_with_caption(callback_query.message, state, image_path, "Выберите бренд автомобиля:",
                                        builder)
    await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
    await state.update_data(category='car')
    await state.set_state(Car.STATE_CAR_BRAND)


@router.callback_query(F.data == "Недвижимость")
@router.message(Realty.STATE_START_REALTY)
async def realty_bot_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    builder = create_keyboard(dict_realty_deal).adjust(1)
    image_path = ImageDirectory.realty_deal_type
    msg = await send_photo_with_caption(callback_query.message, state, image_path, "Укажи тип сделки с недвижимостью:",
                                        builder)
    await add_message_id(state, msg.message_id)
    await state.update_data(category='realty')
    await state.set_state(Realty.STATE_REALTY_DEAL)


@router.callback_query(F.data == "Работа")
@router.message(Job.STATE_START_JOB)
async def hr_bot_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await delete_saved_messages(callback_query.message, state)

    image_path = ImageDirectory.job_category
    builder = create_keyboard(dict_job_categories).adjust(2)

    # await callback_query.message.answer('Напиши название своей вакансии')
    msg = await send_photo_with_caption(callback_query.message, state, image_path,
                                        f"{callback_query.from_user.first_name}, выберите категорию вакансии", builder)
    await add_message_id(state, msg.message_id)

    await state.update_data(category='job'),
    await state.set_state(Job.STATE_JOB_CATEGORY)


@router.message(Car.STATE_CAR_BRAND)
async def get_car_brand(message, state):
    user_data = await state.get_data()
    search_brand = message.text
    await state.update_data(car_brand=search_brand)  # Обновляем данные пользователя в состоянии
    # Удаление сохраненных сообщений

    await delete_saved_messages(message, state)

    if search_brand == "⌨ Введите свой бренд":
        msg = await message.answer("Пожалуйста, введите название марки своего автомобиля:")
        await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
    else:
        models = await recognize_car_model(message, search_brand)
        if not models:
            msg = await message.answer("Марка не найдена, попробуйте еще раз")
            await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
            await state.set_state(Car.STATE_CAR_BRAND)
        else:
            model_names = [model['name'] for model in models]
            builder = create_keyboard(model_names)
            image_path = ImageDirectory.auto_car_model
            msg = await send_photo_with_caption(message, state, image_path, "Выберите модель автомобиля из списка:")
            await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
            msg = await message.answer(f"Модели автомобилей марки '{search_brand}':",
                                       reply_markup=builder.as_markup(resize_keyboard=True))
            await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
            await state.set_state(Car.STATE_CAR_MODEL)


@router.message(Car.STATE_CAR_MODEL)
async def get_car_model(message, state):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)

    await state.update_data(car_model=message.text)
    image_path = ImageDirectory.auto_car_year
    msg = await send_photo_with_caption(message, state, image_path, "Какой год выпуска у автомобиля? (⌨ напишите)")
    await add_message_id(state, msg.message_id)
    await state.set_state(Ads.STATE_PHOTO)



@router.message(Ads.STATE_PHOTO)
@router.message(F.media_group_id)
async def handle_photos(message: types.Message, state: FSMContext, album: list[Message]):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)
    print('19', user_data)
    if 'sent_photos' not in user_data:
        user_data['sent_photos'] = []
    ad_id = str(uuid.uuid4().int)[:6]
    if 'ad_id' not in user_data:
        user_data['ad_id'] = ad_id
    if user_data['category'] == 'car':
        caption = (
            f"🛞 <b>#{user_data['car_brand']}-{user_data['car_model']}</b>\n\n"
            # f"   <b>-Год:</b> {user_data['car_year']}\n"
            # f"   <b>-Пробег (км.):</b> {user_data['car_mileage']}\n"
            # f"   <b>-Тип КПП:</b> {user_data['car_transmission_type']}\n"
            # f"   <b>-Кузов:</b> {user_data['car_body_type']}\n"
            # f"   <b>-Тип двигателя:</b> {user_data['car_engine_type']}\n"
            # f"   <b>-Объем двигателя (л.):</b> {user_data['car_engine_volume']}\n"
            # f"   <b>-Мощность (л.с.):</b> {user_data['car_power']}\n"
            # f"   <b>-Цвет:</b> {user_data['car_color']}\n"
            # f"   <b>-Статус документов:</b> {user_data['car_document_status']}\n"
            # f"   <b>-Количество владельцев:</b> {user_data['car_owners']}\n"
            # f"   <b>-Растаможка:</b> {'Да' if user_data['car_customs_cleared'] else 'Нет'}\n"
            # f"   <b>-Состояние:</b> {user_data['car_condition']}\n\n"
            # f"ℹ️<b>Дополнительная информация:</b> {user_data['car_description']}\n\n"
            # f"🔥<b>Цена:</b> {user_data['car_price']} {user_data['car_currency']}\n\n"
            # f"📍<b>Местоположение:</b> {user_data['car_location']}\n"
            # f"👤<b>Продавец:</b> <span class='tg-spoiler'> {user_data['car_name']} </span>\n"
            # f"📲<b>Телефон продавца:</b> <span class='tg-spoiler'>{user_data['car_phone']} </span>\n"
            f"💬<b>Телеграм:</b> <span class='tg-spoiler'>@{message.from_user.username if message.from_user.username is not None else 'по номеру телефона'}</span>\n\n"
            f" {hlink('Selbie Auto. Рынок тачек в ДНР', 'https://t.me/selbieauto')} | {hlink('Разместить авто', 'https://t.me/selbie_bot')} \n\n"
            f"<b>ID объявления: #{user_data['ad_id']}</b>"
        )
    elif user_data['category'] == 'realty':
        generate_realty_title(user_data)  # Обновление user_data['title']
        # Добавляем информацию о типе сделки и типе недвижимости
        caption = (
                f"<b> 🏘 {user_data['title']} </b>\n\n"
                f"<b>▪Тип недвижимости:</b> {user_data.get('realty_commercial_type', user_data['realty_type'])} \n" +
                (f"<b>▪️Комнат:</b> {user_data['realty_rooms']}\n" if user_data['realty_rooms'] not in [None,
                                                                                                        "Пропустить"] else '') +
                (f"<b>▪️Этаж:</b> {user_data['realty_floor']} из {user_data['realty_floors_total']} \n"
                 if user_data['realty_floor'] is not None and user_data['realty_floors_total'] is not None else '') +
                (f"<b>▪️Этажей:</b> {user_data['realty_floors_total']} \n"
                 if user_data['realty_floors_total'] is not None and user_data['realty_floor'] is None else '') +
                (f"<b>▪️Этаж:</b> {user_data['realty_floor']} \n"
                 if user_data['realty_floor'] is not None and user_data['realty_floors_total'] is None else '') +
                f"<b>▪️Площадь:</b> {user_data['realty_square']} {'сот' if 'Земельный участок' in user_data['realty_type'] else 'м2'}\n\n" +
                f"<b>✅Описание:✅</b>\n {user_data['realty_description']}\n\n" +
                f"🔥<b>Цена:</b> {user_data['realty_price']} {user_data['realty_currency']} 🔥\n\n"
                f"<b>📍Местонахождение:</b> {user_data['realty_location']}\n\n" +
                f"<b>📬Контакты:</b>\n" +
                f"👤<b>Имя:</b> <span class='tg-spoiler'>{user_data['realty_name']}</span>\n" +
                f"📲<b>Телефон:</b> <span class='tg-spoiler'>{user_data['realty_phone']}</span>\n" +
                f"💬<b>Телеграм:</b> <span class='tg-spoiler'>@{message.from_user.username if message.from_user.username is not None else 'по номеру телефона'}</span>\n\n" +

                f" {hlink('Selbie Realty. Недвижимость в ДНР', 'https://t.me/selbierealty')} | {hlink('Разместить объявление', 'https://t.me/selbie_bot')} \n\n"
                f"<b>ID объявления: #{user_data['ad_id']}</b>"

        )

    elif user_data['category'] == 'job':

        caption = (
                f"‼️ЕСТЬ РАБОТА!‼️\n\n" +
                f"<b> Требуется:</b> {user_data['job_title']}\n\n" +
                f" <b>✅Описание работы:✅</b>\n{user_data['job_description']}\n\n" +
                (f"<b>ЗП: </b>💸💸💸{user_data['job_price']}{user_data['job_currency']}💸💸💸\n\n"
                 if user_data.get('job_price') is not None and user_data.get('job_currency') is not None else '') +
                f"<b>📬Контакты:</b>\n" +
                f"👤<b>Имя:</b> <span class='tg-spoiler'>{user_data['job_name']}</span>\n" +
                f"📲<b>Телефон:</b> <span class='tg-spoiler'>{user_data['job_phone']}</span>\n" +
                f"💬<b>Телеграм:</b> <span class='tg-spoiler'>@{message.from_user.username if message.from_user.username is not None else 'по номеру телефона'}</span>\n\n" +
                f" {hlink('Selbie Work. Есть работа в ДНР', 'https://t.me/selbiejob')} | {hlink('Разместить вакансию', 'https://t.me/selbie_bot')} \n\n"
                f"<b>ID объявления: #{user_data['ad_id']}</b>"
        )

    for message in album:
        if message.photo:
            top_photo = message.photo[-1]
            user_data['sent_photos'].append(
                InputMediaPhoto(media=top_photo.file_id, caption=None, parse_mode="HTML"))

    user_data['sent_photos'][0].caption = caption

    await state.update_data(user_data)

    builder = ReplyKeyboardBuilder([[types.KeyboardButton(text="Следущий шаг"), ]])
    if album:
        count_photos = len(album)
        msg = await message.reply(f'{count_photos} Фото добавлены',
                                  reply_markup=builder.as_markup(resize_keyboard=True))
        await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
    await state.set_state(Ads.STATE_PREVIEW_ADVERTISMENT)


@router.message(F.text == "Отправить в канал")
async def send_advertisement(message: types.Message, state):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)
    print('21', user_data)
    # await add_data_to_excel(message, state)
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    if user_data['category'] == 'car':
        await bot.send_media_group(chat_id=CHANNEL_CAR_ID, media=user_data['sent_photos'], disable_notification=True)
    elif user_data['category'] == 'realty':
        await bot.send_media_group(chat_id=CHANNEL_REALTY_ID, media=user_data['sent_photos'], disable_notification=True)
    elif user_data['category'] == 'job':
        await bot.send_media_group(chat_id=CHANNEL_JOB_ID, media=user_data['sent_photos'], disable_notification=True)
    builder = create_keyboard(['Добавить ещё объявление', 'Ускорить продажу'])
    msg = await bot.send_message(user_id, "Объявление отправлено в канал!",
                                 reply_markup=builder.as_markup(resize_keyboard=True))
    await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией
    await send_api(message, state)
    await state.clear()


@router.message(F.text == "Ускорить продажу")
async def promotion(message: types.Message, state):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)

    builder = create_keyboard(['Перезагрузить бота'])
    msg = await message.reply("Чтобы купить закреп, напишите @selbie_adv",
                              reply_markup=builder.as_markup(resize_keyboard=True))
    await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией


@router.message(Ads.STATE_PREVIEW_ADVERTISMENT)
async def preview_advertisement(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await delete_saved_messages(message, state)

    print('20', user_data)
    await bot.send_media_group(chat_id=message.chat.id, media=user_data['sent_photos'])

    builder = ReplyKeyboardBuilder([[
        KeyboardButton(text="Отправить в канал"),
        KeyboardButton(text="Отменить и заполнить заново")
    ]])

    msg = await message.reply(
        "Так будет выглядеть ваше объявление. Вы можете либо разместить либо отменить и заполнить заново.",
        reply_markup=builder.as_markup(resize_keyboard=True))
    await add_message_id(state, msg.message_id)  # добавляем айдишник доп функцией



# старт бота
if __name__ == '__main__':
    asyncio.run(main())
