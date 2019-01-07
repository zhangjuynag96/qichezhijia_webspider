# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from KouBei.settings import MYSQL_HOST, MYSQL_DATABASE, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD


class KouBeiTemplate():
    id = Column(Integer, primary_key=True)
    actual_battery_consumption = Column(String(100))
    actual_oil_consumption = Column(String(100))
    apperance = Column(String(100))
    boughtCityName = Column(String(100))
    bought_city = Column(String(100))
    bought_date = Column(String(100))
    bought_place = Column(String(100))
    bought_province = Column(String(100))
    carOwnerLevels = Column(String(100))
    comfortableness = Column(String(100))
    commentCount = Column(String(100))
    consumption = Column(String(100))
    cost_efficient = Column(String(100))
    created = Column(String(100))
    driven_kilometers = Column(String(100))
    feeling = Column(String(10000))
    feeling_summary = Column(String(1000))
    helpfulCount = Column(String(100))
    interior = Column(String(100))
    last_edit = Column(String(100))
    maneuverability = Column(String(100))
    nickName = Column(String(100))
    power = Column(String(100))
    price = Column(String(100))
    seriesId = Column(String(100))
    showId = Column(String(100))
    space = Column(String(100))
    specName = Column(String(100))
    specid = Column(String(100))
    userid = Column(String(100))
    visitCount = Column(String(100))
    BrandName = Column(String(100))
    SeriesName = Column(String(100))

    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])


class SqlAlachemyPipeline(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'.format(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DATABASE),echo=True)
        self.session=sessionmaker(bind=self.engine)
        self.sess=self.session()
        Base = declarative_base()
        self.Article = type('detail',(Base,KouBeiTemplate),{'__tablename__':'detail'})

    def process_item(self,item,spider):
        result = self.sess.query(self.Article).filter_by(last_edit=item['last_edit']).first()
        if result:
            pass
        else:
            self.sess.add(self.Article(**item))
            self.sess.commit()

    def close_spider(self, spider):
        self.sess.close()
