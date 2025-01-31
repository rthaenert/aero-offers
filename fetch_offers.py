from datetime import datetime
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

import db
import pprint
from my_logging import *
from spiders import SegelflugDeSpider, FlugzeugMarktDeSpider, PlaneCheckComSpider
from mailer import send_mail

logger = logging.getLogger("fetch_offers")
try:
    conn = db.engine.connect()

    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    spiders = {SegelflugDeSpider.SegelflugDeSpider: None,
               FlugzeugMarktDeSpider.FlugzeugMarktDeSpider: None,
               PlaneCheckComSpider.PlaneCheckComSpider: None}
    for spider_cls in spiders.keys():
        crawler = runner.create_crawler(spider_cls)
        spiders[spider_cls] = crawler
        runner.crawl(crawler)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until all crawling jobs are finished

    stats_per_spider = {}

    for spider_cls, crawler in spiders.items():
        logger.debug("Fetching stats for spider: %s", spider_cls)
        stats = crawler.stats.get_stats()  # stats is a dictionary
        stats_per_spider[spider_cls.name] = crawler.stats.get_stats()

    msg = "Crawling offers completed at {0} \n\n {1} \n".format(str(datetime.now()), pprint.pformat(stats_per_spider))

    logger.debug("E-Mail msg: " + msg)
    send_mail(msg)
except Exception as e:
    msg = "Error connecting to the database: {0}".format(repr(e))
    logger.error(msg)
    send_mail(msg)
