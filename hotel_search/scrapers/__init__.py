from hotel_search.scrapers.expedia import ExpediaScraper
from hotel_search.scrapers.orbitz import OrbitzScraper
from hotel_search.scrapers.priceline import PricelineScraper
from hotel_search.scrapers.travelocity import TravelocityScraper
from hotel_search.scrapers.hilton import HiltonScraper
from .common import GeneratorPipeline
from functools import partial


SCRAPERS = [
    ExpediaScraper,
    OrbitzScraper,
    PricelineScraper,
    TravelocityScraper,
    HiltonScraper,
]
SCRAPER_MAP = {s.provider.lower(): s for s in SCRAPERS}

def get_all_scrapers(scrapers):
    return GeneratorPipeline(SCRAPERS)

SCRAPER_MAP['all'] = partial(get_all_scrapers, SCRAPERS)


def get_scraper(provider):
    return SCRAPER_MAP.get(provider.lower())
