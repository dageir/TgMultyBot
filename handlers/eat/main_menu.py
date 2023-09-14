from aiogram import Router, types
from aiogram.filters import Command

from utils.eat.keyboards import main_menu_kb

main_menu_router = Router()


@main_menu_router.message(Command('Eats'))
async def main_menu_handler(message: types.Message) -> None:
    await message.chat.bot.send_photo(chat_id=message.chat.id,
                                      reply_markup=main_menu_kb,
                                      photo='https://play.google.com/store/apps/details?id=ru.foodfox.client&hl=ru')
