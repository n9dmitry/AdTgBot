from aiogram.fsm.state import State, StatesGroup
# from aiogram.dispatcher.filters.state import State, StatesGroup
# Импорт для разных версий aiogram
class User(StatesGroup):
    # support
    STATE_SUPPORT_VALIDATION = State()
    STATE_SUPPORT_MESSAGE = State()
    STATE_SUPPORT_END = State()
    # состояния запусков
    STATE_START_CARBOT = State()
    STATE_START_ESTATEBOT = State()
    STATE_START_HRBOT = State()
    # auto_bot
    STATE_FIRST_QUESTION = State()
    STATE_CAR_BRAND = State()
    STATE_CAR_MODEL = State()
    STATE_CAR_YEAR = State()
    STATE_CAR_BODY_TYPE = State()
    STATE_CAR_ENGINE_TYPE = State()
    STATE_CAR_ENGINE_VOLUME = State()
    STATE_CAR_POWER = State()
    STATE_CAR_TRANSMISSION_TYPE = State()
    STATE_CAR_COLOR = State()
    STATE_CAR_MILEAGE = State()
    STATE_CAR_DOCUMENT_STATUS = State()
    STATE_CAR_OWNERS = State()
    STATE_CAR_CUSTOMS_CLEARED = State()
    STATE_CAR_CONDITION = State()
    STATE_CAR_DESCRIPTION = State()
    STATE_CAR_PRICE = State()
    STATE_SELECT_CURRENCY = State()
    STATE_CAR_LOCATION = State()
    STATE_SELLER_NAME = State()
    STATE_SELLER_PHONE = State()
    STATE_PREVIEW_PHOTO = State()
    STATE_CAR_PHOTO = State()
    STATE_SEND = State()
    # estate_bot
    STATE_ESTATE_PHOTO = State()
    # hr_bot
    STATE_HR_PHOTO = State()