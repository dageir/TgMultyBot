from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from utils.common.universal_buttons import back_ik_button


class EatsCallback(CallbackData, prefix='eats'):
    cb_type: str
    op_id: str


convert_btn = InlineKeyboardButton(text='Convert file', callback_data='eats_convert_file')
history = InlineKeyboardButton(text='history', callback_data='eats_operation_history')


def main_menu_kb() -> InlineKeyboardMarkup:
    main_menu = InlineKeyboardMarkup(inline_keyboard=[
        [convert_btn],
        [history],
        [back_ik_button]
    ])
    return main_menu


def convert_menu_ikb() -> InlineKeyboardMarkup:
    to_csv_btn = InlineKeyboardButton(text='To csv', callback_data='eats_convert_to_csv')
    exit_btn = InlineKeyboardButton(text='Назад', callback_data='eats_convert_exit')
    convert_menu = InlineKeyboardMarkup(inline_keyboard=[
        [to_csv_btn],
        [exit_btn]
    ])
    return convert_menu


def history_ikb(data: list[dict], page_start: int, page_end: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page_end > len(data):
        page_end = len(data)
    for i in range(page_start, page_end):
        builder.button(text=data[i]['or_file_name'],
                       callback_data=EatsCallback(cb_type='df_v1', op_id=data[i]['operation_id']))
        builder.button(text=data[i]['final_file_name'],
                       callback_data=EatsCallback(cb_type='df_v2', op_id=data[i]['operation_id']))

    if page_start != 0:
        builder.button(text='<<', callback_data='eats_history_prev')
    else:
        builder.button(text='<<', callback_data='eats_history_no_prev')
    if page_end < len(data):
        builder.button(text='>>', callback_data='eats_history_next')
    else:
        builder.button(text='>>', callback_data='eats_history_no_next')

    builder.button(text='Назад', callback_data='eats_history_exit')
    builder.adjust(2)
    return builder.as_markup()
