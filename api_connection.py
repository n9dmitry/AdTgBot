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
        title = f"{user_data['realty_rooms']}, {user_data['realty_type']}, {user_data['realty_square']}, {user_data['realty_floor']} / {user_data['realty_floors_total']} этаж"
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