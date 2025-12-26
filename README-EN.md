# Btime Test - Dev RPA

## Overview
This project contains two Python scripts for automating data collection related to the topic "Series":

- **API collection** (`src/api_scraper.py`) — consumes a public API, normalizes the data, and writes it to CSV.

- **Web Scraping** (`src/web_scraper.py`) — uses Selenium to extract data from web pages, including strategies to handle common blocks and restrictions.

Both scripts generate well-structured CSV files in the output/ folder and follow good architecture practices such as separation of concerns and modularity.

## Repository Structure
- `main.py` — Orchestrates the execution of the scrapers
- `src/api_scraper.py` — API collection script
- `src/web_scraper.py` — Web scraper using Selenium
- `src/config.py` — Configurations and constants
- `src/utils.py` — Utility functions (CSV, XLSX, formatting)
- `log/logger.py` — Logger configuration
- `output/` — Results in CSV/XLSX and logs
- `requirements.txt` — Project dependencies

## Requirements
- Python 3.8+ (3.13.9)
- Install main dependencies: `pandas`, `requests`, `openpyxl`, `selenium`, `webdriver-manager`.

```bash
pip install -r requirements.txt
```

## How to Run
1. To run both scrapers sequentially (will generate CSVs in `output/`):

```bash
python main.py
```

2. Run individually:

- API:

```bash
python -m src.api_scraper
```

- Web Scraper:

```bash
python -m src.web_scraper
```

## Configuration

- Adjust `TOP_N` in `src/config.py` to control the number of collected items.
- `src/config.py` also defines the output directory and the URLs/addresses used.
- To run the web scraper in headless mode, enable the `headless` option in `setup_driver()` in `src/web_scraper.py`.

## Output (CSV)

- Both scrapers produce CSV files with a consistent schema to facilitate comparison and later analysis.
- Typical columns:

| Column  | Description                   |
|---------|-------------------------------|
| title   | Item title (e.g., series)     |
| year    | Release year                  |
| rating  | Rating or score               |
| genre   | Genre or category             |
| url     | Page or reference link        |

## Logs and Error Handling

- Logs are configured in `log/logger.py` and are shown in the console; messages indicate start/end of executions and errors.
- Each scraper has basic exception handling to improve robustness against network failures, unexpected responses, or DOM changes.

## Developer
| Name         | Email                     |
|--------------|---------------------------|
| Gabriel Lima | limaruasgabriel@gmail.com |