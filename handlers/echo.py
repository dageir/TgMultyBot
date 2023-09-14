from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

# For each module with handlers we can create a separate router.
echo_router = Router()


@echo_router.message(F.text == 'alo')
async def echo_handler(message: Message, state: FSMContext) -> None:
    try:
        # Send a copy of the received message
        print(await state.get_data())
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")