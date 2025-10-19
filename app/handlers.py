import os
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from .texts import TEXTS
from .keyboards import lang_keyboard, agree_keyboard, main_menu_kb, utils_kb, shorts_kb, aboutus_kb
from .utils import _load_users, _save_users, ensure_user, send_key_to_backend

DEV_WEBHOOK_URL = os.getenv("DEV_WEBHOOK_URL", "")
ABOUT_URL = os.getenv("ABOUT_URL", "https://example.com/about")
LOGIN_URL = os.getenv("LOGIN_URL", "https://example.com/login")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/your_support")
TON_ADDRESS = os.getenv("TON_ADDRESS", "UQ...")

router = Router()

class AddKey(StatesGroup):
    waiting_key = State()

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
    await cb.message.edit_text(TEXTS[lang]["agree_text"], reply_markup=agree_keyboard(TEXTS[lang]["agree_btn"]))
    await cb.answer()

@router.callback_query(F.data == "agree")
async def agree(cb: CallbackQuery):
    users = _load_users()
    ensure_user(users, cb.from_user.id)["consent"] = True
    _save_users(users)
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(f"<b>{Ld['main_title']}</b>\n{Ld['main_msg']}", reply_markup=main_menu_kb(Ld, ABOUT_URL, LOGIN_URL))
    await cb.answer()

@router.callback_query(F.data == "back:main")
async def back_main(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(f"<b>{Ld['main_title']}</b>\n{Ld['main_msg']}", reply_markup=main_menu_kb(Ld, ABOUT_URL, LOGIN_URL))
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
    link = Ld["invite_text"].format(bot=(await cb.bot.get_me()).username, uid=cb.from_user.id)
    await cb.message.edit_text(link, reply_markup=utils_kb(Ld, SUPPORT_URL))
    await cb.answer()

@router.callback_query(F.data == "utils:pay")
async def utils_pay(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(Ld["pay_text"].format(addr=TON_ADDRESS), reply_markup=utils_kb(Ld, SUPPORT_URL))
    await cb.answer()

@router.callback_query(F.data == "menu:shorts")
async def menu_shorts(cb: CallbackQuery):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(f"<b>{Ld['shorts']}</b>\n{Ld['shorts_text']}", reply_markup=shorts_kb(Ld))
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
    await cb.message.edit_text(Ld["enter_key"], reply_markup=aboutus_kb(Ld))
    await cb.answer()

@router.message(AddKey.waiting_key)
async def got_key(message: Message, state: FSMContext):
    users = _load_users()
    Ld = TEXTS[ensure_user(users, message.from_user.id)["lang"]]
    await message.answer(Ld["key_saved"])
    ok = await send_key_to_backend(DEV_WEBHOOK_URL, message.from_user.id, message.text.strip())
    await state.clear()
    if ok:
        await message.answer(Ld["key_ok"], reply_markup=shorts_kb(Ld))
    else:
        await message.answer(Ld["key_failed"], reply_markup=shorts_kb(Ld))

@router.callback_query(F.data == "shorts:list")
async def shorts_list(cb: CallbackQuery):
    # Ключи мы не храним тут. Показываем заглушку или позже подключим ваш API.
    users = _load_users()
    Ld = TEXTS[ensure_user(users, cb.from_user.id)["lang"]]
    await cb.message.edit_text(Ld["no_keys"], reply_markup=shorts_kb(Ld))
    await cb.answer()
