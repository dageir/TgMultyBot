from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.common.keyboards import start_menu

back_router = Router()


async def back(state: FSMContext) -> None:
    await state.clear()


@back_router.message(Command('back'))
async def back_command_handler(message: types.Message, state: FSMContext) -> None:
    await back(state=state)
    await message.answer(text='Вы вернулись в главное меню', reply_markup=start_menu())


@back_router.callback_query(F.data == 'back')
async def back_callback_data_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await back(state=state)
    await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                      message_id=callback.message.message_id)
    await callback.message.answer(text='Вы вернулись в главное меню', reply_markup=start_menu())
    await callback.answer()
