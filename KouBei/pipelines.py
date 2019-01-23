# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from KouBei.settings import MYSQL_HOST, MYSQL_DATABASE, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD


class KouBeiTemplate():
    '''
        数据表detail的映射类
    '''
    id = Column(Integer, primary_key=True)
    energy_consump = Column(String(100))
    gas_consump = Column(String(100))
    apperance = Column(String(100))
    bought_city_name = Column(String(100))
    bought_city = Column(String(100))
    bought_date = Column(String(100))
    bought_place = Column(String(100))
    bought_province = Column(String(100))
    car_owner_levels = Column(String(100))
    comfort = Column(String(100))
    comment_count = Column(String(100))
    economy = Column(String(100))
    cost_efficiency = Column(String(100))
    post_at = Column(String(100))
    odometer = Column(String(100))
    content = Column(String(10000))
    summary = Column(String(1000))
    helpful_count = Column(String(100))
    interior = Column(String(100))
    modified_at = Column(String(100))
    maneuver = Column(String(100))
    nick_name = Column(String(100))
    power = Column(String(100))
    price = Column(String(100))
    series_id = Column(String(100))
    show_id = Column(String(100))
    space = Column(String(100))
    spec = Column(String(100))
    spec_id = Column(String(100))
    user_id = Column(String(100))
    visit_count = Column(String(100))
    brand = Column(String(100))
    series = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    content_id = Column(Integer)

    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])


class SqlAlachemyPipeline(object):
    '''
        __init__:通过sqlalchemy连接mysql数据库，并将数据表与其对应的类连接起来
        process_item:将每个爬虫产生的item，在判断过数据表是否存在后，存入数据表
    '''
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DATABASE))
        self.session=sessionmaker(bind=self.engine)
        self.sess=self.session()
        Base = declarative_base()
        self.Article = type('detail',(Base,KouBeiTemplate),{'__tablename__':'detail'})

    def process_item(self,item,spider):
        result = self.sess.query(self.Article).filter_by(modified_at=item['modified_at']).first()
        if result:
            pass
        else:
            self.sess.add(self.Article(**item))
            self.sess.commit()

    def close_spider(self, spider):
        self.sess.close()
