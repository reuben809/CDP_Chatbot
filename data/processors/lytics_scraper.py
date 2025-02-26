import requests
from bs4 import BeautifulSoup
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LyticsScraper:
    def __init__(self):
        self.base_url = "https://docs.lytics.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.documents = []

    def scrape(self):
        """Main method to scrape Lytics documentation"""
        logger.info("Starting Lytics documentation scraping")

        try:
            main_page = self._get_page(self.base_url)
            if not main_page:
                return []

            section_links = self._extract_section_links(main_page)

            for section_url in section_links:
                self._process_section(section_url)
                time.sleep(1)

            logger.info(f"Completed scraping Lytics documentation. Total documents: {len(self.documents)}")
            return self.documents
        except Exception as e:
            logger.error(f"Error scraping Lytics documentation: {str(e)}")
            return []

    def _get_page(self, url):
        """Get page content with error handling"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None

    def _extract_section_links(self, soup):
        """Extract links to main documentation sections"""
        links = []
        nav_elements = soup.select("nav a")
        for link in nav_elements:
            href = link.get('href')
            if href and (href.startswith("/") or href.startswith("https://docs.lytics.com")):
                full_url = f"https://docs.lytics.com{href}" if href.startswith("/") else href
                if full_url not in links:
                    links.append(full_url)
        return links

    def _process_section(self, section_url):
        """Process a documentation section and its pages"""
        soup = self._get_page(section_url)
        if not soup:
            return

        page_content = self._extract_page_content(soup)
        if page_content:
            self.documents.append({"url": section_url, "content": page_content})
            logger.info(f"Scraped content from {section_url}")

    def _extract_page_content(self, soup):
        """Extract relevant page content"""
        content_div = soup.find("article") or soup.find("div", class_="content")
        return content_div.get_text(strip=True) if content_div else None


if __name__ == "__main__":
    scraper = LyticsScraper()
    docs = scraper.scrape()
    logger.info(f"Scraped {len(docs)} documents.")
