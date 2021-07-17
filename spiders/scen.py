from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'scenics', '-a', 'source=loct.db.050'])
