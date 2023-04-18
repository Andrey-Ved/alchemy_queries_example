import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import alchemy_queries_example.models as models


def clear_db(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    con = engine.connect()
    trans = con.begin()
    for table in meta.sorted_tables:
        con.execute(table.delete())
    trans.commit()


DATABASE_NAME_ORM = 'sqlite_orm.db'
DSN_ORM = f'sqlite:///{DATABASE_NAME_ORM}'

print('Connecting to DB...')

engine_orm = sa.create_engine(DSN_ORM)
Session_ORM = sessionmaker(bind=engine_orm)
session_orm = Session_ORM()

models.Base.metadata.create_all(engine_orm)

print('Clearing the bases...')
clear_db(engine_orm)
