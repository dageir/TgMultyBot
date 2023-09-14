from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from tokens import DATABASE_PASS

database_name = 'tg_bot'
host = 'localhost'

engine = create_engine(f'postgresql://postgres:{DATABASE_PASS}@{host}/{database_name}')

connection = engine.connect()

session = Session(engine)





