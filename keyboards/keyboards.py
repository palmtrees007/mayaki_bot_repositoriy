from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from LEXICON import btns_clbks


inline_rht_btn = InlineKeyboardButton(text='>>', callback_data=btns_clbks['rht_btn'])
inline_lft_btn = InlineKeyboardButton(text='<<', callback_data=btns_clbks['lft_btn'])
inline_to_know_btn = InlineKeyboardButton(text='Узнать больше', callback_data=btns_clbks['to_know_btn'])
inline_back_btn = InlineKeyboardButton(text='Назад', callback_data=btns_clbks['back_btn'])
inline_his_btn = InlineKeyboardButton(text='История маяка', callback_data=btns_clbks['his_btn'])
inline_arrangement_btn = InlineKeyboardButton(text='Устройство ламп', callback_data=btns_clbks['argnt_btn'])
inline_mayaki_btn = InlineKeyboardButton(text='Про историю маяков', callback_data=btns_clbks['mayaki_btn'])
inline_menu_btn = InlineKeyboardButton(text='Назад', callback_data=btns_clbks['menu_btn'])


def PaginationKeyboard(url: str | None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not url is None:
        adress = InlineKeyboardButton(text='На карте', url=url)
    builder.row(inline_lft_btn, inline_to_know_btn, inline_rht_btn, width=3)
    if not url is None:
        builder.row(adress, width=1)
    builder.row(inline_menu_btn)
    return builder.as_markup()
    

def PaginationKbForHis(page) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    page_btn = InlineKeyboardButton(text=str(page), callback_data='pass')
    builder.row(inline_back_btn, width=1)
    builder.row(inline_lft_btn, page_btn, inline_rht_btn, width=3)
    return builder.as_markup()

def StartKb():
    builder = InlineKeyboardBuilder()
    builder.row(inline_mayaki_btn, inline_arrangement_btn, width=1)
    return builder.as_markup()
