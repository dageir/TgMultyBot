from typing import Union

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.common.keyboards import start_menu

back_router = Router()


async def back(state: FSMContext, ret: Union[types.Message, types.CallbackQuery]) -> None:
    await state.clear()


@back_router.message(Command('back'))
async def back_command_handler(message: types.Message, state: FSMContext) -> None:
    await back(ret=message, state=state)
    await message.answer(text='Вы вернулись в главное меню', reply_markup=start_menu())


@back_router.callback_query(F.data == 'back')
async def back_callback_data_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await back(ret=callback, state=state)
    await callback.message.answer(text='Вы вернулись в главное меню', reply_markup=start_menu())
    await callback.answer()
