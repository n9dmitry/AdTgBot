import telebot
from telebot import types
import openpyxl

TOKEN = '6087732169:AAHABX0K5LHguc-ymnd0Um8UOK8oucvX_gY'

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button_add_ad = types.KeyboardButton('Добавить объявление')
    markup.add(button_add_ad)

    greeting_message = (
        'Привет! Я бот для сбора данных. '
        'Чтобы добавить объявление, нажми на кнопку "Добавить объявление".'
    )

    bot.send_message(message.chat.id, greeting_message, reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == 'Добавить объявление')
def add_ad(message):
    markup = types.ReplyKeyboardMarkup()
    car_brands = ['BMW', 'Mercedes', 'Audi', 'Другая']  # Здесь можно добавить список других марок машин
    for brand in car_brands:
        button_brand = types.KeyboardButton(brand)
        markup.add(button_brand)

    select_brand_message = (
        'Выбери марку машины из списка или выбери "Другая", чтобы ввести марку вручную:'
    )

    bot.send_message(message.chat.id, select_brand_message, reply_markup=markup)
    bot.register_next_step_handler(message, handle_brand)


def handle_brand(message):
    user_data[message.chat.id] = {}  # Создаем пустой словарь для нового пользователя

    brand = message.text
    if brand == 'Другая':
        bot.send_message(message.chat.id, 'Введите марку машины вручную')
        bot.register_next_step_handler(message, handle_custom_brand)
    else:
        user_data[message.chat.id]['brand'] = brand
        bot.send_message(message.chat.id, 'Введите модель машины')
        bot.register_next_step_handler(message, handle_model)


def handle_custom_brand(message):
    custom_brand = message.text
    user_data[message.chat.id]['brand'] = custom_brand

    bot.send_message(message.chat.id, 'Введите модель машины')
    bot.register_next_step_handler(message, handle_model)


def handle_model(message):
    model = message.text
    user_data[message.chat.id]['model'] = model

    ask_body_type(message)

def ask_body_type(message):
    body_type = message.text
    user_data[message.chat.id]['body_type'] = body_type

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['Хэтчбек', 'Сидан', 'Универсал', 'Кроссовер']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите тип кузова:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_engine)


def handle_engine(message):
    engine = message.text
    user_data[message.chat.id]['engine'] = engine

    keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    buttons = ['Бензин', 'Дизель', 'Электро']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите тип двигателя:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_engine_type)


def handle_engine_type(message):
    engine_type = message.text
    user_data[message.chat.id]['engine_type'] = engine_type

    bot.send_message(message.chat.id, 'Введите объем двигателя (куб см)')
    bot.register_next_step_handler(message, handle_engine_capacity)


def handle_engine_capacity(message):
    engine_capacity = message.text
    user_data[message.chat.id]['engine_capacity'] = engine_capacity

    bot.send_message(message.chat.id, 'Введите мощность двигателя (л. сил)')
    bot.register_next_step_handler(message, handle_engine_power)

def handle_engine_power(message):
    engine_power = message.text
    user_data[message.chat.id]['engine_power'] = engine_power

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['Автомат', 'Механика', 'Робот', 'Вариатор']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите тип КПП:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_transmission)


def handle_transmission(message):
    transmission = message.text
    user_data[message.chat.id]['transmission'] = transmission

    bot.send_message(message.chat.id, 'Введите цвет автомобиля')
    bot.register_next_step_handler(message, handle_color)


def handle_color(message):
    color = message.text
    user_data[message.chat.id]['color'] = color

    bot.send_message(message.chat.id, 'Введите пробег автомобиля (в километрах)')
    bot.register_next_step_handler(message, handle_mileage)


def handle_mileage(message):
    mileage = message.text
    user_data[message.chat.id]['mileage'] = mileage

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['Оригинал', 'Дубликат', 'Временные', 'Без документов']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите состояние документов:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_document_condition)


def handle_document_condition(message):
    document_condition = message.text
    user_data[message.chat.id]['document_condition'] = document_condition

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['1', '2', '3', '4 и более']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите количество владельцев:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_owners_number)


def handle_owners_number(message):
    owners_number = message.text
    user_data[message.chat.id]['owners_number'] = owners_number

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['Да', 'Нет']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите статус растаможки:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_customs_status)


def handle_customs_status(message):
    customs_status = message.text
    user_data[message.chat.id]['customs_status'] = customs_status

    bot.send_message(message.chat.id, 'Прикрепите фотографию автомобиля')
    bot.register_next_step_handler(message, handle_car_photos)

def handle_car_photos(message):
    if message.content_type == 'photo':
        photo = message.photo[-1].file_id
        user_data[message.chat.id].setdefault('car_photos', []).append(photo)

        if len(user_data[message.chat.id]['car_photos']) < 10:
            bot.send_message(message.chat.id, 'Прикрепите еще фотографии или нажмите /skip, чтобы пропустить этот шаг')
            bot.register_next_step_handler(message, handle_car_photos)
        else:
            handle_additional_description(message)  # вызов функции handle_additional_description
    elif message.text == '/skip':
        bot.send_message(message.chat.id, 'Вы пропустили добавление фотографии. Введите дополнительное описание автомобиля (если есть)')
        bot.register_next_step_handler(message, handle_additional_description)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, прикрепите фотографию автомобиля или нажмите /skip, чтобы пропустить добавление фотографии')
        bot.register_next_step_handler(message, handle_car_photos)

def handle_additional_description(message):
    additional_description = message.text
    user_data[message.chat.id]['additional_description'] = additional_description

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = ['₽', '$']
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите валюту:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_currency)

def handle_currency(message):
    currency = ''

    if message.text == '₽':
        currency = 'RUB'
    elif message.text == '$':
        currency = 'USD'
    # Добавьте дополнительные условия для других валют, если необходимо

    user_data[message.chat.id]['currency'] = currency

    bot.send_message(message.chat.id, 'Введите цену автомобиля')
    bot.register_next_step_handler(message, handle_car_price)


def handle_car_price(message):
    car_price = message.text
    user_data[message.chat.id]['car_price'] = car_price

    bot.send_message(message.chat.id, 'Введите местонахождение автомобиля')
    bot.register_next_step_handler(message, handle_location)


def handle_location(message):
    location = message.text
    user_data[message.chat.id]['location'] = location

    bot.send_message(message.chat.id, 'Введите ваш номер телефона или телеграм для связи')
    bot.register_next_step_handler(message, handle_contact_info)


def handle_contact_info(message):
    contact_info = message.text
    user_data[message.chat.id]['contact_info'] = contact_info

    channel_id = '-1001866290487'  # Здесь нужно указать ID вашего канала
    channel_message = f'Новое объявление:\nМарка машины: {user_data[message.chat.id]["brand"]}\n' \
                      f'Модель машины: {user_data[message.chat.id]["model"]}\n' \
                      f'Тип кузова: {user_data[message.chat.id]["body_type"]}\n' \
                      f'Тип двигателя: {user_data[message.chat.id]["engine"]}\n' \
                      f'Объем двигателя (куб см): {user_data[message.chat.id]["engine_capacity"]}\n' \
                      f'Мощность (л. сил): {user_data[message.chat.id]["engine_power"]}\n' \
                      f'Тип КПП: {user_data[message.chat.id]["transmission"]}\n' \
                      f'Цвет авто: {user_data[message.chat.id]["color"]}\n' \
                      f'Пробег (км): {user_data[message.chat.id]["mileage"]}\n' \
                      f'Состояние документов: {user_data[message.chat.id]["document_condition"]}\n' \
                      f'Кол-во владельцев: {user_data[message.chat.id]["owners_number"]}\n' \
                      f'Растаможена?: {user_data[message.chat.id]["customs_status"]}\n' \
                      f'Дополнительное описание: {user_data[message.chat.id]["additional_description"]}\n' \
                      f'Цена авто: {user_data[message.chat.id]["car_price"]} {user_data[message.chat.id]["currency"]} \n' \
                      f'Местонахождение авто: {user_data[message.chat.id]["location"]}\n' \
                      f'Контактная информация: {user_data[message.chat.id]["contact_info"]}'

    if 'car_photos' in user_data[message.chat.id]:
        photo_file_ids = user_data[message.chat.id]['car_photos']
        for photo_file_id in photo_file_ids:
            bot.send_photo(channel_id, photo_file_id, caption=channel_message)

    preview_message = f'Предпросмотр объявления:\n{channel_message}'

    # Создаем Inline-кнопки "Разместить" и "Редактировать"
    markup = types.InlineKeyboardMarkup()
    publish_button = types.InlineKeyboardButton("Разместить", callback_data="publish")
    edit_button = types.InlineKeyboardButton("Редактировать", callback_data="edit")
    markup.row(publish_button, edit_button)

    bot.send_message(message.chat.id, preview_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query):
    data = callback_query.data

    if data == 'publish':
        handle_publish(callback_query)
    elif data == 'edit':
        handle_edit(callback_query)
    elif data == 'edit_brand':
        handle_edit_field(callback_query, 'brand')
    elif data == 'edit_model':
        handle_edit_field(callback_query, 'model')
    elif data == 'edit_body_type':
        handle_edit_field(callback_query, 'body_type')
    elif data == 'edit_engine':
        handle_edit_field(callback_query, 'engine')
    # Добавьте обработчики для других полей
    elif data == 'edit_engine_capacity':
        handle_edit_field(callback_query, 'engine_capacity')
    elif data == 'edit_engine_power':
        handle_edit_field(callback_query, 'engine_power')
    elif data == 'edit_transmission':
        handle_edit_field(callback_query, 'transmission')
    elif data == 'edit_color':
        handle_edit_field(callback_query, 'color')
    elif data == 'edit_mileage':
        handle_edit_field(callback_query, 'mileage')
    elif data == 'edit_document_condition':
        handle_edit_field(callback_query, 'document_condition')
    elif data == 'edit_owners_number':
        handle_edit_field(callback_query, 'owners_number')
    elif data == 'edit_customs_status':
        handle_edit_field(callback_query, 'customs_status')
    elif data == 'edit_additional_description':
        handle_edit_field(callback_query, 'additional_description')
    elif data == 'edit_car_price':
        handle_edit_field(callback_query, 'car_price')
    elif data == 'edit_currency':
        handle_edit_field(callback_query, 'currency')
    elif data == 'edit_location':
        handle_edit_field(callback_query, 'location')
    elif data == 'edit_contact_info':
        handle_edit_field(callback_query, 'contact_info')
    elif data == 'restart':
        restart(callback_query.message)
    elif data == 'help':
        handle_help(callback_query)
    elif data == 'accelerate':
        handle_accelerate(callback_query)


def handle_publish(callback_query):
    message = callback_query.message

    channel_id = '-1001866290487'  # Здесь нужно указать ID вашего канала
    channel_message = f'Новое объявление:\nМарка машины: {user_data[message.chat.id]["brand"]}\n' \
                      f'Модель машины: {user_data[message.chat.id]["model"]}\n' \
                      f'Тип кузова: {user_data[message.chat.id]["body_type"]}\n' \
                      f'Тип двигателя: {user_data[message.chat.id]["engine"]}\n' \
                      f'Объем двигателя (куб см): {user_data[message.chat.id]["engine_capacity"]}\n' \
                      f'Мощность (л. сил): {user_data[message.chat.id]["engine_power"]}\n' \
                      f'Тип КПП: {user_data[message.chat.id]["transmission"]}\n' \
                      f'Цвет авто: {user_data[message.chat.id]["color"]}\n' \
                      f'Пробег (км): {user_data[message.chat.id]["mileage"]}\n' \
                      f'Состояние документов: {user_data[message.chat.id]["document_condition"]}\n' \
                      f'Кол-во владельцев: {user_data[message.chat.id]["owners_number"]}\n' \
                      f'Растаможена?: {user_data[message.chat.id]["customs_status"]}\n' \
                      f'Дополнительное описание: {user_data[message.chat.id]["additional_description"]}\n' \
                      f'Цена авто: {user_data[message.chat.id]["car_price"]} {user_data[message.chat.id]["currency"]}\n' \
                      f'Местонахождение авто: {user_data[message.chat.id]["location"]}\n' \
                      f'Контактная информация: {user_data[message.chat.id]["contact_info"]}'

    if 'car_photos' in user_data[message.chat.id]:
        photo_file_ids = user_data[message.chat.id]['car_photos']
        for photo_file_id in photo_file_ids:
            bot.send_photo(channel_id, photo_file_id, caption=channel_message)
    else:
        bot.send_message(channel_id, channel_message)

    # Создаем и добавляем кнопки сразу после публикации объявления
    markup = types.InlineKeyboardMarkup(row_width=1)
    restart_button = types.InlineKeyboardButton("Перезапустить бота", callback_data="restart")
    accelerate_button = types.InlineKeyboardButton("Ускорить продажу", callback_data="accelerate")
    help_button = types.InlineKeyboardButton("Помощь", callback_data="help")
    markup.add(restart_button, accelerate_button, help_button)

    # Сохранение файла
    excel_file_path = 'путь_к_вашему_файлу.xlsx'
    workbook = openpyxl.Workbook()

    # Выбор активного листа для записи данных
    worksheet = workbook.active

    # Получение следующей доступной строки
    next_row = worksheet.max_row + 1

    # Запись данных в ячейки
    worksheet[f'A{next_row}'] = user_data[message.chat.id]["brand"]
    worksheet[f'B{next_row}'] = user_data[message.chat.id]["model"]
    # Заполните остальные ячейки соответствующими данными

    # Сохранение файла
    workbook.save(excel_file_path)

    bot.send_message(chat_id=message.chat.id, text='Объявление успешно размещено! 👍', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Перезапустить бота')
def restart(message):
    bot.send_message(message.chat.id, 'Бот перезапущен!')
    user_data[message.chat.id] = {}  # Очистить данные пользователя
    start(message)  # Вызвать функцию start для начала нового цикла


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def handle_help(callback_query):
    faq_message = 'Вот некоторая полезная информация для помощи:\n- Как опубликовать объявление?\n- Как отредактировать информацию об автомобиле?\n- Как удалить объявление?\n- Как связаться с продавцом?\n\nЕсли у вас возникли еще вопросы, обратитесь к администратору.'
    bot.send_message(callback_query.message.chat.id, faq_message)


def handle_accelerate(callback_query):
    telegram_username = '@herofiend'
    bot.send_message(callback_query.message.chat.id, f'Для ускорения продажи свяжитесь с администратором: {telegram_username}')

def handle_edit(callback_query):
    message = callback_query.message

    # Создаем Inline-кнопки для редактирования полей
    markup = types.InlineKeyboardMarkup()
    edit_brand_button = types.InlineKeyboardButton("Марка", callback_data="edit_brand")
    edit_model_button = types.InlineKeyboardButton("Модель", callback_data="edit_model")
    edit_body_type_button = types.InlineKeyboardButton("Тип кузова", callback_data="edit_body_type")
    edit_engine_button = types.InlineKeyboardButton("Тип двигателя", callback_data="edit_engine")
    # Добавьте кнопки для других полей
    edit_engine_capacity_button = types.InlineKeyboardButton("Объем двигателя", callback_data="edit_engine_capacity")
    edit_engine_power_button = types.InlineKeyboardButton("Мощность двигателя", callback_data="edit_engine_power")
    edit_transmission_button = types.InlineKeyboardButton("Тип КПП", callback_data="edit_transmission")
    edit_color_button = types.InlineKeyboardButton("Цвет авто", callback_data="edit_color")
    edit_mileage_button = types.InlineKeyboardButton("Пробег", callback_data="edit_mileage")
    edit_document_condition_button = types.InlineKeyboardButton("Состояние документов", callback_data="edit_document_condition")
    edit_owners_number_button = types.InlineKeyboardButton("Кол-во владельцев", callback_data="edit_owners_number")
    edit_customs_status_button = types.InlineKeyboardButton("Растаможена?", callback_data="edit_customs_status")
    edit_additional_description_button = types.InlineKeyboardButton("Доп. описание", callback_data="edit_additional_description")
    edit_car_price_button = types.InlineKeyboardButton("Цена авто", callback_data="edit_car_price")
    edit_currency_button = types.InlineKeyboardButton("Валюта", callback_data="edit_currency")
    edit_location_button = types.InlineKeyboardButton("Местонахождение", callback_data="edit_location")
    edit_contact_info_button = types.InlineKeyboardButton("Контактная информация", callback_data="edit_contact_info")
    markup.row(edit_brand_button, edit_model_button)
    markup.row(edit_body_type_button, edit_engine_button)
    markup.row(edit_engine_capacity_button, edit_engine_power_button)
    markup.row(edit_transmission_button, edit_color_button)
    markup.row(edit_mileage_button, edit_document_condition_button)
    markup.row(edit_owners_number_button, edit_customs_status_button)
    markup.row(edit_additional_description_button, edit_car_price_button)
    markup.row(edit_currency_button, edit_location_button)
    markup.row(edit_contact_info_button)

    bot.send_message(message.chat.id, 'Выберите поле для редактирования', reply_markup=markup)


def handle_edit_field(callback_query, field_name):
    message = callback_query.message

    bot.send_message(message.chat.id, f'Текущее значение поля "{field_name}": {user_data[message.chat.id][field_name]}'
                                      '\nВведите новое значение')
    bot.register_next_step_handler(message, lambda msg: handle_edit_field_value(msg, field_name))


def handle_edit_field_value(message, field_name):
    user_data[message.chat.id][field_name] = message.text
    bot.send_message(message.chat.id, f'Значение поля "{field_name}" успешно изменено на "{message.text}"')
    handle_contact_info(message)


bot.polling()