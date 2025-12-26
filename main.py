from src.web_scraper import run_web_scraper
from src.api_scraper import run_api_scraper
from src.config import TOP_N
from log.logger import get_logger

logger = get_logger(__name__)


def main():
    # Run API scraper
    logger.info('Starting data extraction with API.')
    run_api_scraper(top_n=TOP_N)
    logger.info('Data extraction with API completed.')

    # Run Web scraper
    logger.info('Starting data extraction with Web Scraping.')
    run_web_scraper(top_n=TOP_N)
    logger.info('Data extraction with Web Scraping completed.')


if __name__ == "__main__":
    main()
