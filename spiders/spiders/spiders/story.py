from typing import Optional

import scrapy

from spiders.items import StoryItem


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

    def start_requests(self):
        for i in range(1, 2):
            url = 'https://travel.qunar.com/travelbook/list.htm?page={}&order=hot_heat'.format(i)
            yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        for each in response.xpath("//li/@data-url"):
            stid = each.extract().replace("/youji/", '')
            yield scrapy.Request(url='https://travel.qunar.com/travelbook/note/' + stid, callback=self.parse_story,
                                 cb_kwargs={'stid': stid})

    def parse_story(self, response, stid):
        story = StoryItem()

        story['stid'] = stid
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
