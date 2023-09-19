from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from models.eat import users_files
from models.eat.users_files import get_operation_by_oper_id
from utils.eat.keyboards import history_ikb, EatsCallback, main_menu_kb

history_router = Router()


async def edit_page(callback: types.CallbackQuery, state: FSMContext,
                    coef_start: int, coef_end: int):
    current_data = await state.get_data()
    current_data.update({
        'page_start': current_data['page_start'] + coef_start,
        'page_end': current_data['page_end'] + coef_end
    })
    await state.update_data(current_data)
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                 message_id=callback.message.message_id,
                                                 reply_markup=history_ikb(current_data['all_user_operations'],
                                                                          current_data['page_start'],
                                                                          current_data['page_end']))


@history_router.callback_query(F.data == 'eats_operation_history')
async def get_history_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_data = await state.get_data()
    all_user_operations = await users_files.get_operations_by_tg_id(callback.from_user.id)
    current_data.update({
        'page_start': 0,
        'page_end': 5,
        'all_user_operations': all_user_operations
    })
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                 message_id=callback.message.message_id,
                                                 reply_markup=history_ikb(current_data['all_user_operations'],
                                                                          current_data['page_start'],
                                                                          current_data['page_end']))
    await state.update_data(current_data)
    await callback.answer()


@history_router.callback_query(EatsCallback.filter(F.cb_type.startswith('df')))
async def download_file_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    cb_data = EatsCallback.unpack(callback.data)
    operation = await get_operation_by_oper_id(cb_data.op_id)
    if cb_data.cb_type == 'df_v1':
        await callback.bot.send_document(chat_id=callback.from_user.id,
                                         document=operation.original_file_id)
    elif cb_data.cb_type == 'df_v2':
        await callback.bot.send_document(chat_id=callback.from_user.id,
                                         document=operation.final_file_id)
    await state.clear()
    await callback.answer()


@history_router.callback_query(F.data == 'eats_history_next')
async def next_page_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await edit_page(callback, state, 5, 5)
    await callback.answer()


@history_router.callback_query(F.data == 'eats_history_prev')
async def prev_page_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await edit_page(callback, state, -5, -5)
    await callback.answer()


@history_router.callback_query(F.data.in_(['eats_history_no_next', 'eats_history_no_prev']))
async def no_page_handler(callback: types.CallbackQuery) -> None:
    await callback.answer('Такой страницы нет')


@history_router.callback_query(F.data == 'eats_history_exit')
async def exit_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await edit_page(callback, state, -4, -5)
    await state.clear()
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                 message_id=callback.message.message_id,
                                                 reply_markup=main_menu_kb())
    await callback.answer()
