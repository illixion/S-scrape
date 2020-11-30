from scrapy.crawler import CrawlerProcess

from .sscrape.spiders.autoss_auto_category import AutoSsAutoCategorySpider
from .sscrape.spiders.autoss_auto import AutoSsAutoSpider
from .sscrape.spiders.elots_auto_category import ELotsAutoCategorySpider
from .sscrape.spiders.elots_auto import ELotsAutoSpider
from .sscrape.spiders.elots_estate import ELotsEstateSpider
from .sscrape.spiders.mm_auto_category import MmAutoCategorySpider
from .sscrape.spiders.mm_auto import MmAutoSpider
from .sscrape.spiders.mm_estate import MmEstateSpider
from .sscrape.spiders.reklama_auto_category import ReklamaAutoCategorySpider
from .sscrape.spiders.reklama_auto import ReklamaAutoSpider
from .sscrape.spiders.reklama_estate import ReklamaEstateSpider
from .sscrape.spiders.ss_auto_category import SsAutoCategorySpider
from .sscrape.spiders.ss_auto import SsAutoSpider
from .sscrape.spiders.ss_estate import SsEstateSpider
from .sscrape.spiders.viss_auto_category import VissAutoCategorySpider
from .sscrape.spiders.viss_auto import VissAutoSpider
from .sscrape.spiders.viss_estate import VissEstateSpider

process = CrawlerProcess()
process.crawl(AutoSsAutoCategorySpider)
process.crawl(AutoSsAutoSpider)
process.crawl(ELotsAutoCategorySpider)
process.crawl(ELotsAutoSpider)
process.crawl(ELotsEstateSpider)
process.crawl(MmAutoCategorySpider)
process.crawl(MmAutoSpider)
process.crawl(MmEstateSpider)
process.crawl(ReklamaAutoCategorySpider)
process.crawl(ReklamaAutoSpider)
process.crawl(ReklamaEstateSpider)
process.crawl(SsAutoCategorySpider)
process.crawl(SsAutoSpider)
process.crawl(SsEstateSpider)
process.crawl(VissAutoCategorySpider)
process.crawl(VissAutoSpider)
process.crawl(VissEstateSpider)
process.start()
