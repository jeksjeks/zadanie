import re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_main_menu

router = Router()

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

user_profiles = {}  # user_id → dict
admin_phones = {"+79018631955"}

REGIONS = ["Сюмси", "Сюмси-Ижевск", "Екатеринбург", "Новосибирск", "Казань", "Другой"]
INTERESTS = ["Получать пятёрки", "Музыка", "Кино", "Громко смеяться", "Игры", "Книги", "Восхищаться преподавателем"]

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Давайте начнем",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Запустить процесс")]],
            resize_keyboard=True
        )
    )

@router.message(F.text == "Запустить процесс")
async def request_phone(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, предоставьте номер телефона",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Отправить номер", request_contact=True)]],
            resize_keyboard=True
        )
    )
    await state.set_state(RegistrationProcess.phone_input_step)

@router.message(RegistrationProcess.phone_input_step, F.contact)
async def handle_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if phone.startswith("8"):
        phone = "+7" + phone[1:]
    elif not phone.startswith("+"):
        phone = "+" + phone

    user_id = message.from_user.id
    await state.update_data(phone=phone, user_id=user_id)

    if phone in admin_phones:
        await message.answer("✅ Вы вошли как администратор.", reply_markup=get_main_menu)
        await state.clear()
        return

    if user_id in user_profiles:
        await message.answer("✅ Добро пожаловать обратно!", reply_markup=get_main_menu)
        await state.clear()
        return

    await message.answer("Введите ваше имя:")
    await state.set_state(RegistrationProcess.first_name_input_step)

def is_valid_name(text: str) -> bool:
    return bool(re.fullmatch(r"[а-яА-ЯёЁa-zA-Z]+", text))

@router.message(RegistrationProcess.first_name_input_step)
async def handle_name(message: Message, state: FSMContext):
    if not is_valid_name(message.text):
        await message.answer("❌ Че то как будто это не имя. Попробуйте еще раз")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegistrationProcess.last_name_input_step)

@router.message(RegistrationProcess.last_name_input_step)
async def handle_surname(message: Message, state: FSMContext):
    if not is_valid_name(message.text):
        await message.answer("❌ Че то как будто это не фамилия. Попробуйте еще раз")
        return
    await state.update_data(surname=message.text.strip())
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
            [KeyboardButton(text="Пропустить")]
        ],
        resize_keyboard=True
    )
    await message.answer("Укажите ваш пол:", reply_markup=kb)
    await state.set_state(RegistrationProcess.gender_selection_step)

@router.message(RegistrationProcess.gender_selection_step)
async def handle_gender(message: Message, state: FSMContext):
    if message.text in ("Мужской", "Женский"):
        await state.update_data(gender=message.text)
    elif message.text == "Пропустить":
        await state.update_data(gender=None)
    else:
        await message.answer("Пожалуйста, используйте предложенные варианты.")
        return
    await message.answer("Укажите ваш возраст (например, 52):")
    await state.set_state(RegistrationProcess.age_input_step)

@router.message(RegistrationProcess.age_input_step)
async def handle_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (10 <= int(message.text) <= 100):
        await message.answer("❌ Некорректный возраст. Укажите число от 10 до 100.")
        return
    await state.update_data(age=int(message.text))
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=r)] for r in REGIONS],
        resize_keyboard=True
    )
    await message.answer("Выберите ваш регион:", reply_markup=kb)
    await state.set_state(RegistrationProcess.location_input_step)

@router.message(RegistrationProcess.location_input_step)
async def handle_region(message: Message, state: FSMContext):
    if message.text not in REGIONS:
        await message.answer("Пожалуйста, выберите регион из списка.")
        return
    await state.update_data(region=message.text)
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i)] for i in INTERESTS] + [[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )
    await message.answer("Выберите ваш интерес:", reply_markup=kb)
    await state.set_state(RegistrationProcess.interests_input_step)

@router.message(RegistrationProcess.interests_input_step)
async def handle_interests(message: Message, state: FSMContext):
    if message.text in INTERESTS:
        await state.update_data(interests=message.text)
    elif message.text == "Пропустить":
        await state.update_data(interests=None)
    else:
        await message.answer("Пожалуйста, выберите из списка.")
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )
    await message.answer("Загрузите фото или нажмите «Пропустить»:", reply_markup=kb)
    await state.set_state(RegistrationProcess.photo_upload_step)

@router.message(RegistrationProcess.photo_upload_step, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await ask_location(message, state)

@router.message(RegistrationProcess.photo_upload_step, F.text == "Пропустить")
async def skip_photo(message: Message, state: FSMContext):
    await state.update_data(photo=None)
    await ask_location(message, state)

@router.message(RegistrationProcess.photo_upload_step)
async def invalid_photo(message: Message):
    await message.answer("Пожалуйста, отправьте фото или нажмите «Пропустить».")

async def ask_location(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить геопозицию", request_location=True)],
            [KeyboardButton(text="Пропустить")]
        ],
        resize_keyboard=True
    )
    await message.answer("Отправьте геопозицию или пропустите:", reply_markup=kb)
    await state.set_state(RegistrationProcess.geolocation_input_step)

@router.message(RegistrationProcess.geolocation_input_step, F.location | (F.text == "Пропустить"))
async def handle_location_or_skip(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    user_profiles[user_id] = {
        "name": data["name"],
        "surname": data["surname"],
        "gender": data.get("gender"),
        "age": data.get("age"),
        "region": data.get("region"),
        "interests": data.get("interests"),
        "photo": data.get("photo"),
        "phone": data["phone"],
        "location": f"{message.location.latitude},{message.location.longitude}" if message.location else None
    }
    await message.answer("✅ Ура у тебя получилось! Это было не сложно. Регистрация завершена!", reply_markup=get_main_menu)
    await state.clear()

@router.message(RegistrationProcess.geolocation_input_step)
async def invalid_location(message: Message):
    await message.answer("Пожалуйста, отправьте геопозицию или нажмите «Пропустить».")

user_profiles = user_profiles