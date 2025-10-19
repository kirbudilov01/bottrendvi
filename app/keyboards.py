from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="English", callback_data="lang:en")],
        [InlineKeyboardButton(text="中文", callback_data="lang:zh")],
    ])

def agree_keyboard(text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="agree")]
    ])

def main_menu_kb(L, ABOUT_URL: str, LOGIN_URL: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L["about"], url=ABOUT_URL)],
        [InlineKeyboardButton(text=L["login"], url=LOGIN_URL)],
        [InlineKeyboardButton(text=L["shorts"], callback_data="menu:shorts")],
        [InlineKeyboardButton(text=L["utils"], callback_data="menu:utils")],
        [InlineKeyboardButton(text=L["about_us"], callback_data="menu:aboutus")],
    ])

def utils_kb(L, SUPPORT_URL: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L["invite"], callback_data="utils:invite")],
        [InlineKeyboardButton(text=L["pay_ton"], callback_data="utils:pay")],
        [InlineKeyboardButton(text=L["support"], url=SUPPORT_URL)],
        [InlineKeyboardButton(text=L["back"], callback_data="back:main")],
    ])

def shorts_kb(L) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L["add_key"], callback_data="shorts:add")],
        [InlineKeyboardButton(text=L["my_keys"], callback_data="shorts:list")],
        [InlineKeyboardButton(text=L["back"], callback_data="back:main")],
    ])

def aboutus_kb(L) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L["later"], callback_data="aboutus:1")],
        [InlineKeyboardButton(text=L["later"], callback_data="aboutus:2")],
        [InlineKeyboardButton(text=L["later"], callback_data="aboutus:3")],
        [InlineKeyboardButton(text=L["back"], callback_data="back:main")],
    ])

