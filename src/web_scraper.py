import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from log.logger import get_logger
from src.utils import save_results
from src.config import IMDB_URL, TOP_N, DATA_DIR

logger = get_logger(__name__)


def setup_driver(headless=True):
    """Setup Chrome WebDriver with options."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def extract_genres(driver):
    """Extract genres from the modal and close it."""
    try:
        genres_elements = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((
                By.XPATH,
                "/html/body/div[4]/div[2]/div/div[2]/div/div/div[1]/div[2]/ul[2]/li"
            ))
        )
        genres = ", ".join([g.text.strip()
                           for g in genres_elements if g.text.strip()])
    except TimeoutException:
        genres = "N/A"

    # Close modal
    try:
        close_button = driver.find_element(
            By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/button")
        driver.execute_script("arguments[0].click();", close_button)
    except NoSuchElementException:
        pass

    return genres


def scrape_top_series(driver, top_n=TOP_N):
    """Scrape the top N TV series from IMBD Top TV page."""
    driver.get(IMDB_URL)

    # Wait for the page title to load
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[@id='__next']/main/div/div[3]/section/div/div[1]/div/div[2]/hgroup/h1")
            )
        )
    except TimeoutException:
        logger.error("IMBD page did not load in time.")
        return []

    wait = WebDriverWait(driver, 10)
    series_data = []

    logger.info("Started scraping top series...")
    for row in range(1, top_n + 1):
        try:
            # Title
            title = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    f"//*[@id='__next']/main/div/div[3]/section/div/div[2]/div/ul/li[{row}]/div/div/div/div/div[2]/div[2]"
                ))
            ).text

            # Year
            year_element = driver.find_element(
                By.XPATH,
                f"//*[@id='__next']/main/div/div[3]/section/div/div[2]/div/ul/li[{row}]/div/div/div/div/div[2]/div[3]/span[1]"
            )
            year = year_element.text[:4] if year_element.text else "N/A"

            # Rating
            rating_element = driver.find_element(
                By.XPATH,
                f"//*[@id='__next']/main/div/div[3]/section/div/div[2]/div/ul/li[{row}]/div/div/div/div/div[2]/span/div/span/span[1]"
            )
            try:
                rating = float(rating_element.text.replace(
                    ",", ".")) if rating_element.text else 0.0
            except ValueError:
                rating = 0.0

            # Click info button to open modal for genres
            button_info = driver.find_element(
                By.XPATH,
                f"//*[@id='__next']/main/div/div[3]/section/div/div[2]/div/ul/li[{row}]/div/div/div/div/div[3]/button"
            )
            driver.execute_script("arguments[0].click();", button_info)

            # Extract genres
            genres = extract_genres(driver)

            # URL
            url_link = driver.find_element(
                By.XPATH,
                f"//*[@id='__next']/main/div/div[3]/section/div/div[2]/div/ul/li[{row}]/div/div/div/div/div[2]/div[2]/a"
            ).get_attribute("href")

            series_data.append({
                "title": title,
                "year": year,
                "rating": rating,
                "genres": genres,
                "url": url_link
            })

            logger.info(
                f"{row}/{TOP_N}: Processed '{title} - {year} - {rating} - {genres}'")

        except Exception as e:
            logger.warning(f"Failed to scrape row {row}: {e}")

    return series_data


def run_web_scraper(top_n=None):
    """
    Run the web scraper and save results to DATA_DIR.
    """
    if top_n is None:
        top_n = TOP_N

    driver = setup_driver(headless=True)
    try:
        series = scrape_top_series(driver, top_n=top_n)
        if series:
            df = pd.DataFrame(series).sort_values(by="rating", ascending=False)
            save_results(df, f"{DATA_DIR}/ws_top_series.csv",
                         f"{DATA_DIR}/ws_top_series.xlsx")
        else:
            logger.info("No series scraped.")
    finally:
        driver.quit()
        logger.info("Scraping finished.")


if __name__ == "__main__":
    run_web_scraper()
