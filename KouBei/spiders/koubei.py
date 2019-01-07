# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy import Request
from KouBei.items import AutohomeKoubeiViewItem
import time
from scrapy.http import TextResponse

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
        # 正则匹配需要的信息，可继续往内添加需要的信息
        pattern = re.compile(
            '.*?"actual_battery_consumption":(\-\d+|\d+\.\d+).*?"actual_oil_consumption":(\-\d+|\d+\.\d+)'
            '.*?"apperance":(\d+).*?"boughtCityName":"(.*?)".*?"bought_city":(\d+).*?"bought_date":"(.*?)"'
            '.*?"bought_place":(\-\d+|\d+).*?"bought_province":(\d+).*?"carOwnerLevels":(\d+).*?"comfortableness":(\d+)'
            '.*?"commentCount":(\d+).*?"consumption":(\d+).*?"cost_efficient":(\d+).*?"created":"(.*?)"'
            '.*?"driven_kilometers":(\-\d+|\d+).*?"feeling":"(.*?)".*?"feeling_summary":"(.*?)".*?"helpfulCount":(\d+)'
            '.*?"interior":(\d+).*?"last_edit":"(.*?)".*?"maneuverability":(\d+).*?"nickName":"(.*?)".*?"power":(\d+)'
            '.*?"price":(\d+\.\d+).*?"seriesId":(\d+).*?"showId":"(.*?)".*?"space":(\d+).*?"specName":"(.*?)"'
            '.*?"specid":(\d+).*?"userid":(\d+).*?"visitCount":(\d+)', re.S)
        details = pattern.findall(response.text)

        #从其他页面获取该id车型的车型名称与所属公司
        pattern_test = re.compile('.*?rue&Id=(.*?)&')
        x = pattern_test.findall(response.url)
        name_url = 'https://www.autohome.com.cn/{seriesId}'.format(seriesId=x[0])
        name = requests.get(name_url)
        name = TextResponse(body=name.content, url=name_url)
        BrandName = name.css('.athm-sub-nav__car__name a::text').extract_first()
        SeriesName = name.css('.athm-sub-nav__car__name h1::text').extract_first()

        # 遍历匹配到的信息，并将其存入字典
        for result in details:

            item = AutohomeKoubeiViewItem()
            # 除去文本中的换行符
            feeling = result[15]
            feelings = re.sub(r'\\r|\\n', '', feeling)

            item['actual_battery_consumption'] = result[0]
            item['actual_oil_consumption'] = result[1]
            item['apperance'] = result[2]
            item['boughtCityName'] = result[3]
            item['bought_city'] = result[4]
            item['bought_date'] = result[5]
            item['bought_place'] = result[6]
            item['bought_province'] = result[7]
            item['carOwnerLevels'] = result[8]
            item['comfortableness'] = result[9]
            item['commentCount'] = result[10]
            item['consumption'] = result[11]
            item['cost_efficient'] = result[12]
            item['created'] = result[13]
            item['driven_kilometers'] = result[14]
            item['feeling'] = feelings
            item['feeling_summary'] = result[16]
            item['helpfulCount'] = result[17]
            item['interior'] = result[18]
            item['last_edit'] = result[19]
            item['maneuverability'] = result[20]
            item['nickName'] = result[21]
            item['power'] = result[22]
            item['price'] = result[23]
            item['seriesId'] = result[24]
            item['showId'] = result[25]
            item['space'] = result[26]
            item['specName'] = result[27]
            item['specid'] = result[28]
            item['userid'] = result[29]
            item['visitCount'] = result[30]
            item['BrandName'] = BrandName
            item['SeriesName'] = SeriesName

            yield item

    def parse(self, response):
        pass

