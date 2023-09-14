import asyncio
import logging

from handlers.back import back_router
from handlers.eat.convert_file import convert_file_router
from handlers.eat.operations_history import history_router
from handlers.echo import echo_router
from handlers.start import start_router
from handlers.eat.main_menu import main_menu_router

from tokens import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from models.create_all_models import create_all_models

TOKEN = BOT_TOKEN

storage = MemoryStorage()


async def main() -> None:
    await create_all_models()

    dp = Dispatcher(storage=storage)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp.include_routers(
        start_router,
        back_router,
        echo_router,
        main_menu_router,
        convert_file_router,
        history_router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
