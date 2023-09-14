from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from models.eat import users_files
from utils.eat.keyboards import history_ikb, EatsCallback

history_router = Router()


async def edit_page(callback: types.CallbackQuery, state: FSMContext,
                    coef_start: int, coef_end: int):
    current_data = await state.get_data()
    current_data.update({
        'page_start': current_data['page_start'] + coef_start,
        'page_end': current_data['page_end'] + coef_end
    })
    await state.update_data(current_data)
    await callback.bot.edit_message_reply_markup(chat_id=current_data['chat_id'],
                                                 message_id=current_data['msg_id'],
                                                 reply_markup=history_ikb(current_data['all_user_operations'],
                                                                          current_data['page_start'],
                                                                          current_data['page_end']))


@history_router.callback_query(F.data == 'eats_operation_history')
async def get_history_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_data = await state.get_data()
    all_user_operations = await users_files.get_operations_by_id(callback.from_user.id)
    current_data.update({
        'page_start': 1,
        'page_end': 6,
        'all_user_operations': all_user_operations
    })

    msg = await callback.message.answer(text='text',
                                        reply_markup=history_ikb(all_user_operations,
                                                                 current_data['page_start'], current_data['page_end']))
    current_data.update({
        'chat_id': msg.chat.id,
        'msg_id': msg.message_id
    })
    await state.update_data(current_data)
    await callback.answer()


@history_router.callback_query(EatsCallback.filter(F.cb_type == 'download_file'))
async def download_file_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()


@history_router.callback_query(F.data == 'eats_history_next')
async def next_page_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await edit_page(callback, state, 4, 5)
    await callback.answer()


@history_router.callback_query(F.data == 'eats_history_prev')
async def prev_page_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await edit_page(callback, state, -4, -5)
    await callback.answer()
