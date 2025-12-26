import requests
import pandas as pd

from log.logger import get_logger
from src.utils import save_results
from src.config import TVMAZE_URL, TOP_N, DATA_DIR

logger = get_logger(__name__)


def fetch_series(url):
    """
    Makes a request to the TVmaze API and returns a list of series in JSON format.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {e}")
        return []


def format_series(series_list, top_n=TOP_N):
    """
    Formats the list of series into a DataFrame, handling missing values.
    Returns only the top_n series sorted by rating.
    """
    formatted = []
    for index, show in enumerate(series_list):
        title = show.get('name', 'N/A')
        premiered = show.get('premiered')
        year = premiered[:4] if premiered else 'N/A'
        try:
            rating = float(show.get('rating', {}).get('average') or 0)
        except ValueError:
            rating = 0.0
        genres = ', '.join(show.get('genres', []))
        url = show.get('url', 'N/A')

        logger.info(
            f"{index + 1}/{len(series_list)}: Processed '{title} - {year} - {rating} - {genres}'")
        formatted.append({
            'title': title,
            'year': year,
            'rating': rating,
            'genres': genres,
            'url': url
        })

    df = pd.DataFrame(formatted)
    df = df.sort_values(by='rating', ascending=False).head(top_n)
    return df


def run_api_scraper(top_n=None):
    """
    Run the API scraper and save results to DATA_DIR.
    """
    if top_n is None:
        top_n = TOP_N

    series_list = fetch_series(TVMAZE_URL)
    if not series_list:
        logger.warning("No data received from the API. Exiting script.")
        return

    df = format_series(series_list, top_n=top_n)
    save_results(df, f"{DATA_DIR}/api_top_series.csv",
                 f"{DATA_DIR}/api_top_series.xlsx")
    logger.info("API scraping finished successfully.")


if __name__ == "__main__":
    run_api_scraper()
