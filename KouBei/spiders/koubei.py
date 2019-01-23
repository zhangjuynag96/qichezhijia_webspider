# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy import Request
from KouBei.items import AutohomeKoubeiViewItem
import time
from scrapy.http import TextResponse
import json
import jsonpath_rw_ext
import datetime

class KoubeiSpider(scrapy.Spider):
    name = 'koubei'
    allowed_domains = ['k.autohome.com.cn']
    id_url = 'https://k.autohome.com.cn/ajax/getSceneSelectCar?minprice=2&maxprice=110&_appid=koubei&level={level}'
    detail_url = 'https://k.m.autohome.com.cn/ajax/series/getserieskoubeilist?pageIndex={index}&PageCount={pagecount}&isSeries=true&Id={sid}&SemanticKey=&IsSemantic=false&GradeEnum=0&order=1&yearId=0&isSending=true'


    def start_requests(self):
        #各种车辆的类别编号，可自行添加，此爬虫主要针对A型，B型，SUV车型
        list = [3, 4, 16, 17, 18, 19, 20]

        for level in list:
            #获取每个车类别下的所有车型的id
            result = requests.get(self.id_url.format(level=level))
            pattern_sid = re.compile('"SeriesId":(\d+).*?"BrandName":"(.*?)".*?"SeriesName":"(.*?)"', re.S)
            sids = pattern_sid.findall(result.text)

            for sid in sids:
                #获取每个车型下所有评论的页数
                page_counts = requests.get(
                    'https://k.m.autohome.com.cn/ajax/series/getserieskoubeilist?pageIndex=1&PageCount=&isSeries=true&Id=' + str(
                        sid[0]) + '&SemanticKey=&IsSemantic=false&GradeEnum=0&order=1&yearId=0&isSending=true')
                pattern_page = re.compile('.*?"pagecount":(.*?),', re.S)
                pagecount = pattern_page.findall(page_counts.text)
                pagecount = int(pagecount[0])

                #利用获得的车辆id与评论页数构造目的url
                for index in range(1,pagecount+1):
                    yield Request(self.detail_url.format(index=index, pagecount=pagecount, sid=str(sid[0])), callback=self.get_detail)

    def get_detail(self,response):
        #使用jsonpath_rw_ext提取数据
        html = json.loads(response.text)
        
        actual_battery_consumption =  jsonpath_rw_ext.match('$..actual_battery_consumption',html)
        actual_oil_consumption = jsonpath_rw_ext.match('$..actual_oil_consumption',html)
        apperance = jsonpath_rw_ext.match('$..apperance',html)
        boughtCityName = jsonpath_rw_ext.match('$..boughtCityName',html)
        bought_city = jsonpath_rw_ext.match('$..bought_city',html)
        bought_date = jsonpath_rw_ext.match('$..bought_date',html)
        bought_place = jsonpath_rw_ext.match('$..bought_place',html)
        bought_province = jsonpath_rw_ext.match('$..bought_province',html)
        carOwnerLevels = jsonpath_rw_ext.match('$..carOwnerLevels',html)
        comfortableness = jsonpath_rw_ext.match('$..comfortableness',html)
        commentCount = jsonpath_rw_ext.match('$..commentCount',html)
        consumption = jsonpath_rw_ext.match('$..consumption',html)
        cost_efficient = jsonpath_rw_ext.match('$..cost_efficient',html)
        created = jsonpath_rw_ext.match('$..created',html)
        driven_kilometers = jsonpath_rw_ext.match('$..driven_kilometers',html)
        feeling = jsonpath_rw_ext.match('$..feeling',html)
        feeling_summary = jsonpath_rw_ext.match('$..feeling_summary',html)
        helpfulCount = jsonpath_rw_ext.match('$..helpfulCount',html)
        interior = jsonpath_rw_ext.match('$..interior',html)
        last_edit = jsonpath_rw_ext.match('$..last_edit',html)
        maneuverability = jsonpath_rw_ext.match('$..maneuverability',html)
        nickName = jsonpath_rw_ext.match('$..nickName',html)
        power = jsonpath_rw_ext.match('$..power',html)
        price = jsonpath_rw_ext.match('$..price',html)
        seriesId = jsonpath_rw_ext.match('$..seriesId',html)
        showId = jsonpath_rw_ext.match('$..showId',html)
        space = jsonpath_rw_ext.match('$..space',html)
        specName = jsonpath_rw_ext.match('$..specName',html)
        specid = jsonpath_rw_ext.match('$..specid',html)
        userid = jsonpath_rw_ext.match('$..userid',html)
        visitCount = jsonpath_rw_ext.match('$..visitCount',html)

        #从其他页面获取该id车型的车型名称与所属公司
        pattern_test = re.compile('.*?rue&Id=(.*?)&')
        x = pattern_test.findall(response.url)
        name_url = 'https://www.autohome.com.cn/{seriesId}'.format(seriesId=x[0])
        name = requests.get(name_url)
        name = TextResponse(body=name.content, url=name_url)
        BrandName = name.css('.athm-sub-nav__car__name a::text').extract_first()
        SeriesName = name.css('.athm-sub-nav__car__name h1::text').extract_first()

        # 遍历匹配到的信息，并将其存入字典
        for i in range(0,len(nickName)):

            item = AutohomeKoubeiViewItem()
            # 除去文本中的换行符
            feelings = re.sub('\r+|\n+', '', str(feeling[i]))

            item['energy_consump'] = str(actual_battery_consumption[i])
            item['gas_consump'] = str(actual_oil_consumption[i])
            item['apperance'] = str(apperance[i])
            item['bought_city_name'] = str(boughtCityName[i])
            item['bought_city'] = str(bought_city[i])
            item['bought_date'] = str(bought_date[i])
            item['bought_place'] = str(bought_place[i])
            item['bought_province'] = str(bought_province[i])
            item['car_owner_levels'] = str(carOwnerLevels[i])
            item['comfort'] = str(comfortableness[i])
            item['comment_count'] = str(commentCount[i])
            item['economy'] = str(consumption[i])
            item['cost_efficiency'] = str(cost_efficient[i])
            item['post_at'] = str(created[i])
            item['odometer'] = str(driven_kilometers[i])
            item['content'] = feelings
            item['summary'] = str(feeling_summary[i])
            item['helpful_count'] = str(helpfulCount[i])
            item['interior'] = str(interior[i])
            item['modified_at'] = str(last_edit[i])
            item['maneuver'] = str(maneuverability[i])
            item['nick_name'] = str(nickName[i])
            item['power'] = str(power[i])
            item['price'] = str(price[i])
            item['series_id'] = str(seriesId[i])
            item['show_id'] = str(showId[i])
            item['space'] = str(space[i])
            item['spec'] = str(specName[i])
            item['spec_id'] = str(specid[i])
            item['user_id'] = str(userid[i])
            item['visit_count'] = str(visitCount[i])
            item['brand'] = BrandName
            item['series'] = SeriesName
            item['created_at'] = datetime.datetime.now()
            item['updated_at'] = datetime.datetime.now()
            item['content_id'] = 0

            yield item

    def parse(self, response):
        pass

