from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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



# Начало работы бота

    async def start(self, event, state):
        image_hello_path = ImageDirectory.say_hi
        with open(image_hello_path, "rb") as image_hello:
            self.m = await event.answer_photo(image_hello,
                                     caption=f"Привет, {event.from_user.first_name}! Давай продадим твоё авто! Начнём же сбор данных!")
        await asyncio.sleep(2)
        await self.m.delete()
        # self.m = await event.answer(f"Привет, {event.from_user.first_name}! Я бот для сбора данных. Давай начнем.")
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        image_path = ImageDirectory.car_brand  # Путь к вашему изображению
        with open(image_path, "rb") as image:
            self.m = await event.answer_photo(image, caption="Выберите бренд автомобиля:", reply_markup=keyboard)
        # self.m = await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        await state.set_state(User.STATE_CAR_BRAND)



    async def get_car_brand(self, event, state):
        user_data = (await state.get_data()).get("user_data", {})
        await self.m.delete()

        selected_brand = event.text
        valid_brands = dict_car_brands_and_models
        if await validate_car_brand(selected_brand, valid_brands):
            user_data["car_brand"] = selected_brand
            await state.update_data(user_data=user_data)
            # await self.delete_previous_question(event)
            # await self.delete_hello(event)
            # Создаем клавиатуру
            # keyboard = create_keyboard(
            #     dict_car_brands_and_models[selected_brand])
            # image_path = ImageDirectory.car_model
            # with open(image_path, "rb") as image:
            #     self.m = await event.answer_photo(image, caption="Отлично! Выберите модель автомобиля:", reply_markup=keyboard)
            self.m = await event.answer("Отлично! Теперь фото:")
            await state.set_state(User.STATE_CAR_PHOTO)
        else:
#             await self.delete_previous_question(event)
#             await self.delete_hello(event)
            keyboard = create_keyboard(dict_car_brands_and_models.keys())
            self.m = await bot.send_message(event.from_user.id, "Пожалуйста, выберите бренд из предложенных вариантов или напишите нам если вашего бренда нет", reply_markup=keyboard)
            await state.set_state(User.STATE_CAR_BRAND)

    async def handle_photos(self, event, state):
        user_data = await state.get_data('user_data')
        user_id = event.from_user.id
        photo_id = event.photo[-1].file_id

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
            f"ООО 'Продвижение' Авто в ДНР (link: разместить авто)"
        )




        print(user_data)
        photo_uuid = str(uuid.uuid4())

        if "sent_photos" not in user_data:
            user_data["sent_photos"] = []

        user_data["sent_photos"].append(
            {"file_id": photo_id, "uuid": photo_uuid})
        buffered_photos.append(InputMediaPhoto(
            media=photo_id, caption=caption, parse_mode=types.ParseMode.HTML))
        # await self.m.delete()
        if len(buffered_photos) > 1:
            for i in range(len(buffered_photos) - 1):
                buffered_photos[i].caption = None
            last_photo = buffered_photos[-1]
            last_photo.caption = caption


        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Следущий шаг")
        )


        #
        #
        # def check_duplicate_rows(ws, data_row):
        #     for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(data_row)):
        #         if all([str(cell.value) == str(data_row[i]) for i, cell in enumerate(row)]):
        #             return True
        #     return False
        #
        # # Save user_data to Excel file
        # excel_file_path = "db.xlsx"
        # wb = openpyxl.load_workbook(excel_file_path) if os.path.exists(excel_file_path) else openpyxl.Workbook()
        # ws = wb.active
        # sheet = wb.active
        # column_headers = [
        #     'Название', 'Модель', 'Год', 'Пробег (км.)', 'Тип КПП', 'Кузов', 'Тип двигателя',
        #     'Объем двигателя (л.)', 'Мощность (л.с.)', 'Цвет', 'Статус документов', 'Количество владельцев',
        #     'Растаможка', 'Состояние', 'Дополнительная информация', 'Цена', 'Местоположение',
        #     'Продавец', 'Телефон продавца', 'Телеграм'
        # ]
        # data_row = []
        # if data_row == []:
        #     data_row = [user_data['user_data'].get(field, '') for field in [
        #         'car_brand', 'car_model', 'car_year', 'car_mileage', 'car_transmission_type',
        #         'car_body_type', 'car_engine_type', 'car_engine_volume', 'car_power', 'car_color',
        #         'car_document_status', 'car_owners', 'car_customs_cleared', 'car_condition',
        #         'car_description', 'car_price', 'car_location', 'seller_name', 'seller_phone'
        #     ]]
        #     data_row.append(event.from_user.username if event.from_user.username is not None else 'по номеру телефона')
        # else:
        #     pass
        #
        # if not ws['A1'].value:  # Check if the headers are not already written
        #     for i, header in enumerate(column_headers, start=1):
        #         ws.cell(row=1, column=i).value = header
        #
        # # Check for duplicate rows before appending
        # if not check_duplicate_rows(ws, data_row):
        #     sheet.append(data_row)
        #
        #
        #
        # # Сохранение книги
        # wb.save(excel_file_path)


        self.m = await event.reply("Фото добавлено", reply_markup=keyboard)
        await state.finish()


    async def preview_advertisement(self, event):
        await bot.send_media_group(chat_id=event.chat.id, media=buffered_photos, disable_notification=True)


        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Отправить в канал"),
            KeyboardButton("Отменить и заполнить заново"),
        )
        await event.reply("Так будет выглядеть ваше объявление. Вы можете либо разместить либо отменить и заполнить заново.", reply_markup=keyboard)

    async def send_advertisement(self, event):
        user_id = event.from_user.id
        await self.m.delete()
        async with lock:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=buffered_photos, disable_notification=True)
            await bot.send_message(user_id, "Объявление отправлено в канал!")

            buffered_photos.clear()

    async def fill_again(self, event, state):
        keyboard = create_keyboard(list(dict_car_brands_and_models.keys()))
        image_path = ImageDirectory.car_brand # Путь к вашему изображению
        with open(image_path, "rb") as image:
            self.m = await event.answer_photo(image, caption="Выберите бренд автомобиля:", reply_markup=keyboard)
        # self.m = await event.answer("Выберите бренд автомобиля:", reply_markup=keyboard)
        buffered_photos.clear()
        await state.set_state(User.STATE_CAR_BRAND)


car_bot = CarBotHandler()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
lock = asyncio.Lock()
buffered_photos = []


@dp.message_handler(commands=["start"])
async def cmd_start(event: types.Message, state: FSMContext):
    await car_bot.start(event, state)


@dp.message_handler(state=User.STATE_CAR_BRAND)
async def process_brand_selection(event: types.Message, state: FSMContext):
    await car_bot.get_car_brand(event, state)

@dp.message_handler(state=User.STATE_CAR_PHOTO, content_types=['photo'])
async def handle_photos(event: types.Message, state: FSMContext):
    await car_bot.handle_photos(event, state)


@dp.message_handler(lambda message: message.text == "Следущий шаг")
async def preview_advertisement(event: types.Message):
    await car_bot.preview_advertisement(event)


@dp.message_handler(lambda message: message.text == "Отправить в канал")
async def send_advertisement(event: types.Message):
    await car_bot.send_advertisement(event)


@dp.message_handler(lambda message: message.text == "Отменить и заполнить заново")
async def fill_again(event: types.Message, state: FSMContext):
    await car_bot.fill_again(event, state)





# старт бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
