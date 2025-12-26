from pathlib import Path

# Root of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output folder
DATA_DIR = PROJECT_ROOT / "output"
DATA_DIR.mkdir(exist_ok=True)

# URLs
TVMAZE_URL = "https://api.tvmaze.com/shows"
IMDB_URL = "https://www.imdb.com/pt/chart/toptv/"

# Number of top series to scrape
TOP_N = 10
