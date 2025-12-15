import os
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from .texts import TEXTS
from .keyboards import (
    lang_keyboard,
    agree_keyboard,
    main_menu_kb,
    utils_kb,
    shorts_kb,
    aboutus_kb,
)
from .utils import _load_users, _save_users, ensure_user

# === LINKS from .env ===
# RU
ABOUT_URL_RU = os.getenv("ABOUT_URL_RU", "https://trendvi.ru")
LOGIN_URL_RU = os.getenv("LOGIN_URL_RU", "https://app.trendvi.ru")

# INT (EN/ZH)
ABOUT_URL_INT = os.getenv("ABOUT_URL_INT", "https://trendvi.media")
LOGIN_URL_INT = os.getenv("LOGIN_URL_INT", "https://app.trendvi.media")

SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/fabricbotsupport")

router = Router()

class AddKey(StatesGroup):
    waiting_key = State()

def resolve_urls_by_lang(lang: str):
    """Возвращает (about_url, login_url) для заданного языка."""
    if lang == "ru":
        return ABOUT_URL_RU, LOGIN_URL_RU
    return ABOUT_URL_INT, LOGIN_URL_INT

def L(users, uid, key):
    lang = ensure_user(users, uid).get("lang", "ru")
    return TEXTS.get(lang, TEXTS["ru"])[key]

@router.message(CommandStart())
async def cmd_start(message: Message):
    users = _load_users()
    ensure_user(users, message.from_user.id)
    await message.answer(TEXTS["ru"]["choose_lang"], reply_markup=lang_keyboard())

@router.callback_query(F.data.startswith("lang:"))
async def set_lang(cb: CallbackQuery):
    users = _load_users()
    lang = cb.data.split(":", 1)[1]
    ensure_user(users, cb.from_user.id)["lang"] = lang
    _save_users(users)
    await cb.message.edit_text(
        TEXTS[lang]["agree_text"],
        reply_markup=agree_keyboard(TEXTS[lang]["agree_btn"]),
    )
    await cb.answer()

@router.callback_query(F.data == "agree")
async def agree(cb: CallbackQuery):
    users = _load_users()
    ensure_user(users, cb.from_user.id)["consent"] = True
    _save_users(users)
    lang = ensure_user(users, cb.from_user.id)["lang"]
    Ld = TEXTS[lang]
    about_url, login_url = resolve_urls_by_lang(lang)
    await cb.message.edit_text(
        f"<b>{Ld['main_title']}</b>\n{Ld['main_msg']}",
        reply_markup=main_menu_kb(Ld, about_url, login_url),
    )
    await cb.answer()

@router.callback_query(F.data == "back:main")
async def back_main(cb: CallbackQuery):
    users = _load_users()
    lang = ensure_user(users, cb.from_user.id)["lang"]
    Ld = TEXTS[lang]
    about_url, login_url = resolve_urls_by_lang(lang)
    await cb.message.edit_text(
        f"<b>{Ld['main_title']}</b>\n{Ld['main_msg']}",
        reply_markup=main_menu_kb(Ld, about_url, login_url),
    )
    await cb.answer()

@router.callback_query(F.data == "menu:utils")
async def menu_utils(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(Ld["utils"], reply_markup=utils_kb(Ld, SUPPORT_URL))
    await cb.answer()

@router.callback_query(F.data == "utils:invite")
async def utils_invite(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    link = Ld["invite_text"].format(
        bot=(await cb.bot.get_me()).username, uid=cb.from_user.id
    )
    await cb.message.edit_text(link, reply_markup=utils_kb(Ld, SUPPORT_URL))
    await cb.answer()

@router.callback_query(F.data == "menu:myid")
async def menu_myid(cb: CallbackQuery):
    users = _load_users()
    lang = ensure_user(users, cb.from_user.id)["lang"]
    Ld = TEXTS[lang]

    await cb.message.edit_text(
        Ld["my_id_text"].format(id=cb.from_user.id),
        reply_markup=main_menu_kb(
            Ld,
            *resolve_urls_by_lang(lang),
        ),
    )
    await cb.answer()

@router.callback_query(F.data == "utils:pay")
async def utils_pay(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    # Просто текст без TON-кошелька:
    await cb.message.edit_text(Ld["pay_text"], reply_markup=utils_kb(Ld, SUPPORT_URL))
    await cb.answer()

@router.callback_query(F.data == "menu:shorts")
async def menu_shorts(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(
        f"<b>{Ld['shorts']}</b>\n{Ld['shorts_text']}",
        reply_markup=shorts_kb(Ld),
    )
    await cb.answer()

@router.callback_query(F.data == "menu:aboutus")
async def menu_aboutus(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(Ld["about_us"], reply_markup=aboutus_kb(Ld))
    await cb.answer()

@router.callback_query(F.data == "shorts:add")
async def shorts_add(cb: CallbackQuery, state: FSMContext):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await state.set_state(AddKey.waiting_key)
    # используем aboutus_kb(Ld) как клавиатуру с кнопкой «Назад»
    await cb.message.edit_text(Ld["enter_key"], reply_markup=aboutus_kb(Ld))
    await cb.answer()

@router.message(AddKey.waiting_key)
async def got_key(message: Message, state: FSMContext):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, message.from_user.id)["lang"]]
    # Бэкенда нет — просто сообщаем, что ключ принят
    await message.answer(Ld["key_saved"])
    await state.clear()
    await message.answer(Ld["key_ok"], reply_markup=shorts_kb(Ld))

@router.callback_query(F.data == "shorts:list")
async def shorts_list(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(Ld["no_keys"], reply_markup=shorts_kb(Ld))
    await cb.answer()
