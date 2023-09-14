from aiogram.fsm.state import StatesGroup, State


class FormatFile(StatesGroup):
    download_file = State()
    name_out_file = State()
    upload_file = State()
    status = State()
