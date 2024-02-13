from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import datetime
import uuid
import asyncio
import openpyxl
from config import *
from states import *
from validation import *
import json
from enumlist import *

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
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard, row_width=2)
    buttons = [KeyboardButton(text=text) for text in button_texts]
    keyboard.add(*buttons)
    return keyboard




class CarBotHandler:
    def __init__(self):
        self.lock = asyncio.Lock()


# Команды

    async def restart(self, event, state):
        # В этом методе вы должны определить логику перезапуска вашего бота
        # # await self.m.delete()
        await state.finish()  # Завершаем текущее состояние FSM
        await event.answer("Бот перезапущен.")  # Отправляем сообщение о перезапуске
        await self.start(event, state)  # Запускаем начальное действие вашего бота


    async def support(self, event, state):
        await state.finish()
        self.secret_number = str(random.randint(100, 999))

        await event.answer(f"Нашли баг? Давайте отправим сообщение разработчикам! "
                             f"Но перед этим введите проверку. Докажите что вы не робот. Напишите число {self.secret_number}:")
        await state.set_state(User.STATE_SUPPORT_VALIDATION)

    async def support_validation(self, event, state):
        if event.text.isdigit() and event.text == self.secret_number:
            await event.reply(f"Проверка пройдена успешно!")
            await asyncio.sleep(1)
            await event.answer(f"Опишите техническую проблему в деталях для разработчиков: ")
            await state.set_state(User.STATE_SUPPORT_MESSAGE)
        else:
            await event.answer(f"Попробуйте ещё раз!")
            await asyncio.sleep(1)
            await cmd_support(event, state)

    async def support_message(self, event: types.Message, state):
        # Получаем текущую дату и время
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Формируем строку для записи в файл
        message_to_write = f"""
        Дата: {current_time}
        Имя: {event.from_user.full_name}
        Telegram @{event.from_user.username or event.from_user.id} 
      
        Сообщение: {event.text}
        ...
            """

        # Открываем файл для записи и записываем сообщение
        with open("support.txt", "a") as file:
            file.write(message_to_write)
        keyboard = create_keyboard(['Перезагрузить бота'])
        await event.reply("Спасибо за ваше сообщение! Мы рассмотрим вашу проблему!", reply_markup=keyboard)
        await state.set_state(User.STATE_SUPPORT_END)
    async def support_end(selfself, event, state):
        if event.text == 'Перезагрузить бота':
            await cmd_restart(event, state)
        await state.finish()



# Начало работы бота

    async def start(self, event, state):
        image_hello_path = ImageDirectory.say_hi
        with open(image_hello_path, "rb") as image_hello:
            self.m = await event.answer_photo(image_hello,
                                     caption=f"Привет, {event.from_user.first_name}! Давай продадим твоё авто! Начнём же сбор данных!")
        await asyncio.sleep(2)
        # # await self.m.delete()
        # self.m = await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        image_path = ImageDirectory.car_brand  # Путь к вашему изображению
        with open(image_path, "rb") as image:
            self.m = await event.answer_photo(image, caption="Выберите бренд автомобиля:", reply_markup=keyboard)
        # self.m = await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_BRAND)




    async def get_car_brand(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        selected_brand = event.text
        valid_brands = dict_car_brands_and_models
        if await validate_car_brand(selected_brand, valid_brands):
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            # await self.delete_hello(event)
            # Создаем клавиатуру
            keyboard = create_keyboard(
                dict_car_brands_and_models[selected_brand])
            image_path = ImageDirectory.car_model
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Отлично! Выберите модель автомобиля:", reply_markup=keyboard)
            # self.m = await event.answer("Отлично! Выберите модель автомобиля:", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_MODEL)
        else:
#             await self.delete_previous_question(event)
#             await self.delete_hello(event)
            keyboard = create_keyboard(dict_car_brands_and_models.keys())
            self.m = await bot.send_message(event.from_user.id, "Пожалуйста, выберите бренд из предложенных вариантов или напишите нам если вашего бренда нет", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_BRAND)

    async def get_car_model(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        car_brand = user_data.get("car_brand", "")
        valid_models = dict_car_brands_and_models.get(car_brand, [])

        if await validate_car_model(event.text, valid_models):
            user_data["car_model"] = event.text
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.car_year
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Какой год выпуска у автомобиля? (напишите)")
            # self.m = await event.answer("Какой год выпуска у автомобиля? (напишите)")
            await state.set_state(User.STATE_CAR_YEAR)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(valid_models)
            self.m = await bot.send_message(event.from_user.id, "Пожалуйста, выберите модель из предложенных вариантов.",
                                   reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_MODEL)

    async def get_car_year(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # # await self.m.delete()

        if await validate_year(event.text):
            user_data["car_year"] = event.text
            keyboard = create_keyboard(dict_car_body_types)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_body_type
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Отлично! Какой тип кузова у автомобиля?", reply_markup=keyboard)
            # self.m = await event.answer("Отлично! Какой тип кузова у автомобиля?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_BODY_TYPE)
        else:
            # await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите год в формате YYYY (например, 1990 или 2024)")
            await state.set_state(User.STATE_CAR_YEAR)

    async def get_car_body_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_body_types):
            user_data["car_body_type"] = event.text
            keyboard = create_keyboard(dict_car_engine_types)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_engine_type
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Отлично! Какой тип двигателя у автомобиля?", reply_markup=keyboard)
            # self.m = await event.answer("Отлично! Какой тип двигателя у автомобиля?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_ENGINE_TYPE)
        else:
            # await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_body_types)
            self.m = await event.answer("Пожалуйста, выберите корректный тип кузова.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_BODY_TYPE)

    async def get_car_engine_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_engine_types):
            user_data["car_engine_type"] = event.text
            # Добавляем кнопки на основе словаря
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_engine_volume
            with open(image_path, "rb") as image:
                self.m = self.m = await event.answer_photo(image, caption="Хорошо! Какой объем двигателя у автомобиля (л.)? (напишите через точку: например 1.6)")
            # self.m = await event.answer("Хорошо! Какой объем двигателя у автомобиля (л.)? (напишите через точку: например 1.6)")
            await state.set_state(User.STATE_CAR_ENGINE_VOLUME)
        else:
            # await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_engine_types)
            self.m = await event.answer("Пожалуйста, выберите корректный тип двигателя.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_ENGINE_TYPE)

    async def get_car_engine_volume(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        try:
            if "," in event.text:
                event.text = event.text.replace(',', '.')
            event.text = float(event.text)

            if await validate_engine_volume(event.text):
                user_data["car_engine_volume"] = event.text

                # Добавляем кнопки на основе словаря

                await state.update_data(user_data=user_data)
                # await self.delete_previous_question(event)
                image_path = ImageDirectory.car_power
                with open(image_path, "rb") as image:
                    self.m = await event.answer_photo(image,
                                             caption="Отлично! Укажите мощность двигателя автомобиля от 50 до 1000 (л.с.). (напишите)")
                # self.m = await event.answer("Отлично! Укажите мощность двигателя автомобиля от 50 до 1000 (л.с.). (напишите)")
                await state.set_state(User.STATE_CAR_POWER)
        except ValueError:
            # Если не удалось преобразовать введенный текст в число
            self.m = await event.answer(
                "Пожалуйста, корректный объем двигателя (в пределах от 0.2 до 10.0 литров) через точку или целым числом(!).")
            await state.set_state(User.STATE_CAR_ENGINE_VOLUME)

    async def get_car_power(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_car_power(event.text):
            user_data["car_power"] = event.text
            keyboard = create_keyboard(dict_car_transmission_types)

            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_transmission_type
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Отлично! Какой тип коробки передач используется в автомобиле?", reply_markup=keyboard)
            # await event.answer("Отлично! Какой тип коробки передач используется в автомобиле?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_TRANSMISSION_TYPE)
        else:
            # await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите корректную мощность двигателя (в пределах от 50 до 1000 л.с.).")
            await state.set_state(User.STATE_CAR_POWER)

    async def get_car_transmission_type(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_transmission_types):
            user_data["car_transmission_type"] = event.text
            keyboard = create_keyboard(dict_car_colors)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_color
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Какого цвета автомобиль?", reply_markup=keyboard)
            # self.m = await event.answer("Какого цвета автомобиль?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_COLOR)
        else:
            # await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_transmission_types)
            self.m = await event.answer("Пожалуйста, выберите корректный тип трансмиссии.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_TRANSMISSION_TYPE)

    async def get_car_color(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_colors):
            user_data["car_color"] = event.text
            keyboard = create_keyboard(dict_car_mileages)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_mileage
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Каков пробег автомобиля(км.)? (если новый, выберите 'Новый')", reply_markup=keyboard)
            # self.m = await event.answer("Каков пробег автомобиля(км.)? (если новый, выберите 'Новый')", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_MILEAGE)
        else:
            # await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_colors)
            self.m = await event.answer("Пожалуйста, выберите корректный цвет автомобиля.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_COLOR)

    async def get_car_mileage(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_car_mileage(event.text):
            user_data["car_mileage"] = event.text
            keyboard = create_keyboard(dict_car_document_statuses)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_document_status
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Каков статус документов у автомобиля ?", reply_markup=keyboard)
            # self.m = await event.answer("Каков статус документов у автомобиля ?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_DOCUMENT_STATUS)
        else:
            # await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_mileages)
            self.m = await event.answer("Пожалуйста, введите корректное значение пробега.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_MILEAGE)

    async def get_car_document_status(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_document_statuses):

            user_data["car_document_status"] = event.text
            keyboard = create_keyboard(dict_car_owners)
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_owners
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Сколько владельцев у автомобиля?", reply_markup=keyboard)
            # self.m = await event.answer("Сколько владельцев у автомобиля?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_OWNERS)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_document_statuses)
            self.m = await event.answer("Пожалуйста, выберите корректный статус документов автомобиля.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_DOCUMENT_STATUS)

    async def get_car_owners(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_owners):
            user_data["car_owners"] = event.text
            keyboard = create_keyboard(dict_car_customs_cleared)
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.car_customs_cleared
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Растаможен ли автомобиль?", reply_markup=keyboard)
            # self.m = await event.answer("Растаможен ли автомобиль?", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_CUSTOMS_CLEARED)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_owners)
            self.m = await event.answer("Пожалуйста, выберите корректное количество владельцев автомобиля.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_OWNERS)

    async def get_car_customs_cleared(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_customs_cleared):
            user_data["car_customs_cleared"] = event.text
            keyboard = create_keyboard(dict_car_conditions)
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.car_condition
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Выберите состояние автомобиля:", reply_markup=keyboard)
            # self.m = await event.answer("Выберите состояние автомобиля:", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_CONDITION)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_customs_cleared)
            self.m = await event.answer("Пожалуйста, выберите корректный статус растаможки автомобиля.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_CUSTOMS_CLEARED)

    async def get_car_condition(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_car_conditions):
            user_data["car_condition"] = event.text
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.car_description
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Описание автомобиля. (напишите)")
            # self.m = await event.answer("Описание автомобиля. (напишите)")
            await state.set_state(User.STATE_CAR_DESCRIPTION)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_car_conditions)
            self.m = await event.answer("Пожалуйста, выберите корректное состояние автомобиля.", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_CONDITION)

    async def get_car_description(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        if await validate_length_text(event):
            if await validate_car_description(event.text):
                user_data["car_description"] = event.text
                keyboard = create_keyboard(dict_currency)
                await state.update_data(user_data=user_data)
    #             await self.delete_previous_question(event)
                image_path = ImageDirectory.car_currency
                with open(image_path, "rb") as image:
                    self.m = await event.answer_photo(image, caption="Выберите валюту:", reply_markup=keyboard)
                # self.m = await event.answer("Выберите валюту:", reply_markup=keyboard)
                await state.set_state(User.STATE_SELECT_CURRENCY)
            else:
    #             await self.delete_previous_question(event)
                self.m = await event.answer("Пожалуйста, введите корректное описание.")
                await state.set_state(User.STATE_CAR_DESCRIPTION)
        else:
            self.m = await event.answer("Ваше описание сильно большое. Напишите до ~500 символов:")
            await state.set_state(User.STATE_CAR_DESCRIPTION)

    async def select_currency(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()
        if await validate_button_input(event.text, dict_currency):
            user_data["currency"] = event.text
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.car_price
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Цена автомобиля?")
            # self.m = await event.answer("Цена автомобиля?")
            await state.set_state(User.STATE_CAR_PRICE)
        else:
#             await self.delete_previous_question(event)
            keyboard = create_keyboard(dict_currency)
            self.m = await event.answer("Пожалуйста, выберите корректную валюту.", reply_markup=keyboard)
            await state.set_state(User.STATE_SELECT_CURRENCY)

    async def get_car_price(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        if await validate_car_price(event.text):
            user_data["car_price"] = event.text
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            image_path = ImageDirectory.car_location
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Прекрасно! Где находится автомобиль? Город/пункт. (напишите)")
            # self.m = await event.answer("Прекрасно! Где находится автомобиль? Город/пункт. (напишите)")
            await state.set_state(User.STATE_CAR_LOCATION)
        else:
#             await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите корректную цену.")
            await state.set_state(User.STATE_CAR_PRICE)

    async def get_car_location(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        if await validate_car_location(event.text):
            user_data["car_location"] = event.text
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.seller_name
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Прекрасно! Укажите имя продавца. (напишите)")
            # self.m = await event.answer("Прекрасно! Укажите имя продавца. (напишите)")
            await state.set_state(User.STATE_SELLER_NAME)
        else:
#             await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите корректные данные.")
            await state.set_state(User.STATE_CAR_LOCATION)

    async def get_seller_name(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        if await validate_name(event.text) is True:
            user_data["seller_name"] = event.text
            await state.update_data(user_data=user_data)
#             await self.delete_previous_question(event)
            image_path = ImageDirectory.seller_phone
            with open(image_path, "rb") as image:
                self.m = await event.answer_photo(image, caption="Отлично! Какой телефонный номер у продавца? (напишите в формате +7XXXNNNXXNN или 8XXXNNNXXNN)")
            # self.m = await event.answer("Отлично! Какой телефонный номер у продавца? (напишите в формате +7XXXNNNXXNN)")
            await state.set_state(User.STATE_SELLER_PHONE)
        else:
#             await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите корректное имя.")
            await state.set_state(User.STATE_SELLER_NAME)

    async def get_seller_phone(self, event, state):

        user_data = (await state.get_data()).get("user_data", {})
        # await self.m.delete()

        if await validate_phone_number(event.text) is True:
            event.text = '+7' + event.text[1:] if event.text.startswith('8') else event.text
            user_data["seller_phone"] = event.text
            await state.update_data(user_data=user_data)
            print(user_data)
            print(await validate_final_length(event, state, user_data))
            if await validate_final_length(event, state, user_data):
                print(validate_final_length)
    #             await self.delete_previous_question(event)
                image_path = ImageDirectory.car_photos
                with open(image_path, "rb") as image:
                    self.m = await event.answer_photo(image, caption="Добавьте фотографии авто до 10 штук (За один раз!)")
                # self.m = await event.answer("Добавьте фотографии авто")
                await state.set_state(User.STATE_CAR_PHOTO)
            else:
                await event.reply(f"Ваше сообщение получилось сильно большим! \nПерезагрузите бота и напишите объявление заново.")

        else:
#             await self.delete_previous_question(event)
            self.m = await event.answer("Пожалуйста, введите корректный номер в формате +7XXXNNNXXNN.")
            await state.set_state(User.STATE_SELLER_PHONE)

    async def handle_photos(self, event, state):
        user_data = await state.get_data('user_data')
        photo_id = event.photo[-1].file_id


        self.new_id = str(uuid.uuid4().int)[:6]

        caption = (
            f"🛞 <b>#{user_data.get('user_data').get('car_brand')}-{user_data.get('user_data').get('car_model')}</b>\n\n"
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
            f"💬<b>Телеграм:</b> <span class='tg-spoiler'>{event.from_user.username if event.from_user.username is not None else 'по номеру телефона'}</span>\n\n"
            f"ООО 'Продвижение' Авто в ДНР (link: разместить авто)\n\n"
            f"<b>ID объявления: #{self.new_id}</b>"
        )




        if "sent_photos" not in user_data:
            user_data["sent_photos"] = []

        user_data["sent_photos"].append(
            {"file_id": photo_id,})
        buffered_photos.append(InputMediaPhoto(
            media=photo_id, caption=caption, parse_mode=types.ParseMode.HTML))
        # # await self.m.delete()
        if len(buffered_photos) > 1:
            for i in range(len(buffered_photos) - 1):
                buffered_photos[i].caption = None
            last_photo = buffered_photos[-1]
            last_photo.caption = caption


        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Следущий шаг")
        )



        self.m = await event.answer("Фото добавлено", reply_markup=keyboard)


        self.db_fix = user_data

        await state.finish()


    async def add_data_to_excel(self, event):
        file_path = 'db.xlsx'


        row_data = [
            self.new_id,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.db_fix.get('user_data').get('car_brand', ''),
            self.db_fix.get('user_data').get('car_model', ''),
            self.db_fix.get('user_data').get('car_year', ''),
            self.db_fix.get('user_data').get('car_mileage', ''),
            self.db_fix.get('user_data').get('car_transmission_type', ''),
            self.db_fix.get('user_data').get('car_body_type', ''),
            self.db_fix.get('user_data').get('car_engine_type', ''),
            self.db_fix.get('user_data').get('car_engine_volume', ''),
            self.db_fix.get('user_data').get('car_power', ''),
            self.db_fix.get('user_data').get('car_color', ''),
            self.db_fix.get('user_data').get('car_document_status', ''),
            self.db_fix.get('user_data').get('car_owners', ''),
            self.db_fix.get('user_data').get('car_customs_cleared'),
            self.db_fix.get('user_data').get('car_condition', ''),
            self.db_fix.get('user_data').get('car_description', ''),
            self.db_fix.get('user_data').get('car_price', ''),
            self.db_fix.get('user_data').get('currency', ''),
            self.db_fix.get('user_data').get('car_location', ''),
            self.db_fix.get('user_data').get('seller_name', ''),
            self.db_fix.get('user_data').get('seller_phone', ''),
            event.from_user.username if event.from_user.username is not None else 'по номеру телефона',
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
                'ID','Дата', 'Бренд', 'Модель', 'Год', 'Пробег (км)', 'Тип трансмиссии',
                'Тип кузова', 'Тип двигателя', 'Объем двигателя (л)', 'Мощность (л.с.)',
                'Цвет', 'Статус документа', 'Количество владельцев', 'Растаможен',
                'Состояние', 'Дополнительное описание', 'Цена', 'Валюта',
                'Местоположение', 'Имя продавца', 'Телефон продавца', 'Телеграм'
            ]
            sheet.append(headers)

        sheet.append(row_data)
        workbook.save(file_path)

    async def preview_advertisement(self, event):
        await bot.send_media_group(chat_id=event.chat.id, media=buffered_photos, disable_notification=True)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Отправить в канал"),
            KeyboardButton("Отменить и заполнить заново"),
        )
        await event.reply("Так будет выглядеть ваше объявление. Вы можете либо разместить либо отменить и заполнить заново.", reply_markup=keyboard)

    async def send_advertisement(self, event):
        # user_id = event.from_user.id
        # await self.m.delete()
        async with lock:
            user_id = event.from_user.id
            await self.add_data_to_excel(event)
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            keyboard = create_keyboard(['Добавить ещё объявление', 'Ускорить продажу'])
            await bot.send_message(user_id, "Объявление отправлено в канал!", reply_markup=keyboard)

            buffered_photos.clear()


    async def fill_again(self, event, state):
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        image_path = ImageDirectory.car_brand # Путь к вашему изображению
        with open(image_path, "rb") as image:
            self.m = await event.answer_photo(image, caption="Выберите бренд автомобиля:", reply_markup=keyboard)
        # self.m = await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        async with lock:
            buffered_photos.clear()
        await state.set_state(User.STATE_CAR_BRAND)

    async def add_more(self, event, state):
        await car_bot.restart(event, state)

    async def promotion(self, event, state):
        keyboard = create_keyboard(['Перезагрузить бота'])
        await event.reply("Чтобы купить закреп напишите @n9dmitry", reply_markup=keyboard)


car_bot = CarBotHandler()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
lock = asyncio.Lock()
buffered_photos = []


@dp.message_handler(commands=['restart'], state='*')
async def cmd_restart(event: types.Message, state: FSMContext):
    await car_bot.restart(event, state)

@dp.message_handler(lambda message: message.text == "Перезагрузить бота", state='*')
async def cmd_restart(event: types.Message, state: FSMContext):
    await car_bot.restart(event, state)

@dp.message_handler(commands=["start"])
async def cmd_start(event: types.Message, state: FSMContext):
    await car_bot.start(event, state)

#support
@dp.message_handler(commands=['support'], state='*')
async def cmd_support(event: types.Message, state: FSMContext):
    await car_bot.support(event, state)

@dp.message_handler(state=User.STATE_SUPPORT_VALIDATION)
async def support_validation(event: types.Message, state: FSMContext):
    await car_bot.support_validation(event, state)

@dp.message_handler(state=User.STATE_SUPPORT_MESSAGE)
async def support_message(event: types.Message, state: FSMContext):
    await car_bot.support_message(event, state)

@dp.message_handler(state=User.STATE_SUPPORT_END)
async def support_end(event: types.Message, state: FSMContext):
    await car_bot.restart(event, state)
# end support

@dp.message_handler(state=User.STATE_CAR_BRAND)
async def process_brand_selection(event: types.Message, state: FSMContext):
    await car_bot.get_car_brand(event, state)


@dp.message_handler(state=User.STATE_CAR_MODEL)
async def process_model(event: types.Message, state: FSMContext):
    await car_bot.get_car_model(event, state)


@dp.message_handler(state=User.STATE_CAR_YEAR)
async def get_car_year_handler(event: types.Message, state: FSMContext):
    await car_bot.get_car_year(event, state)


@dp.message_handler(state=User.STATE_CAR_BODY_TYPE)
async def get_car_body_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_body_type(event, state)


@dp.message_handler(state=User.STATE_CAR_ENGINE_TYPE)
async def get_car_engine_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_engine_type(event, state)


@dp.message_handler(state=User.STATE_CAR_ENGINE_VOLUME)
async def get_car_engine_volume(event: types.Message, state: FSMContext):
    await car_bot.get_car_engine_volume(event, state)


@dp.message_handler(state=User.STATE_CAR_POWER)
async def get_car_power(event: types.Message, state: FSMContext):
    await car_bot.get_car_power(event, state)


@dp.message_handler(state=User.STATE_CAR_TRANSMISSION_TYPE)
async def get_car_transmission_type(event: types.Message, state: FSMContext):
    await car_bot.get_car_transmission_type(event, state)


@dp.message_handler(state=User.STATE_CAR_COLOR)
async def get_car_color(event: types.Message, state: FSMContext):
    await car_bot.get_car_color(event, state)


@dp.message_handler(state=User.STATE_CAR_MILEAGE)
async def get_car_mileage(event: types.Message, state: FSMContext):
    await car_bot.get_car_mileage(event, state)


@dp.message_handler(state=User.STATE_CAR_DOCUMENT_STATUS)
async def get_car_document_status(event: types.Message, state: FSMContext):
    await car_bot.get_car_document_status(event, state)


@dp.message_handler(state=User.STATE_CAR_OWNERS)
async def get_car_owners(event: types.Message, state: FSMContext):
    await car_bot.get_car_owners(event, state)


@dp.message_handler(state=User.STATE_CAR_CUSTOMS_CLEARED)
async def get_car_customs_cleared(event: types.Message, state: FSMContext):
    await car_bot.get_car_customs_cleared(event, state)


@dp.message_handler(state=User.STATE_CAR_CONDITION)
async def get_car_condition(event: types.Message, state: FSMContext):
    await car_bot.get_car_condition(event, state)


@dp.message_handler(state=User.STATE_CAR_DESCRIPTION)
async def get_car_description(event: types.Message, state: FSMContext):
    await car_bot.get_car_description(event, state)


@dp.message_handler(state=User.STATE_SELECT_CURRENCY)
async def select_currency(event: types.Message, state: FSMContext):
    await car_bot.select_currency(event, state)


@dp.message_handler(state=User.STATE_CAR_PRICE)
async def get_car_price(event: types.Message, state: FSMContext):
    await car_bot.get_car_price(event, state)


@dp.message_handler(state=User.STATE_CAR_LOCATION)
async def get_car_location_handler(event: types.Message, state: FSMContext):
    await car_bot.get_car_location(event, state)


@dp.message_handler(state=User.STATE_SELLER_NAME)
async def get_seller_name_handler(event: types.Message, state: FSMContext):
    await car_bot.get_seller_name(event, state)


@dp.message_handler(state=User.STATE_SELLER_PHONE)
async def get_seller_phone_handler(event: types.Message, state: FSMContext):
    await car_bot.get_seller_phone(event, state)


@dp.message_handler(state=User.STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(event: types.Message, state: FSMContext):
    print('STATE:', state, event)
    await car_bot.handle_photos(event, state)


@dp.message_handler(lambda message: message.text == "Следущий шаг")
async def preview_advertisement(event: types.Message):
    await car_bot.preview_advertisement(event)


@dp.message_handler(lambda message: message.text == "Отправить в канал")
async def send_advertisement(event: types.Message, state: FSMContext):
    await car_bot.send_advertisement(event)

@dp.message_handler(lambda message: message.text == "Отменить и заполнить заново")
async def fill_again(event: types.Message, state: FSMContext):
    await car_bot.fill_again(event, state)

@dp.message_handler(lambda message: message.text == "Добавить ещё объявление")
async def add_more(event: types.Message, state: FSMContext):
    await car_bot.add_more(event, state)

@dp.message_handler(lambda message: message.text == "Ускорить продажу")
async def promotion(event: types.Message, state: FSMContext):
    await car_bot.promotion(event, state)


# старт бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
