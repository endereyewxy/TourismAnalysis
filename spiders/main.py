import sys

import scrapy.cmdline

from spiders.settings import SQLITE_DB_NAME

if __name__ == '__main__':
    page_l, page_r = int(sys.argv[1]), int(sys.argv[2])
    for page in range(page_l, page_r + 1):
        for _ in range(5):
            scrapy.cmdline.execute(['scrapy', 'crawl', 'story', '-a', 'page=' + str(page)])
        scrapy.cmdline.execute(['cp', SQLITE_DB_NAME, SQLITE_DB_NAME + '.%3d' % page])
