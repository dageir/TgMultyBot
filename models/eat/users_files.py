from uuid import uuid4

from sqlalchemy import String, Column, DateTime, JSON, select
from sqlalchemy.orm import declarative_base

from utils.database import engine, session

from datetime import datetime


Base = declarative_base()

# TODO написать методы для модели, протестировать модель
class UserFile(Base):
    __tablename__ = 'user_files'
    operation_id = Column(String(200), primary_key=True)
    user_tg_id = Column(String(50), nullable=False)
    original_file_id = Column(String(150), nullable=False)
    original_file_name = Column(String(100), nullable=False)
    final_file_id = Column(String(150), nullable=False)
    final_file_name = Column(String(100), nullable=False)
    created_on = Column(DateTime(), nullable=False)

    def __repr__(self):
        return f'{self.operation_id} {self.user_tg_id} {self.original_file_id} ' \
               f'{self.original_file_name} {self.final_file_id} {self.final_file_name} ' \
               f'{self.created_on}'


def create_user_file_model():
    Base.metadata.create_all(engine)


async def add_operation(**data):
    with session:
        try:
            operation = UserFile(
                operation_id=f'oper_id_{uuid4()}',
                user_tg_id=data['user_id'],
                original_file_id=data['original_file_id'],
                original_file_name=data['original_file_name'],
                final_file_id=data['final_file_id'],
                final_file_name=data['final_file_name'],
                created_on=datetime.utcnow())
            session.add(operation)
            session.commit()
            return {'status': 'ok'}
        finally:
            return {'status': 'err', 'error': 'Ошибка на стороне БД'}


async def get_operations_by_id(tg_id: str):
    query = select(UserFile).where(UserFile.user_tg_id == str(tg_id))
    result = session.scalars(query).all()
    json_res = []
    for field in result:
        json_res.append({
            'operation_id': field.operation_id,
            'or_file_id': field.original_file_id,
            'or_file_name': field.original_file_name,
            'final_file_id': field.final_file_id,
            'final_file_name': field.final_file_name,
            'created_on': field.created_on
        })
    session.close()
    return json_res
