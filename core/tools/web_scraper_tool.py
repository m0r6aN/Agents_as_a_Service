# File: core/tools/web_scraper_tool.py

from typing import Dict
from venv import logger
import requests
from bs4 import BeautifulSoup
from tool_base import BaseTool

class WebScraperTool(BaseTool):
    """
    Tool for scraping web pages and extracting information.
    """

    def __init__(self):
        super().__init__(
            name="WebScraper",
            description="Scrapes web pages and extracts text content.",
            version="1.0"
        )

    def execute(self, url: str, parser: str = "html.parser") -> Dict[str, any]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, parser)
            text = soup.get_text(separator=' ', strip=True)
            return {"url": url, "content": text}
        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {"url": url, "error": str(e)}