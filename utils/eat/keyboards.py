from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from utils.common.universal_buttons import back_ik_button


class EatsCallback(CallbackData, prefix='eats'):
    cb_type: str
    op_id: str


convert_btn = InlineKeyboardButton(text='Convert file', callback_data='eats_convert_file')
history = InlineKeyboardButton(text='history', callback_data='eats_operation_history')


main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [convert_btn],
    [history],
    [back_ik_button]
])

# TODO добавить кнопку "Выход" для удаления сообщения и завершения сессии
def history_ikb(data: list[dict], page_start: int, page_end: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page_end > len(data):
        page_end = len(data)
    for i in range(page_start, page_end):
        builder.button(text=data[i]['or_file_name'],
                       callback_data=EatsCallback(cb_type='df_v1', op_id=data[i]['operation_id']))
        builder.button(text=data[i]['final_file_name'],
                       callback_data=EatsCallback(cb_type='df_v2', op_id=data[i]['operation_id']))
    if page_start != 1:
        builder.button(text='<<', callback_data='eats_history_prev')
    if page_end < len(data):
        builder.button(text='>>', callback_data='eats_history_next')
    builder.adjust(2)
    return builder.as_markup()
