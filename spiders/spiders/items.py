import sys

import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()


class Story(Base):
    __tablename__ = 'stories'

    stid = sqlalchemy.Column(name='stid', type_=sqlalchemy.Integer, primary_key=True)
    cost = sqlalchemy.Column(name='cost', type_=sqlalchemy.Integer)
    auth = sqlalchemy.Column(name='auth', type_=sqlalchemy.String)
    relp = sqlalchemy.Column(name='relp', type_=sqlalchemy.String)

    title = sqlalchemy.Column(name='title', type_=sqlalchemy.String)

    date_start = sqlalchemy.Column(name='date_start', type_=sqlalchemy.String)
    date_count = sqlalchemy.Column(name='date_count', type_=sqlalchemy.Integer)
    text_count = sqlalchemy.Column(name='text_count', type_=sqlalchemy.Integer)
    pict_count = sqlalchemy.Column(name='pict_count', type_=sqlalchemy.Integer)
    cmmt_count = sqlalchemy.Column(name='cmmt_count', type_=sqlalchemy.Integer)
    like_count = sqlalchemy.Column(name='like_count', type_=sqlalchemy.Integer)
    view_count = sqlalchemy.Column(name='view_count', type_=sqlalchemy.Integer)


if __name__ == '__main__':
    # Create database and tables according to input url.
    engine = sqlalchemy.create_engine(sys.argv[1])
    session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
