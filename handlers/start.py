from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models.common import users as user
from utils.common.keyboards import start_menu

start_router = Router()


@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    if await user.get_user_by_id(str(message.from_user.id)) is None:
        await user.create_user(tg_id=str(message.from_user.id),
                               name=str(message.from_user.full_name),
                               login=str(message.from_user.username))
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>", reply_markup=start_menu())
