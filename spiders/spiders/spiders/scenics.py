import json
import sqlite3

import scrapy


# noinspection PyAbstractClass
class StorySpider(scrapy.Spider):
    name = 'scenics'
    allowed_domains = ['travel.qunar.com']

    def __init__(self, source: str):
        super().__init__()
        self.source = source

    def start_requests(self):
        cursor = sqlite3.connect(self.source)
        for (stid,) in cursor.execute('SELECT stid FROM stories').fetchall():
            yield scrapy.Request('http://travel.qunar.com/analysis/api/note/poiLink2?bookId=' + str(stid), self.parse,
                                 cb_kwargs={'stid': stid})

    # noinspection PyMethodOverriding
    def parse(self, response, stid):
        data = json.loads(response.text)
        source = sqlite3.connect(self.source)
        cursor = source.cursor()
        index = 0
        for item in data["data"]["data"]:
            tag_num = item["links"][0]["link"].split("-")[1]
            tag = tag_num[0:2]
            num = int(tag_num[2:])
            if tag == 'cs':
                cursor.execute('SELECT COUNT(*) FROM visits WHERE vstid = ? AND vctid = ?', (stid, num))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('INSERT INTO visits VALUES (?, ?, ?, ?)', (stid, index, None, num))
            if tag == 'oi':
                cursor.execute('SELECT COUNT(*) FROM visits WHERE vstid = ? AND vscid = ?', (stid, num))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('INSERT INTO visits VALUES (?, ?, ?, ?)', (stid, index, num, None))
            index += 1
        source.commit()
