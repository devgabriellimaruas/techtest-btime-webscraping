import pandas as pd

from log.logger import get_logger

logger = get_logger(__name__)


def save_results(df: pd.DataFrame, csv_filename: str, excel_filename: str):
    """Save DataFrame to CSV and Excel files."""
    try:
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        df.to_excel(excel_filename, index=False, engine="openpyxl")
        logger.info(f"Saved files: {csv_filename}, {excel_filename}")
    except Exception as e:
        logger.error(f"Failed to save files: {e}")
