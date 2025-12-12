import random
import logging
from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import dice_controls, games_selection, get_main_menu

logger = logging.getLogger(__name__)

router = Router()

# Обработчик для кнопки "🎯 Угадай число" из games_selection
@router.message(F.text == "🎯 Угадай число")
async def start_dice(message: Message):
    logger.info(f"Start dice game by user {message.from_user.id}")
    await message.answer(
        "Выберите число от 1 до 6:",
        reply_markup=dice_controls
    )

@router.message(F.text.in_(["🎲 1", "🎲 2", "🎲 3", "🎲 4", "🎲 5", "🎲 6"]))
async def play_dice(message: Message):
    logger.info(f"Получено сообщение: '{message.text}' от пользователя {message.from_user.id}")

    emoji_to_num = {
        "🎲 1": 1, "🎲 2": 2, "🎲 3": 3,
        "🎲 4": 4, "🎲 5": 5, "🎲 6": 6
    }

    user_guess = emoji_to_num[message.text]
    real_roll = random.randint(1, 6)

    logger.info(f"User guess: {user_guess}, Real roll: {real_roll}")

    if user_guess == real_roll:
        result = "<b>🎯 Поздравляю! Вы угадали!</b>"
    else:
        result = f"<b>❌ Не угадали.</b> Выпало: <code>{real_roll}</code>"

    dice_emoji = ["🎲 1", "🎲 2", "🎲 3", "🎲 4", "🎲 5", "🎲 6"][real_roll - 1]

    await message.answer(
        f"<b>Вы выбрали:</b> {message.text}\n"
        f"<b>Кубик показал:</b> {dice_emoji}\n\n"
        f"{result}",
        reply_markup=dice_controls,
        parse_mode="HTML"
    )

@router.message(F.text == "🔙 К списку игр")
async def back_to_games(message: Message):
    await message.answer("Выберите игру:", reply_markup=games_selection)

@router.message(F.text == "🏠 В главное меню")
async def back_to_main(message: Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu)