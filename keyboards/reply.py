from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Профиль пользователя")],
        [KeyboardButton(text="🎲 Игровой раздел")],
        [KeyboardButton(text="👑 Принцессы Диснея")],
        [KeyboardButton(text="📋 Информация")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие..."
)

games_selection = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪨✂️📄 КНБ")],
        [KeyboardButton(text="🎯 Угадай число")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите игру..."
)

rps_controls = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🪨 Камень"),
            KeyboardButton(text="✂️ Ножницы"),
            KeyboardButton(text="📃 Бумага")
        ],
        [KeyboardButton(text="🔙 К списку игр")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Ваш ход..."
)

dice_controls = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎲 1"),
            KeyboardButton(text="🎲 2"),
            KeyboardButton(text="🎲 3")
        ],
        [
            KeyboardButton(text="🎲 4"),
            KeyboardButton(text="🎲 5"),
            KeyboardButton(text="🎲 6")
        ],
        [KeyboardButton(text="🔙 К списку игр")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Ваше предположение..."
)

# Алиасы для обратной совместимости со старым кодом
central_navigation = get_main_menu
main_menu = get_main_menu
games_menu = games_selection
rps_menu = rps_controls
dice_menu = dice_controls