from sqlalchemy import String, Column, DateTime, JSON, select
from sqlalchemy.orm import declarative_base

from utils.database import engine, session

from datetime import datetime
from typing import Union



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    tg_id = Column(String(50), primary_key=True)
    name = Column(String(40), nullable=False)
    login = Column(String(100), nullable=True)
    data = Column(JSON(), default={})
    create_on = Column(DateTime(), nullable=False)

def create_user_model():
    Base.metadata.create_all(engine)


async def create_user(**data: dict[str, Union[str, dict]]):
    with session:
        try:
            user = User(tg_id=data['tg_id'],
                        name=data['name'],
                        login=data['login'],
                        create_on=datetime.utcnow())

            session.add(user)
            session.commit()
            return {'status': 'ok'}
        finally:
            session.close()
            return {'status': 'err', 'error': 'Ошибка на стороне БД'}


async def get_user_by_id(tg_id: str) -> Union[User, None]:
    query = select(User).where(User.tg_id == tg_id)
    result = session.scalars(query).one_or_none()
    session.close()
    return result


async def get_user_by_login(login: str) -> Union[User, None]:
    query = select(User).where(User.login == login)
    result = session.scalars(query).one_or_none()
    session.close()
    return result
