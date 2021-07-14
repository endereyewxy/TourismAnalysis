import json
from typing import Optional

import scrapy
import sqlalchemy

from spiders.items import get_engine, StoryItem, HowToItem, VisitItem, CityItem, ScenicItem


def int_or_none(s: str) -> Optional[int]:
    if s is None:
        return None
    if s[-1] == '万':
        return int(float(s[:-1]) * 10000)
    return int(s)


# noinspection PyAbstractClass
class StorySpider(scrapy.Spider):
    name = 'story'
    allowed_domains = ['travel.qunar.com']

    def __init__(self):
        super().__init__()
        conn = get_engine().connect()
        self.cs_set = {x for x, in conn.execute(sqlalchemy.select(CityItem.sqlmodel.c.ctid))}
        self.oi_set = {x for x, in conn.execute(sqlalchemy.select(ScenicItem.sqlmodel.c.scid))}
        self.st_set = {x for x, in conn.execute(sqlalchemy.select(StoryItem.sqlmodel.c.stid))}
        self.page = 2
        self.month_tag = ["&month=1_2_3", "&month=4_5_6", "&month=7_8_9", "&month=10_11_12"]
        self.days_tag = ["&days=1_2_3", "&days=4_5_6_7", "&days=8to10", "&days=11to15", "&days=16tom"]
        self.avg_price_tag = ["&avgPrice=1", "&avgPrice=2", "&avgPrice=3", "&avgPrice=4", "&avgPrice=5"]

    def start_requests(self):
        for month in self.month_tag:
            for days in self.days_tag:
                for avg_price in self.avg_price_tag:
                    for i in range(1, self.page + 1):
                        url = ('https://travel.qunar.com/travelbook/list.htm?page={}&order=hot_heat' + month + days
                               + avg_price).format(i)
                        yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        for each in response.xpath("//li/@data-url"):
            stid = each.extract().replace("/youji/", '')
            yield scrapy.Request(url='https://travel.qunar.com/travelbook/note/' + stid, callback=self.parse_story,
                                 cb_kwargs={'stid': int(stid)})

    # noinspection PyMethodMayBeStatic
    def parse_story(self, response, stid):
        story = StoryItem()
        story['stid'] = stid
        if response.xpath('//p[@class="b_crumb_cont"]/a[@target="_blank"]/text()').extract_first() is not None:
            story['loct'] = response.xpath('//p[@class="b_crumb_cont"]/a[@target="_blank"]/text()').extract_first() \
                .replace('\xa0', '').replace('旅游攻略', '')
        story['title'] = response.xpath('//p[@class="b_crumb_cont"]/span/text()')[-1].extract().replace('\xa0', '')

        info = response.xpath('//ul[@class="foreword_list"]')
        story['date_start'] = info.xpath('./li[@class="f_item when"]/p/span[@class="data"]/text()').extract_first()
        story['date_count'] = int_or_none(
            info.xpath('./li[@class="f_item howlong"]/p/span[@class="data"]/text()').extract_first())
        story['relp'] = info.xpath('./li[@class="f_item who"]/p/span[@class="data"]/text()').extract_first()
        story['cost'] = int_or_none(
            info.xpath('./li[@class="f_item howmuch"]/p/span[@class="data"]/text()').extract_first())

        story['auth'] = response.xpath('//div[@class="e_line2"]/ul/li/a/text()').extract_first()
        story['cmmt_count'] = int_or_none(
            response.xpath('//li[@class="nav_item comment"]//span[@class="num"]/text()').extract_first())
        story['like_count'] = int_or_none(
            response.xpath('//li[@class="nav_item like"]//span[@class="num"]/text()').extract_first())

        story['view_count'] = int_or_none(response.xpath('//span[@class="view_count"]/text()').extract_first())

        story['text_count'] = len(
            response.xpath('//div[@id="main_box"][@class="main_box clrfix"]').xpath('string(.)').extract_first())
        story['pict_count'] = len(response.xpath('//div[@class="b_panel_schedule"]//img'))

        yield story

        play_ways = response.xpath("//*[@id='js_mainleft']/div[2]/ul/li[5]/p/span[2]//text()").extract()
        for way in play_ways:
            if way.strip(' ') != '\xa0':
                how_to = HowToItem()
                how_to['hstid'] = stid
                how_to['h_tag'] = way.strip(' ')
                yield how_to

        yield scrapy.Request('http://travel.qunar.com/analysis/api/note/poiLink2?bookId=' + str(stid),
                             callback=self.parse_scenic, cb_kwargs={'stid': stid})

    def parse_scenic(self, response, stid):
        data = json.loads(response.text)
        index = 0
        for item in data["data"]["data"]:
            name = item["links"][0]["name"]
            link = item["links"][0]["link"]
            tag_num = link.split("-")[1]
            tag = tag_num[0:2]
            num = tag_num[2:]
            cb_kwargs = {'stid': stid, 'id_': int(num), 'name': name, 'index': index}
            if tag == 'cs':
                if int(num) not in self.cs_set:
                    self.cs_set.add(int(num))
                    yield scrapy.Request(link, callback=self.find_prov, cb_kwargs=cb_kwargs)
            if tag == 'oi':
                if int(num) not in self.oi_set:
                    self.oi_set.add(int(num))
                    yield scrapy.Request(link, callback=self.find_city, cb_kwargs=cb_kwargs)
            index += 1

    # noinspection PyMethodMayBeStatic
    def find_prov(self, response, stid, id_, name, index):
        prov_name = response.xpath('//li[@class="item pull"]/a/@title')[-1].extract()
        city = CityItem()
        city['ctid'] = id_
        city['name'] = name
        city['prov'] = prov_name
        yield city
        visit = VisitItem()
        visit['vstid'] = stid
        visit['index'] = index
        visit['vctid'] = id_
        yield visit

    def find_city(self, response, stid, id_, name, index):
        try:
            city_name = response.xpath('//li[@class="item pull"]/a/@title')[-1].extract()
            city_id = int(response.xpath('//li[@class="item pull"]/a/@href')[-1].extract().split("-")[1][2:])
            if city_id not in self.cs_set:
                self.cs_set.add(city_id)
                prov_name = response.xpath('//li[@class="item pull"]/a/@title')[-2].extract()
                city = CityItem()
                city['ctid'] = city_id
                city['name'] = city_name
                city['prov'] = prov_name
                yield city
            scenic = ScenicItem()
            scenic['scid'] = id_
            scenic['name'] = name
            scenic['city'] = city_id
            yield scenic
            visit = VisitItem()
            visit['vstid'] = stid
            visit['index'] = index
            visit['vscid'] = id_
            yield visit
        except IndexError:
            pass
