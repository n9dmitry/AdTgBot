from aiogram.fsm.state import State, StatesGroup
# from aiogram.dispatcher.filters.state import State, StatesGroup
# Импорт для разных версий aiogram

class Cmd(StatesGroup):
    # support
    STATE_SUPPORT_VALIDATION = State()
    STATE_SUPPORT_MESSAGE = State()
    STATE_SUPPORT_END = State()


class Car(StatesGroup):
    # состояния запусков
    STATE_START_CARBOT = State()
    # auto_bot
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





class Realty(StatesGroup):
    #estate_bot
    STATE_START_REALTY = State()
    STATE_REALTY_DEAL = State()
    STATE_REALTY_TYPE = State()
    STATE_CUSTOM_REALTY_TYPE = State()
    # ewrfwefr
    STATE_REALTY_CHECK_TYPE = State()
    # ewrfwefr
    STATE_QUESTION_BEFORE_SQUARE = State()
    STATE_REALTY_SQUARE = State()
    STATE_REALTY_DESCRIPTION = State()
    STATE_REALTY_LOCATION = State()
    STATE_REALTY_CURRENCY = State()
    STATE_REALTY_PRICE = State()
    STATE_REALTY_NAME = State()
    STATE_REALTY_CONTACTS = State()
    STATE_REALTY_PHOTO = State()
    # ымзвщшагмиыв
    STATE_REALTY_ROOMS = State()
    STATE_REALTY_FLOOR = State()
    STATE_REALTY_TOTAL_FLOORS = State()

class Job(StatesGroup):
    #hr_bot
    STATE_START_JOB = State()
    STATE_JOB_TITLE = State()
    STATE_JOB_REQUIREMENTS = State()
    STATE_JOB_RESPONSIBILITIES = State()
    STATE_JOB_CONDITIONS = State()

    STATE_JOB_DESCRIPTION = State()
    STATE_JOB_NAME = State()
    STATE_JOB_CURRENCY = State()
    STATE_JOB_PRICE = State()
    STATE_JOB_CONTACTS = State()
    STATE_JOB_PHOTOS = State()

class Ads(StatesGroup):
    STATE_PHOTO = State()
    STATE_PREVIEW_ADVERTISMENT = State()
    STATE_SEND = State()


class X(StatesGroup):
    X = State()
