import os
import sys

import scrapy.crawler
import scrapy.utils.log
import scrapy.utils.project
from twisted.internet import defer, reactor

import spiders.spiders.story
from spiders.settings import SQLITE_DB_NAME

if __name__ == '__main__':
    page_l, page_r = int(sys.argv[1]), int(sys.argv[2])
    runner = scrapy.crawler.CrawlerRunner(scrapy.utils.project.get_project_settings())
    scrapy.utils.log.configure_logging()


    @defer.inlineCallbacks
    def _run():
        for page in range(page_l, page_r + 1):
            for _ in range(5):
                yield runner.crawl(spiders.spiders.story.StorySpider, page=page)
            os.system('cp %s %s.%03d' % (SQLITE_DB_NAME, SQLITE_DB_NAME, page))
        # noinspection PyUnresolvedReferences
        reactor.stop()


    _run()
    # noinspection PyUnresolvedReferences
    reactor.run()
