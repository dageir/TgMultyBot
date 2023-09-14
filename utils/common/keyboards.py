from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from utils.common.universal_buttons import back_button


def start_menu() -> ReplyKeyboardMarkup:
    kb =ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='/Eats')],
            [back_button]
        ],
        resize_keyboard=True
    )
    return kb

