import uuid

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from models.eat.States import FormatFile
from models.eat import users_files
from utils.eat.convert_file import convert_file_to_csv, delete_temp_file
from utils.eat.keyboards import convert_menu_ikb, main_menu_kb

convert_file_router = Router()

TEMP_PATH = 'attachments/eats/temp/'


@convert_file_router.callback_query(F.data == 'eats_convert_file')
async def convert_menu_handler(callback: types.CallbackQuery) -> None:
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                 message_id=callback.message.message_id,
                                                 reply_markup=convert_menu_ikb())
    await callback.answer()


@convert_file_router.callback_query(F.data == 'eats_convert_exit')
async def exit_handler(callback: types.CallbackQuery) -> None:
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                 message_id=callback.message.message_id,
                                                 reply_markup=main_menu_kb())
    await callback.answer()


@convert_file_router.callback_query(F.data == 'eats_convert_to_csv')
async def get_file_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FormatFile.download_file)
    await callback.message.answer(text='Пришлите файл для обработки (расширение xlsx)')
    await callback.answer()


@convert_file_router.message(FormatFile.download_file, F.content_type == 'document')
async def save_file_handler(message: types.Message, state: FSMContext) -> None:
    file_extension = message.document.file_name.split('.')[1]
    if file_extension == 'xlsx':
        try:
            await state.set_data({
                'file_id': message.document.file_id,
                'file_name': message.document.file_name.split('.')[0],
                'file': await message.bot.get_file(message.document.file_id)
            })
            await message.answer('Введи наименование выходного файла (без указания расширения)')
            # TODO Добавить проверку на отсутствие расширения в итоговом имени и наличии в нём недопустимых символов
            await state.set_state(FormatFile.name_out_file)
        except Exception as err:
            await message.answer('Произошла непредвиденная ошибка, попробуйте снова :(')
            print(err)
    else:
        await message.answer('Неправильный формат файла, ожидался "xlsx"')


@convert_file_router.message(FormatFile.download_file, F.content_type != 'document')
async def check_doc_format_handler(message: types.Message) -> None:
    await message.answer('Это не документ!')


@convert_file_router.message(FormatFile.name_out_file, F.content_type == 'text')
async def main_menu_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data({
        'out_file_name_for_user': message.text,
        'out_file_name_for_bot': uuid.uuid4()
    })
    current_data = await state.get_data()
    current_file_path = current_data['file'].file_path
    await message.bot.download_file(current_file_path, f'{TEMP_PATH}{current_data["file_id"]}.xlsx')
    result_convert = await convert_file_to_csv(file_path=f'{TEMP_PATH}{current_data["file_id"]}.xlsx',
                                               file_name=current_data['out_file_name_for_bot'])
    result_del = delete_temp_file(f'{TEMP_PATH}{current_data["file_id"]}.xlsx')
    if result_del and result_convert:
        document = FSInputFile(path=f'{TEMP_PATH}{current_data["out_file_name_for_bot"]}.csv',
                               filename=f'{current_data["out_file_name_for_user"]}.csv')
        sending_document = await message.bot.send_document(chat_id=message.chat.id,
                                                           document=document)
        delete_temp_file(f'{TEMP_PATH}{current_data["out_file_name_for_bot"]}.csv')
        await users_files.add_operation(user_id=message.from_user.id,
                                        original_file_id=current_data['file_id'],
                                        original_file_name=f'{current_data["file_name"]}.xlsx',
                                        final_file_id=sending_document.document.file_id,
                                        final_file_name=f'{current_data["out_file_name_for_user"]}.csv'
                                        )
        await state.clear()
    else:
        await message.answer('Что-то пошло не так...')


@convert_file_router.message(FormatFile.name_out_file, F.content_type != 'text')
async def check_text_format_handler(message: types.Message) -> None:
    await message.answer('Введите текст!')
