import scrapy_sqlitem
import sqlalchemy.orm

from spiders.settings import DATABASE_URL

Base = sqlalchemy.orm.declarative_base()


def get_engine():
    return sqlalchemy.create_engine(DATABASE_URL, encoding='utf-8')


def get_metadata():
    return sqlalchemy.MetaData(get_engine())


class StoryItem(scrapy_sqlitem.SqlItem, metaclass=scrapy_sqlitem.sqlitem.SqlAlchemyItemMeta):
    sqlmodel = sqlalchemy.Table('stories', get_metadata(),

                                sqlalchemy.Column(name='stid', type_=sqlalchemy.Integer, primary_key=True),
                                sqlalchemy.Column(name='cost', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='auth', type_=sqlalchemy.String),
                                sqlalchemy.Column(name='relp', type_=sqlalchemy.String),
                                sqlalchemy.Column(name='loct', type_=sqlalchemy.String),

                                sqlalchemy.Column(name='title', type_=sqlalchemy.String),

                                sqlalchemy.Column(name='date_start', type_=sqlalchemy.String),
                                sqlalchemy.Column(name='date_count', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='text_count', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='pict_count', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='cmmt_count', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='like_count', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='view_count', type_=sqlalchemy.Integer))


StoryItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
