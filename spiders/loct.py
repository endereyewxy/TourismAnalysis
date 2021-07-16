from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'location', '-a', 'source=loct.db.050'])
