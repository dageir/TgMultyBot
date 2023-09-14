from models.eat.users_files import create_user_file_model
from models.common.users import create_user_model

async def create_all_models():
    create_user_model()
    create_user_file_model()