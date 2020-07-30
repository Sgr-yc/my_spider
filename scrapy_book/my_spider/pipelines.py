# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class MySpiderPipeline:
    """
    功能：保存item数据
    """

    def __init__(self):
        self.filename = open("tencent.json", "w")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()
