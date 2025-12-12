import logging
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.reply import get_main_menu

router = Router()

@dataclass
class DisneyPrincess:
    """Информация о принцессе Диснея"""
    display_name: str
    description: str
    princess_id: str

# Статичные описания принцесс
DISNEY_PRINCESSES = [
    DisneyPrincess(
        "Золушка",
        "Золушка — добрая и трудолюбивая девушка, которая, несмотря на тяготы жизни с мачехой и сводными сёстрами, сохранила доброе сердце. С помощью крестной феи она попадает на королевский бал, где встречает принца. Потеряв хрустальную туфельку, она даёт принцу шанс её найти. В итоге принц находит Золушку, и они женятся.",
        "cinderella"
    ),
    DisneyPrincess(
        "Рапунцель",
        "Рапунцель — принцесса с волшебными золотистыми волосами, обладающими целебной силой. В детстве её похитила матушка Готель, которая спрятала её в высокой башне. Рапунцель мечтает увидеть мир и особенно летающие фонарики, которые появляются в день её рождения. С помощью вора Флина Райдера ей удаётся сбежать и узнать правду о своём происхождении.",
        "rapunzel"
    ),
    DisneyPrincess(
        "Ариэль (Русалочка)",
        "Ариэль — младшая дочь короля Тритона, русалка, которая мечтает о жизни на земле. Она влюбляется в принца Эрика и заключает сделку с морской ведьмой Урсулой, чтобы стать человеком. В обмен на голос Ариэль получает ноги, но должна поцеловать Эрика за три дня. Несмотря на козни Урсулы, любовь побеждает, и Ариэль навсегда остаётся с Эриком.",
        "ariel"
    ),
    DisneyPrincess(
        "Бель (Красавица и Чудовище)",
        "Бель — умная, начитанная девушка, которая живёт в маленькой французской деревне. Чтобы спасти отца, она соглашается жить в замке у Чудовища. Со временем Бель видит в нём добрую душу и влюбляется, разрушая проклятие. Чудовище превращается обратно в принца Адама, и они живут долго и счастливо.",
        "belle"
    ),
    DisneyPrincess(
        "Аврора (Спящая красавица)",
        "Аврора — принцесса, над которой злая фея Малефисента наложила проклятие: в свой шестнадцатый день рождения она уколется веретеном и уснёт вечным сном. Три добрые феи прячут её в лесу, воспитывая под именем Розочка. В день рождения Аврора встречает принца Филиппа, но проклятие сбывается. Только поцелуй истинной любви может её разбудить.",
        "aurora"
    ),
    DisneyPrincess(
        "Мулан",
        "Мулан — храбрая девушка, которая, чтобы спасти своего больного отца, выдаёт себя за мужчину и отправляется на войну вместо него. Проявив смекалку и отвагу, она становится героем армии и спасает Китай от захватчиков. Мулан доказывает, что героем может быть каждый, независимо от пола.",
        "mulan"
    ),
    DisneyPrincess(
        "Жасмин",
        "Жасмин — принцесса Аграбы, которая устала от дворцовой жизни и хочет свободы. Она сбегает из дворца и встречает Аладдина, простого вора, который с помощью джина пытается завоевать её сердце. Жасмин ценит искренность и смелость, и в итоге выбирает любовь, а не богатство.",
        "jasmine"
    ),
    DisneyPrincess(
        "Покахонтас",
        "Покахонтас — дочь вождя индейского племени, которая верит в гармонию с природой. Она знакомится с английским колонизатором Джоном Смитом и учит его видеть красоту в окружающем мире. Покахонтас становится мостом между двумя культурами, предотвращая конфликт.",
        "pocahontas"
    ),
    DisneyPrincess(
        "Эльза (Холодное сердце)",
        "Эльза — королева Эренделла, обладающая магической силой создавать лёд и снег. Из-за страха навредить другим, она скрывает свои способности. После случайного проклятия королевства вечной зимой, Эльза сбегает в горы. Её сестра Анна помогает ей понять, что настоящая сила в любви, а не в страхе.",
        "elsa"
    ),
    DisneyPrincess(
        "Анна (Холодное сердце)",
        "Анна — младшая сестра Эльзы, весёлая, оптимистичная и преданная. После того как Эльза сбегает, Анна отправляется в опасное путешествие, чтобы найти её и спасти королевство. По пути она встречает Кристоффа, оленя Свена и снеговика Олафа. Анна доказывает, что истинная любовь — это не только романтические чувства, но и любовь к семье.",
        "anna"
    ),
    DisneyPrincess(
        "Моана",
        "Моана — дочь вождя островного племени, которая с детства чувствует зов океана. Когда её острову угрожает опасность, она отправляется в опасное путешествие через океан, чтобы найти полубога Мауи и вернуть сердце богини Те Фити. Моана становится первым мореплавателем своего народа за тысячу лет.",
        "moana"
    ),
    DisneyPrincess(
        "Тиана (Принцесса и лягушка)",
        "Тиана — трудолюбивая официантка из Нового Орлеана, которая мечтает открыть собственный ресторан. Встретив принца Навина, превращённого в лягушку, она сама становится лягушкой после поцелуя. Вместе они отправляются в путешествие по болотам, чтобы найти способ стать людьми. Тиана учится, что мечты сбываются, но важно не забывать о любви и семье.",
        "tiana"
    )
]

class ReadingSession:
    """Управление состоянием чтения для пользователя"""
    def __init__(self):
        self.current_princess_idx = 0
        self.current_segment = 0
        self.saved_position: Optional[Tuple[int, int]] = None

    def set_position(self, princess_idx: int, segment: int = 0):
        self.current_princess_idx = princess_idx
        self.current_segment = segment

    def save_bookmark(self):
        self.saved_position = (self.current_princess_idx, self.current_segment)

    def load_bookmark(self) -> Optional[Tuple[int, int]]:
        return self.saved_position

reading_sessions: Dict[int, ReadingSession] = {}

def prepare_markdown_text(raw_text: str) -> str:
    """Экранирование специальных символов для MarkdownV2"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    for char in escape_chars:
        raw_text = raw_text.replace(char, f'\\{char}')
    return raw_text

def segment_content(content: str, segment_size: int = 1200) -> list:
    """Разбивка текста на удобные для чтения сегменты"""
    segments = []

    while len(content) > segment_size:
        break_point = content.rfind('. ', 0, segment_size)
        if break_point == -1:
            break_point = content.rfind(' ', 0, segment_size)
        if break_point == -1:
            break_point = segment_size

        segments.append(content[:break_point].strip())
        content = content[break_point:].lstrip()

    if content:
        segments.append(content)

    return segments

def generate_navigation_buttons(
    princess_index: int,
    segment_idx: int,
    total_segments: int,
    has_bookmark: bool
) -> InlineKeyboardMarkup:
    """Создание навигационной клавиатуры"""
    navigation_buttons = []

    segment_nav = []
    if segment_idx > 0:
        segment_nav.append(InlineKeyboardButton(
            text="◀️ Предыдущая часть",
            callback_data=f"segment:prev:{princess_index}:{segment_idx}"
        ))

    if segment_idx + 1 < total_segments:
        segment_nav.append(InlineKeyboardButton(
            text="Следующая часть ▶️",
            callback_data=f"segment:next:{princess_index}:{segment_idx}"
        ))

    if segment_nav:
        navigation_buttons.append(segment_nav)

    princess_nav = []
    if princess_index > 0:
        princess_nav.append(InlineKeyboardButton(
            text="⏪ Предыдущая принцесса",
            callback_data=f"princess:prev:{princess_index}"
        ))

    if princess_index + 1 < len(DISNEY_PRINCESSES):
        princess_nav.append(InlineKeyboardButton(
            text="Следующая принцесса ⏩",
            callback_data=f"princess:next:{princess_index}"
        ))

    if princess_nav:
        navigation_buttons.append(princess_nav)

    bookmark_button = [InlineKeyboardButton(
        text="👑 Вернуться к закладке" if has_bookmark else "💎 Сохранить позицию",
        callback_data="bookmark:restore" if has_bookmark else "bookmark:save"
    )]
    navigation_buttons.append(bookmark_button)

    navigation_buttons.append([
        InlineKeyboardButton(
            text="↩️ В главное меню",
            callback_data="navigation:main_menu"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=navigation_buttons)

async def display_princess_article(
    interaction: Message | CallbackQuery,
    user_identifier: int,
    princess_idx: int,
    segment_idx: int = 0
):
    """Отображение статьи о принцессе"""
    if not 0 <= princess_idx < len(DISNEY_PRINCESSES):
        error_msg = "🎀 Вы просмотрели всех диснеевских принцесс!"
        if isinstance(interaction, Message):
            await interaction.answer(error_msg, reply_markup=get_main_menu)
        else:
            await interaction.message.edit_text(error_msg)
            await interaction.answer()

        reading_sessions.pop(user_identifier, None)
        return

    princess = DISNEY_PRINCESSES[princess_idx]
    session = reading_sessions.get(user_identifier)

    if not session or session.current_princess_idx != princess_idx:
        session = ReadingSession()
        session.set_position(princess_idx, segment_idx)
        reading_sessions[user_identifier] = session

    content_segments = segment_content(princess.description)

    if segment_idx >= len(content_segments):
        segment_idx = len(content_segments) - 1

    current_segment = content_segments[segment_idx]
    total_segments = len(content_segments)

    safe_title = prepare_markdown_text(princess.display_name)
    safe_content = prepare_markdown_text(current_segment)

    message_template = (
        f"*👑 {safe_title}*\n"
        f"_Часть {segment_idx + 1} из {total_segments}_\n\n"
        f"{safe_content}"
    )

    has_saved_bookmark = session.saved_position is not None
    navigation = generate_navigation_buttons(
        princess_idx, segment_idx,
        total_segments, has_saved_bookmark
    )

    if isinstance(interaction, Message):
        await interaction.answer(message_template, reply_markup=navigation, parse_mode="MarkdownV2")
    else:
        await interaction.message.edit_text(message_template, reply_markup=navigation, parse_mode="MarkdownV2")
        await interaction.answer()

@router.message(F.text == "👑 Принцессы Диснея")
async def launch_disney_library(message: Message):
    """Запуск энциклопедии принцесс Диснея"""
    user_identifier = message.from_user.id

    reading_sessions[user_identifier] = ReadingSession()

    welcome_text = (
        "✨ *Мир Принцесс Диснея*\n\n"
        "Откройте для себя истории, характер и приключения "
        "ваших любимых диснеевских принцесс!\n\n"
        "Всего принцесс: *{}*\n"
        "Используйте кнопки для навигации.\n\n"
        "_Загружаю информацию о первой принцессе..._"
    ).format(len(DISNEY_PRINCESSES))

    await message.answer(
        prepare_markdown_text(welcome_text),
        parse_mode="MarkdownV2"
    )

    await display_princess_article(message, user_identifier, 0)

@router.callback_query(F.data.startswith("segment:"))
async def handle_segment_navigation(callback: CallbackQuery):
    """Обработка навигации между сегментами"""
    try:
        _, action, princess_idx, seg_idx = callback.data.split(":")
        princess_idx, seg_idx = int(princess_idx), int(seg_idx)
        user_id = callback.from_user.id

        session = reading_sessions.get(user_id)
        if not session:
            await callback.answer("Сессия устарела. Начните заново.", show_alert=True)
            return

        princess = DISNEY_PRINCESSES[princess_idx]
        segments = segment_content(princess.description)

        if action == "next" and seg_idx + 1 < len(segments):
            session.set_position(princess_idx, seg_idx + 1)
            await display_princess_article(callback, user_id, princess_idx, seg_idx + 1)
        elif action == "prev" and seg_idx > 0:
            session.set_position(princess_idx, seg_idx - 1)
            await display_princess_article(callback, user_id, princess_idx, seg_idx - 1)
        else:
            await callback.answer(
                "Это крайний сегмент в этой статье.",
                show_alert=True
            )

    except Exception as error:
        logging.error(f"Ошибка навигации: {error}")
        await callback.answer("Ошибка при переключении.", show_alert=True)

@router.callback_query(F.data.startswith("princess:"))
async def handle_princess_navigation(callback: CallbackQuery):
    """Обработка навигации между принцессами"""
    try:
        _, action, princess_idx = callback.data.split(":")
        princess_idx = int(princess_idx)
        user_id = callback.from_user.id

        session = reading_sessions.get(user_id)
        if not session:
            await callback.answer("Сессия устарела. Начните заново.", show_alert=True)
            return

        if action == "next" and princess_idx + 1 < len(DISNEY_PRINCESSES):
            session.set_position(princess_idx + 1, 0)
            await display_princess_article(callback, user_id, princess_idx + 1, 0)
        elif action == "prev" and princess_idx > 0:
            session.set_position(princess_idx - 1, 0)
            await display_princess_article(callback, user_id, princess_idx - 1, 0)
        else:
            await callback.answer(
                "Это крайняя принцесса в списке.",
                show_alert=True
            )

    except Exception as error:
        logging.error(f"Ошибка переключения принцесс: {error}")
        await callback.answer("Ошибка при переключении.", show_alert=True)

@router.callback_query(F.data == "bookmark:save")
async def save_reading_position(callback: CallbackQuery):
    """Сохранение текущей позиции как закладки"""
    user_id = callback.from_user.id
    session = reading_sessions.get(user_id)

    if session:
        session.save_bookmark()
        await callback.answer("💎 Позиция сохранена!", show_alert=True)
    else:
        await callback.answer("Нет активной сессии.", show_alert=True)

@router.callback_query(F.data == "bookmark:restore")
async def restore_bookmark_position(callback: CallbackQuery):
    """Восстановление позиции из закладки"""
    user_id = callback.from_user.id
    session = reading_sessions.get(user_id)

    if session and session.saved_position:
        princess_idx, seg_idx = session.saved_position
        session.set_position(princess_idx, seg_idx)
        await display_princess_article(callback, user_id, princess_idx, seg_idx)
    else:
        await callback.answer("Сохранённая позиция отсутствует.", show_alert=True)

@router.callback_query(F.data == "navigation:main_menu")
async def return_to_main_interface(callback: CallbackQuery):
    """Возврат в главное меню"""
    user_id = callback.from_user.id
    reading_sessions.pop(user_id, None)

    await callback.message.edit_text(
        prepare_markdown_text("Возвращаемся в главное меню..."),
        parse_mode="MarkdownV2"
    )

    await callback.message.answer(
        "🏠 Главное меню:",
        reply_markup=get_main_menu
    )
    await callback.answer()

@router.message(F.text == "🏠 Главное меню")
async def navigate_to_main(message: Message):
    """Возврат в главное меню из любого места"""
    user_id = message.from_user.id
    reading_sessions.pop(user_id, None)
    await message.answer("Главное меню:", reply_markup=get_main_menu)