# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from spiders.items import get_engine


class SpidersPipeline:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_item(self, item, spider):
        item.commit_item(get_engine())
        return item
