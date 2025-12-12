from aiogram.fsm.state import State, StatesGroup

class RegistrationProcess(StatesGroup):
    """Последовательность шагов регистрации пользователя"""
    phone_input_step = State()
    first_name_input_step = State()
    last_name_input_step = State()
    gender_selection_step = State()
    age_input_step = State()
    location_input_step = State()
    interests_input_step = State()
    photo_upload_step = State()
    geolocation_input_step = State()