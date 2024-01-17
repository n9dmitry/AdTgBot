# Массивы вопросов
dict_car_brands_and_models = {
    'Audi': ['Ввести марку', 'A3', 'A4', 'Q5', 'Q7'],
    'BMW': ['Ввести марку', '3 Series', '5 Series', 'X3', 'X5'],
    'Mercedes-Benz': ['Ввести марку', 'C-Class', 'E-Class', 'GLC', 'GLE'],
    'Chevrolet': ['Ввести марку', 'Cruze', 'Malibu', 'Equinox', 'Tahoe'],
    'Ford': ['Ввести марку', 'Focus', 'Fusion', 'Escape', 'Explorer'],
    'Honda': ['Ввести марку', 'Civic', 'Accord', 'CR-V', 'Pilot'],
    'Hyundai': ['Ввести марку', 'Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Ввести марку', 'Optima', 'Sorento', 'Sportage', 'Telluride'],
    'Nissan': ['Ввести марку', 'Altima', 'Maxima', 'Rogue', 'Pathfinder'],
    'Toyota': ['Ввести марку', 'Camry', 'Corolla', 'Rav4', 'Highlander'],
    'Volkswagen': ['Ввести марку', 'Golf', 'Jetta', 'Tiguan', 'Atlas'],
    'Volvo': ['Ввести марку', 'S60', 'S90', 'XC60', 'XC90'],
    'Ferrari': ['Ввести марку', '488', 'F8 Tributo', 'Portofino', 'SF90 Stradale'],
    'Porsche': ['Ввести марку', '911', 'Cayenne', 'Panamera', 'Macan'],
    'Tesla': ['Ввести марку', 'Model S', 'Model 3', 'Model X', 'Model Y'],
    'Lamborghini': ['Ввести марку', 'Huracan', 'Aventador', 'Urus'],
    'Jaguar': ['Ввести марку', 'XE', 'XF', 'F-Pace', 'I-Pace'],
    'Land Rover': ['Ввести марку', 'Discovery', 'Range Rover Evoque', 'Range Rover Sport', 'Defender'],
    'Mazda': ['Ввести марку', 'Mazda3', 'Mazda6', 'CX-5', 'CX-9'],
    'Subaru': ['Ввести марку', 'Impreza', 'Outback', 'Forester', 'Ascent'],
    'LADA': ['Ввести марку', 'Vesta', 'Granta', 'XRAY', '4x4'],
    'УАЗ': ['Ввести марку', 'Patriot', 'Hunter', 'Bukhanka'],
    'ГАЗ': ['Ввести марку', 'Sobol', 'Next', 'Gazelle'],
    'КАМАЗ': ['Ввести марку', '5490', '6520', '43118'],
    'АвтоВАЗ': ['Ввести марку', 'LADA 4x4', 'LADA Kalina', 'LADA Priora', 'LADA XRAY']
}
# car_year - нужна просто проверка на инпут на 4 знака
dict_car_body_types = {
    "Седан",
    "Хэтчбек",
    "Универсал",
    "Купе",
    "Кабриолет",
    "Спортивный купе",
    "Внедорожник",
    "Кроссовер",
    "Минивэн",
    "Пикап",
}
dict_car_engine_types = {
    "Бензиновый",
    "Дизельный",
    "Электрический",
    "Гибридный",
    "Турбированный",
    "Роторный (Ванкель)",
    "Газовый",
    "Водородный",
}
# car_engine_volume (объём) - не нужен словарь. инпут проверка (продумать логику)
# car_power (мощность) - не нужен словарь. инпут проверка (продумать логику)
dict_car_transmission_types = {
    "Механическая",
    "Автоматическая",
    "Роботизированная",
    "Вариатор",
}
dict_car_colors = {
    "Черный": "⚫",
    "Белый": "⚪",
    "Серый": "⚪",
    "Красный": "🔴",
    "Синий": "🔵",
    "Зеленый": "🟢",
    "Желтый": "🟡",
    "Оранжевый": "🟠",
    "Фиолетовый": "🟣",
    "Розовый": "💗",
}
# car_mileage (пробег) - проверка на инпут, примеры
dict_car_document_statuses = {
    "Оригинал",
    "Дубликат",
    "Временный",
    "Без документов",
    "Исполненные",
    "Отозванные",
    "На рассмотрении",
    "Продленные",
    "Утерянные",
}
dict_car_owners = {
    "1",
    "2",
    "3",
    "4 и более",
}
# car_customs_cleared - yes/no
# car_description - проверка на количество символов
# car_price - проверка на количество символов
# car_location - валидация
# seller_name - валидация
# seller_phone - валидация