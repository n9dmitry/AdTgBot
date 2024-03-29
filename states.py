from aiogram.dispatcher.filters.state import State, StatesGroup

# STATE_CAR_BRAND = 'state_car_brand'
# STATE_CAR_MODEL = 'state_car_model'
# STATE_CAR_YEAR = 'state_car_year'
# STATE_CAR_BODY_TYPE = 'state_car_body_type'
# STATE_CAR_ENGINE_TYPE = 'state_car_engine_type'
# STATE_CAR_ENGINE_VOLUME = 'state_car_engine_volume'
# STATE_CAR_POWER = 'state_car_power'
# STATE_CAR_TRANSMISSION_TYPE = 'state_car_transmission_type'
# STATE_CAR_COLOR = 'state_car_color'
# STATE_CAR_MILEAGE = 'state_car_mileage'
# STATE_CAR_DOCUMENT_STATUS = 'state_car_document_status'
# STATE_CAR_OWNERS = 'state_car_owners'
# STATE_CAR_CUSTOMS_CLEARED = 'state_car_customs_cleared'
# STATE_CAR_CONDITION = 'state_car_condition'
# STATE_CAR_DESCRIPTION = 'state_car_description'
# STATE_CAR_PRICE = 'state_car_price'
# STATE_SELECT_CURRENCY = "state_select_currency"
# STATE_CAR_LOCATION = 'state_car_location'
# STATE_SELLER_NAME = 'state_seller_name'
# STATE_SELLER_PHONE = 'state_seller_phone'
# STATE_PREVIEW_PHOTO = 'state_preview_photo'
# STATE_CAR_PHOTO = 'state_car_photo'
# STATE_SEND = 'state_send'

class User(StatesGroup):
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
    # support
    STATE_SUPPORT_VALIDATION = State()
    STATE_SUPPORT_MESSAGE = State()
    STATE_SUPPORT_END = State()