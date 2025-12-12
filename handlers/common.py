from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import get_main_menu, games_selection

router = Router()

@router.message(F.text == "🎲 Игровой раздел")
async def display_games(message: Message):
    await message.answer("Доступные игры:", reply_markup=games_selection)

@router.message(F.text == "📋 Информация")
async def bot_description(message: Message):
    await message.answer(
        "🤖 *Бот-развлечение с разнообразным функционалом:*\n\n"

        "👤 <b>Профиль пользователя</b>\n"
        "• Создайте и настройте персональный профиль\n"
        "• Храните информацию о себе в удобном формате\n"
        "• Просматривайте свои данные в любое время\n\n"

        "🎮 <b>Игровой раздел</b>\n"
        "🪨 <i>«Камень-Ножницы-Бумага»</i>\n"
        "• Сделайте выбор из трех классических вариантов\n"
        "• Бот также делает случайный выбор\n"
        "• Побеждает по принципу: камень бьёт ножницы, ножницы режут бумагу, бумага накрывает камень\n\n"

        "🎲 <i>Угадывание результата броска</i>\n"
        "• Попробуйте предсказать число от 1 до 6\n"
        "• Бот имитирует случайный бросок виртуального кубика\n"
        "• Точное совпадение приносит победу! 🎯\n\n"

        "👑 <b>Энциклопедия Принцесс Диснея</b>\n"
        "• Узнайте о ваших любимых героинях\n"
        "• История, характер и приключения\n"
        "• Красочные описания и интересные факты\n\n"

        "✨ <i>Наслаждайтесь разнообразными возможностями бота!</i> 😊",
        reply_markup=get_main_menu,
        parse_mode="HTML"
    )

@router.message(F.text == "👤 Профиль пользователя")
async def my_profile(message: Message):
    from handlers.auth import user_profiles

    profile = user_profiles.get(message.from_user.id)
    if not profile:
        await message.answer("❌ Профиль не найден. Пройдите регистрацию заново (/start).")
        return

    lines = []
    lines.append(f"👤 <b>{profile['name']} {profile['surname']}</b>")
    if profile.get("age"):
        lines.append(f"🎂 Возраст: {profile['age']}")
    if profile.get("gender"):
        lines.append(f"⚧️ Пол: {profile['gender']}")
    if profile.get("region"):
        lines.append(f"📍 Регион: {profile['region']}")
    if profile.get("interests"):
        lines.append(f"❤️ Интересы: {profile['interests']}")

    text = "\n".join(lines)

    if profile.get("photo"):
        await message.answer_photo(photo=profile["photo"], caption=text, parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")

@router.message(F.text == "🔙 Назад")
async def back_from_games(message: Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu)

@router.message(F.text == "🔙 К списку игр")
async def back_to_game_selection(message: Message):
    await message.answer("Выберите игру:", reply_markup=games_selection)

@router.message(F.text == "🔙 В меню")
async def back_to_menu(message: Message):
    await message.answer("Основное меню:", reply_markup=get_main_menu)

@router.message()
async def handle_unknown(message: Message):
    await message.answer(
        "❌ Извините, я не понимаю это сообщение.\nПожалуйста, используйте кнопки меню.",
        reply_markup=get_main_menu
    )