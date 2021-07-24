import re
import sqlite3

import scrapy


# noinspection PyAbstractClass
class StorySpider(scrapy.Spider):
    name = 'location'
    allowed_domains = ['travel.qunar.com']

    def __init__(self, source: str):
        super().__init__()
        self.source = source

    def start_requests(self):
        cursor = sqlite3.connect(self.source)
        try:
            cursor.execute('ALTER TABLE scenics ADD COLUMN lng REAL')
            cursor.execute('ALTER TABLE scenics ADD COLUMN lat REAL')
        except sqlite3.OperationalError:
            pass
        for (scid,) in cursor.execute('SELECT scid FROM scenics WHERE lng IS NULL OR lat IS NULL').fetchall():
            yield scrapy.Request('http://travel.qunar.com/p-oi' + str(scid), self.parse, cb_kwargs={'scid': scid})

    # noinspection PyMethodOverriding
    def parse(self, response, scid):
        location = re.search(r'latlng="([-\d.,]+)"', response.text).group(1).split(',')
        lng, lat = location[1], location[0]

        source = sqlite3.connect(self.source)
        source.execute('UPDATE scenics SET lng = ?, lat = ? WHERE scid = ?', (lng, lat, scid))
        source.commit()
