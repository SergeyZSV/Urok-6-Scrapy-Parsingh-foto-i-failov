import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class UnsplashCrawlerSpider(CrawlSpider):
    name = "unsplash_crawler"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    # в первом правиле указан индекс, чтобы быстрее парсил
    rules = (Rule(LinkExtractor(restrict_xpaths=("//figure[@itemprop = 'image'][1]")), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths=("//ul[@class = 'ossD0 GxtYC N46Vv'][1]")))
            )

    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashItem(), response=response)
            # loader.default_input_processor = MapCompose(str.strip)
        loader.add_xpath("name", "//img/@alt[0]")
        loader.add_xpath("url", "//img/@src[0]")
        
        yield loader.load_item()