import scrapy_sqlitem
import sqlalchemy.orm

from spiders.settings import SQLITE_DB_NAME

Base = sqlalchemy.orm.declarative_base()


def get_engine():
    return sqlalchemy.create_engine('sqlite:///' + SQLITE_DB_NAME, encoding='utf-8')


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


class HowToItem(scrapy_sqlitem.SqlItem, metaclass=scrapy_sqlitem.sqlitem.SqlAlchemyItemMeta):
    sqlmodel = sqlalchemy.Table('how_to', get_metadata(),
                                sqlalchemy.Column(name='hstid', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='h_tag', type_=sqlalchemy.String))


class CityItem(scrapy_sqlitem.SqlItem, metaclass=scrapy_sqlitem.sqlitem.SqlAlchemyItemMeta):
    sqlmodel = sqlalchemy.Table('cities', get_metadata(),
                                sqlalchemy.Column(name='ctid', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='name', type_=sqlalchemy.String),
                                sqlalchemy.Column(name='prov', type_=sqlalchemy.String))


class ScenicItem(scrapy_sqlitem.SqlItem, metaclass=scrapy_sqlitem.sqlitem.SqlAlchemyItemMeta):
    sqlmodel = sqlalchemy.Table('scenics', get_metadata(),
                                sqlalchemy.Column(name='scid', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='name', type_=sqlalchemy.String),
                                sqlalchemy.Column(name='city', type_=sqlalchemy.String),

                                sqlalchemy.Column(name='lng', type_=sqlalchemy.Float),
                                sqlalchemy.Column(name='lat', type_=sqlalchemy.Float))


class VisitItem(scrapy_sqlitem.SqlItem, metaclass=scrapy_sqlitem.sqlitem.SqlAlchemyItemMeta):
    sqlmodel = sqlalchemy.Table('visits', get_metadata(),
                                sqlalchemy.Column(name='vstid', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='index', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='vscid', type_=sqlalchemy.Integer),
                                sqlalchemy.Column(name='vctid', type_=sqlalchemy.Integer))


StoryItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
HowToItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
VisitItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
ScenicItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
CityItem.sqlmodel.create(bind=get_engine(), checkfirst=True)
