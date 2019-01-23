# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class AutohomeKoubeiViewItem(Item):
    collection = table =  'detail'

    energy_consump = Field()  #百公里耗电
    gas_consump = Field()   #百公里耗油
    apperance = Field()    #车辆外观评分
    bought_city_name = Field()    #车辆购买城市
    bought_city = Field()
    bought_date = Field()        #购买时间
    bought_place = Field()
    bought_province = Field()
    car_owner_levels = Field()
    comfort = Field()     #舒适度评分
    comment_count = Field()
    economy = Field()     #车辆油耗评分
    cost_efficiency = Field()   #车辆性价比评分
    post_at = Field()    #创建评论时间
    odometer = Field()        #行驶公里数
    content = Field()     #评价内容
    summary = Field()    #评价总结
    helpful_count = Field()
    interior = Field()    #内饰评分
    modified_at = Field()     #最后一次评论时间
    maneuver = Field()    #车辆操作评分
    nick_name = Field()     #评论人昵称
    power = Field()     #动力评分
    price = Field()     #购买价格
    series_id = Field()    #车辆型号id
    show_id = Field()    #此条评论id
    space = Field()     #空间评分
    spec = Field()    #车辆配置
    spec_id = Field()
    user_id = Field()    #评论人id
    visit_count = Field()     #此评论访问数
    brand = Field()    #汽车归属公司
    series = Field()    #汽车型号
    created_at = Field() #记录创建时间
    updated_at = Field() #记录修改时间
    content_id = Field() #索引
