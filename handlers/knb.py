import random
from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import games_selection, get_main_menu, rps_controls

router = Router()

# Важно: текст должен совпадать с текстом кнопок в rps_controls!
CHOICES = {
    "🪨 Камень": "🪨",
    "✂️ Ножницы": "✂️",
    "📃 Бумага": "📃"
}

WINNING_COMBINATIONS = {
    "🪨": "✂️",
    "✂️": "📃",
    "📃": "🪨"
}

@router.message(F.text == "🪨✂️📄 КНБ")
async def start_rps(message: Message):
    await message.answer(
        "Выберите свой ход:",
        reply_markup=rps_controls
    )

@router.message(F.text.in_(CHOICES.keys()))
async def play_rps(message: Message):
    user_choice_emoji = CHOICES[message.text]
    bot_choice_emoji = random.choice(list(CHOICES.values()))

    if user_choice_emoji == bot_choice_emoji:
        result = "*Ничья!* 🤝"
    elif WINNING_COMBINATIONS[user_choice_emoji] == bot_choice_emoji:
        result = "*Вы победили!* 🎉"
    else:
        result = "_Вы проиграли ХАХАХАХАХ._ 😞"

    await message.answer(
        f"*Ваш выбор:* {user_choice_emoji}\n"
        f"*Выбор бота:* {bot_choice_emoji}\n\n"
        f"{result}",
        reply_markup=rps_controls,
        parse_mode="Markdown"
    )

@router.message(F.text == "🔙 К списку игр")
async def back_to_games_rps(message: Message):
    await message.answer("Выберите игру:", reply_markup=games_selection)

@router.message(F.text == "🏠 В главное меню")
async def back_to_main_rps(message: Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu)